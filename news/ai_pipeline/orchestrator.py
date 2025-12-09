"""
AI News Orchestrator
Main pipeline coordinator for AI-generated news articles

Task 2.3: Orchestrator Implementation
- AINewsOrchestrator class
- Initialize LLM instances (GPT-4, Claude)
- Register all pipeline stages
- process_article() main method
- Error handling and retry logic
- Stage transition management
- Logging and progress tracking
"""


"""
AI News Pipeline Orchestrator

Phase 2, Task 2.3: Main orchestrator for coordinating the entire AI content generation pipeline.
Uses LangChain to manage multi-stage article generation with quality control.

This orchestrator aligns with AI Analitica's mission:
- Unbiased, data-driven news analysis
- Multiple AI models for cross-validation
- Comprehensive quality checks for bias, facts, and perspectives
"""

import os
import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from decimal import Decimal

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage

# Django imports
from django.conf import settings
from django.utils import timezone

# Import models (assuming Django context)
try:
    from news.ai_models import AIArticle, AIWorkflowLog, AIGenerationConfig
except ImportError:
    # For development/testing outside Django
    AIArticle = None
    AIWorkflowLog = None
    AIGenerationConfig = None

# Import pipeline components (to be created in Phase 3)
# Uncomment these as components are built
# from .chains.content_generator import ContentGenerationChain
# from .chains.humanizer import HumanizationChain
# from .chains.seo_optimizer import SEOOptimizationChain
# from .chains.meta_generator import MetaGenerationChain
from .agents.research_agent import ResearchAgent
# from .tools.keyword_scraper import KeywordResearchTool
# from .tools.ai_detector import AIDetectionTool
# from .tools.plagiarism_checker import PlagiarismChecker
# from .tools.bias_detector import BiasDetectionTool
# from .tools.fact_verifier import FactVerificationTool
# from .tools.perspective_analyzer import PerspectiveAnalyzer
# from .tools.image_generator import ImageGenerationTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AINewsOrchestrator:
    """
    Main orchestrator for AI news generation pipeline.
    
    Coordinates multiple AI agents and tools through a multi-stage workflow:
    1. Keyword Analysis & Research
    2. Content Generation
    3. Humanization
    4. Quality Checks (AI Detection, Plagiarism, Bias, Facts, Perspectives)
    5. SEO Optimization
    6. Meta Tags Generation
    7. Image Generation
    8. Finalization
    
    Ensures all content meets AI Analitica's standards for objectivity and quality.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the orchestrator with AI models and pipeline components.
        
        Args:
            config: Optional configuration dictionary to override defaults
        """
        self.config = config or self._load_default_config()
        
        # Initialize LLM instances
        self._init_llms()
        
        # Initialize pipeline stages
        self.stages = {
            'keyword_analysis': self._keyword_analysis,
            'research': self._research,
            'outline': self._create_outline,
            'content_generation': self._generate_content,
            'humanization': self._humanize_content,
            'ai_detection': self._check_ai_detection,
            'plagiarism_check': self._check_plagiarism,
            'bias_detection': self._check_bias,
            'fact_verification': self._verify_facts,
            'perspective_analysis': self._analyze_perspectives,
            'seo_optimization': self._optimize_seo,
            'meta_generation': self._generate_meta,
            'image_generation': self._generate_image,
            'finalization': self._finalize,
        }
        
        # Track pipeline state
        self.current_article_id = None
        self.pipeline_start_time = None
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration from settings or environment."""
        return {
            'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
            'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY', ''),
            'gemini_api_key': os.getenv('GEMINI_API_KEY', ''),
            'default_provider': 'google',  # Changed to Gemini
            'default_model': 'gemini-exp-1206',  # Gemini 3 Pro (experimental release)
            'temperature': 0.7,
            'max_tokens': 32000,  # Gemini 3 supports very large context
            'max_retries': 3,
            'quality_thresholds': {
                'max_ai_score': 50.0,
                'max_plagiarism': 5.0,
                'min_seo_score': 75.0,
                'min_readability': 60.0,
                'max_bias_score': 20.0,  # AI Analitica standard
                'min_fact_check': 80.0,
            }
        }
    
    def _init_llms(self):
        """Initialize Language Model instances."""
        try:
            # Primary model: Gemini for content generation
            provider = self.config.get('default_provider', 'google')
            
            if provider == 'google' and self.config.get('gemini_api_key'):
                self.llm_primary = ChatGoogleGenerativeAI(
                    model=self.config['default_model'],
                    temperature=self.config['temperature'],
                    max_output_tokens=self.config['max_tokens'],
                    google_api_key=self.config['gemini_api_key']
                )
                logger.info(f"Primary LLM: Gemini ({self.config['default_model']})")
            elif provider == 'openai' and self.config.get('openai_api_key'):
                self.llm_primary = ChatOpenAI(
                    model=self.config.get('default_model', 'gpt-4-turbo-preview'),
                    temperature=self.config['temperature'],
                    max_tokens=self.config['max_tokens'],
                    openai_api_key=self.config['openai_api_key']
                )
                logger.info(f"Primary LLM: OpenAI ({self.config['default_model']})")
            else:
                raise ValueError(f"Invalid provider '{provider}' or missing API key")
            
            # Secondary model: Claude for cross-validation and bias checking
            if self.config.get('anthropic_api_key'):
                self.llm_secondary = ChatAnthropic(
                    model='claude-3-5-sonnet-20241022',
                    temperature=0.3,  # Lower temp for quality checks
                    anthropic_api_key=self.config['anthropic_api_key']
                )
                logger.info("Secondary LLM: Claude (for cross-validation)")
            else:
                self.llm_secondary = None
                logger.warning("Claude API key not found. Cross-validation will use primary model.")
            
            logger.info("LLMs initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLMs: {e}")
            raise
    
    # ========================================================================
    # Main Pipeline Execution
    # ========================================================================
    
    async def process_article(self, article_id: str, start_stage: str = 'keyword_analysis') -> Dict[str, Any]:
        """
        Process an article through the complete pipeline.
        
        Args:
            article_id: UUID of the AIArticle to process
            start_stage: Stage to start from (default: 'keyword_analysis')
            
        Returns:
            Dictionary containing final article data and metadata
        """
        self.current_article_id = article_id
        self.pipeline_start_time = datetime.now()
        
        logger.info(f"Starting pipeline for article {article_id} from stage: {start_stage}")
        
        try:
            # Load article from database
            article = await self._load_article(article_id)
            
            # Update status
            await self._update_article_status(
                article_id,
                status='generating',
                workflow_stage=start_stage
            )
            
            # Execute pipeline stages sequentially
            context = {'article_id': article_id}
            
            # Skip stages before start_stage
            stage_names = list(self.stages.keys())
            start_index = stage_names.index(start_stage) if start_stage in stage_names else 0
            
            for i, (stage_name, stage_func) in enumerate(self.stages.items()):
                # Skip stages before the start_stage
                if i < start_index:
                    logger.info(f"Skipping stage: {stage_name}")
                    continue
                    
                logger.info(f"Executing stage: {stage_name}")
                
                # Create workflow log entry
                log_id = await self._create_workflow_log(
                    article_id, stage_name, 'started'
                )
                
                try:
                    # Execute stage
                    stage_start = datetime.now()
                    result = await stage_func(article, context)
                    stage_duration = (datetime.now() - stage_start).total_seconds()
                    
                    # Update context with stage results
                    context[stage_name] = result
                    
                    # Log success
                    await self._complete_workflow_log(
                        log_id, result, stage_duration
                    )
                    
                    # Update article workflow stage
                    await self._update_article_status(
                        article_id,
                        workflow_stage=stage_name
                    )
                    
                    logger.info(f"Stage {stage_name} completed in {stage_duration:.2f}s")
                    
                except Exception as e:
                    logger.error(f"Stage {stage_name} failed: {e}")
                    
                    # Log failure
                    await self._fail_workflow_log(log_id, str(e))
                    
                    # Update article as failed
                    await self._update_article_status(
                        article_id,
                        status='failed',
                        workflow_stage=stage_name,
                        error=str(e)
                    )
                    
                    # Check if we should retry
                    article = await self._load_article(article_id)
                    if article.retry_count < self.config['max_retries']:
                        logger.info(f"Retrying article {article_id} (attempt {article.retry_count + 1})")
                        return await self.retry_article(article_id, stage_name)
                    
                    raise
            
            # Pipeline completed successfully
            total_time = (datetime.now() - self.pipeline_start_time).total_seconds()
            
            await self._update_article_status(
                article_id,
                status='reviewing',
                workflow_stage='completed',
                generation_time=int(total_time)
            )
            
            logger.info(f"Pipeline completed for article {article_id} in {total_time:.2f}s")
            
            return {
                'success': True,
                'article_id': article_id,
                'total_time': total_time,
                'context': context
            }
            
        except Exception as e:
            logger.error(f"Pipeline failed for article {article_id}: {e}")
            return {
                'success': False,
                'article_id': article_id,
                'error': str(e)
            }
    
    # ========================================================================
    # Pipeline Stage Implementations
    # ========================================================================
    
    async def _keyword_analysis(self, article, context: Dict) -> Dict[str, Any]:
        """
        Stage 1: Analyze keyword and determine article angle.
        
        Determines the best approach for covering the keyword based on:
        - Current trends and news
        - Search intent
        - Available data and sources
        - Potential perspectives to cover
        """
        keyword = article.keyword.keyword
        
        prompt = f"""Analyze this keyword for news article generation: "{keyword}"

Provide a comprehensive analysis including:

1. **News Angle**: What's the most newsworthy aspect of this topic right now?
2. **Target Audience**: Who would be most interested in this?
3. **Key Questions**: What are the 5 most important questions to answer?
4. **Data Points Needed**: What statistics, studies, or data should be included?
5. **Perspectives to Cover**: List different viewpoints on this topic (minimum 2)
6. **Potential Bias Risks**: What biases should we actively avoid?
7. **Fact-Check Priority**: What claims will require strong citations?

Format as JSON with these keys: angle, audience, questions, data_needed, perspectives, bias_risks, fact_check_priorities"""
        
        response = await self._invoke_llm(
            self.llm_primary,
            system="You are an expert news analyst helping to plan objective, data-driven news coverage.",
            prompt=prompt
        )
        
        # Parse response
        analysis = self._parse_json_response(response)
        
        return {
            'keyword_analysis': analysis,
            'recommended_template': self._determine_template(analysis)
        }
    
    async def _research(self, article, context: Dict) -> Dict[str, Any]:
        """
        Stage 2: Research and gather data from credible sources.
        
        Uses web search and news APIs to collect:
        - Recent news and developments
        - Statistical data
        - Expert opinions and quotes
        - Multiple perspectives
        """
        keyword = article.keyword.keyword
        analysis = context.get('keyword_analysis', {}).get('keyword_analysis', {})
        
        logger.info(f"Researching: {keyword}")
        
        # Initialize research agent
        research_agent = ResearchAgent()
        
        # Collect references from multiple sources
        research_data = research_agent.collect_references(keyword, max_sources=20)
        
        logger.info(f"Research complete: {research_data['source_count']} sources, "
                   f"avg credibility: {research_data['credibility_avg']:.1f}")
        
        return {
            'research_data': research_data,
            'source_count': research_data['source_count'],
            'statistics': research_data['statistics'],
            'quotes': research_data['quotes'],
            'perspectives': research_data['perspectives']
        }
    
    async def _create_outline(self, article, context: Dict) -> Dict[str, Any]:
        """
        Stage 3: Create structured article outline.
        
        Generates a detailed outline ensuring:
        - Logical flow
        - Balanced coverage of perspectives
        - Clear sections for data and analysis
        - Proper heading hierarchy
        """
        keyword = article.keyword.keyword
        analysis = context.get('keyword_analysis', {}).get('keyword_analysis', {})
        research = context.get('research', {}).get('research_data', {})
        
        prompt = f"""Create a detailed outline for an unbiased news analysis article about: "{keyword}"

Article Requirements:
- Target Word Count: {article.target_word_count} words
- Template: {article.template_type}
- Must present multiple perspectives objectively
- Must include data and statistics
- Must cite all factual claims

Research Summary: {research}

Analysis: {analysis}

Create an outline with:
1. Compelling headline (neutral, factual)
2. Lead paragraph (5W1H: Who, What, When, Where, Why, How)
3. 5-7 main sections with H2 headings
4. Subsections with H3 headings where needed
5. Notes on what data/sources to include in each section
6. Call-outs for different perspectives to present

Format as JSON with: headline, lead, sections (array of {{title, subsections, content_notes, data_points, perspectives}}))"""
        
        response = await self._invoke_llm(
            self.llm_primary,
            system="You are a news editor creating outlines for objective, data-driven articles.",
            prompt=prompt
        )
        
        outline = self._parse_json_response(response)
        
        return {
            'outline': outline,
            'section_count': len(outline.get('sections', []))
        }
    
    async def _generate_content(self, article, context: Dict) -> Dict[str, Any]:
        """
        Stage 4: Generate full article content.
        
        Creates comprehensive, objective article following outline and incorporating:
        - Research data and sources
        - Multiple perspectives
        - Neutral language
        - Proper citations
        """
        keyword = article.keyword.keyword
        outline = context.get('outline', {}).get('outline', {})
        research = context.get('research', {}).get('research_data', {})
        
        # Import prompts
        from .prompts.article_templates import SYSTEM_PROMPT, ARTICLE_GENERATION_PROMPT
        
        prompt = f"""Generate a comprehensive news article based on the following:

KEYWORD: {keyword}
WORD COUNT TARGET: {article.target_word_count}
TEMPLATE TYPE: {article.template_type}

OUTLINE:
{outline}

RESEARCH DATA:
{research}

FOCUS KEYWORDS: {article.focus_keywords or [keyword]}

Please generate a well-structured, objective news article following AI Analitica standards.
"""
        
        response = await self._invoke_llm(
            self.llm_primary,
            system=SYSTEM_PROMPT + " Return ONLY the article content in Markdown format without any preamble or code block markers.",
            prompt=prompt
        )
        
        # Parse content (which includes cleaning)
        content_data = self._parse_article_content(response)
        
        return {
            'title': content_data.get('title'),
            'content': content_data.get('content'),
            'word_count': self._count_words(content_data.get('content', '')),
            'references': content_data.get('references', [])
        }
    
    async def _humanize_content(self, article, context: Dict) -> Dict[str, Any]:
        """
        Stage 5: Make content more natural and readable while maintaining objectivity.
        
        Improves:
        - Sentence variety
        - Readability
        - Natural flow
        - Maintains all facts and citations
        - Preserves neutral tone
        """
        content = context.get('content_generation', {}).get('content', '')
        
        if not content:
            return {'humanized': False, 'content': content}
        
        prompt = f"""Refine this news analysis to be more readable and natural while MAINTAINING complete objectivity:

{content}

Improvements to make:
- Vary sentence structure for better flow
- Use clear transitions between ideas
- Simplify complex sentences where possible
- Maintain professional, neutral tone
- Keep all facts, data, and citations intact
- DO NOT add opinions or emotional language
- DO NOT lose any perspectives or viewpoints
- Keep the analytical, objective style

Return the improved article maintaining the same structure and all citations."""
        
        response = await self._invoke_llm(
            self.llm_primary,
            system="You are an editor improving readability while maintaining journalistic objectivity. Return ONLY the improved article content without any preamble, explanations, or code block markers.",
            prompt=prompt
        )
        
        # Clean unwanted preamble and code blocks
        cleaned_response = self._clean_llm_response(response)
        
        return {
            'content': cleaned_response,
            'humanized': True
        }
    
    async def _check_ai_detection(self, article, context: Dict) -> Dict[str, Any]:
        """
        Stage 6: Check if content appears AI-generated.
        
        Note: For AI Analitica, we embrace AI generation, but we want
        content to be readable and natural, not obviously robotic.
        """
        content = context.get('humanization', {}).get('content', '')
        
        # TODO: Integrate with GPTZero or Originality.AI API
        # Placeholder implementation
        
        ai_score = 45.0  # Simulated score (0-100, lower is more human-like)
        
        return {
            'ai_score': ai_score,
            'passed': ai_score < self.config['quality_thresholds']['max_ai_score'],
            'flagged_sections': []
        }
    
    async def _check_plagiarism(self, article, context: Dict) -> Dict[str, Any]:
        """
        Stage 7: Check for plagiarism.
        
        Critical for AI Analitica - all content must be original analysis.
        """
        content = context.get('humanization', {}).get('content', '')
        
        # TODO: Integrate with Copyscape or similar API
        # Placeholder implementation
        
        plagiarism_score = 2.5  # Simulated percentage
        
        return {
            'plagiarism_score': plagiarism_score,
            'passed': plagiarism_score < self.config['quality_thresholds']['max_plagiarism'],
            'matched_sources': []
        }
    
    async def _check_bias(self, article, context: Dict) -> Dict[str, Any]:
        """
        Stage 8: Detect political, emotional, or subjective bias.
        
        CRITICAL for AI Analitica mission - ensuring complete objectivity.
        Uses multiple AI models for cross-validation.
        """
        content = context.get('humanization', {}).get('content', '')
        
        # Primary bias check with GPT-4
        bias_prompt = f"""Analyze this news article for bias and objectivity:

{content}

Evaluate on these criteria (rate 0-100, where 0 is perfectly objective):

1. **Political Bias**: Does it favor any political viewpoint?
2. **Emotional Language**: Does it use emotionally charged words?
3. **One-Sided Presentation**: Does it present multiple perspectives fairly?
4. **Subjective Statements**: Are opinions presented as facts?
5. **Loaded Language**: Does it use terminology that implies judgment?

For each biased element found:
- Quote the exact phrase
- Explain the bias
- Suggest neutral alternative

Format as JSON with: overall_bias_score, political_bias, emotional_language, one_sided, subjective_statements, loaded_language, flagged_phrases (array), suggestions (array)"""
        
        primary_analysis = await self._invoke_llm(
            self.llm_primary,
            system="You are an expert at detecting bias in news content. Be thorough and critical.",
            prompt=bias_prompt
        )
        
        bias_data = self._parse_json_response(primary_analysis)
        
        # Cross-validate with Claude if available
        if self.llm_secondary:
            secondary_analysis = await self._invoke_llm(
                self.llm_secondary,
                system="You are checking news content for objectivity and bias. Flag any subjective language.",
                prompt=bias_prompt
            )
            secondary_data = self._parse_json_response(secondary_analysis)
            
            # Average the scores
            bias_score = (bias_data.get('overall_bias_score', 0) + secondary_data.get('overall_bias_score', 0)) / 2
        else:
            bias_score = bias_data.get('overall_bias_score', 0)
        
        return {
            'bias_score': bias_score,
            'passed': bias_score < self.config['quality_thresholds']['max_bias_score'],
            'analysis': bias_data,
            'flagged_phrases': bias_data.get('flagged_phrases', []),
            'suggestions': bias_data.get('suggestions', [])
        }
    
    async def _verify_facts(self, article, context: Dict) -> Dict[str, Any]:
        """
        Stage 9: Verify all factual claims have citations.
        
        Ensures every claim is backed by credible sources.
        """
        content = context.get('humanization', {}).get('content', '')
        
        prompt = f"""Analyze this article and identify all factual claims that need citations:

{content}

For each factual claim:
1. Extract the claim
2. Check if it has a citation
3. If no citation, flag it as "needs citation"
4. Rate confidence that this needs a source (0-100)

Format as JSON with: total_claims, cited_claims, uncited_claims (array of {{claim, needs_citation, confidence}}), citation_rate (percentage)"""
        
        response = await self._invoke_llm(
            self.llm_primary,
            system="You are a fact-checker ensuring all claims are properly cited.",
            prompt=prompt
        )
        
        fact_data = self._parse_json_response(response)
        
        citation_rate = fact_data.get('citation_rate', 0)
        
        return {
            'fact_check_score': citation_rate,
            'passed': citation_rate >= self.config['quality_thresholds']['min_fact_check'],
            'uncited_claims': fact_data.get('uncited_claims', []),
            'total_claims': fact_data.get('total_claims', 0)
        }
    
    async def _analyze_perspectives(self, article, context: Dict) -> Dict[str, Any]:
        """
        Stage 10: Ensure multiple perspectives are represented.
        
        Checks that complex issues are covered from different angles.
        """
        content = context.get('humanization', {}).get('content', '')
        keyword = article.keyword.keyword
        
        prompt = f"""Analyze this article about "{keyword}" for perspective diversity:

{content}

Identify:
1. What perspectives are currently represented?
2. What perspectives are missing?
3. Is coverage balanced between perspectives?
4. Are viewpoints presented fairly and neutrally?

Rate balance on 0-100 scale (100 = perfectly balanced).

Format as JSON with: perspectives_covered (array), perspectives_missing (array), balance_score, is_balanced (boolean), recommendations (array)"""
        
        response = await self._invoke_llm(
            self.llm_primary,
            system="You are analyzing news coverage for perspective diversity and balance.",
            prompt=prompt
        )
        
        perspective_data = self._parse_json_response(response)
        
        return {
            'perspectives_covered': perspective_data.get('perspectives_covered', []),
            'perspectives_missing': perspective_data.get('perspectives_missing', []),
            'balance_score': perspective_data.get('balance_score', 0),
            'passed': perspective_data.get('is_balanced', False),
            'recommendations': perspective_data.get('recommendations', [])
        }
    
    async def _optimize_seo(self, article, context: Dict) -> Dict[str, Any]:
        """
        Stage 11: Optimize for search engines.
        
        Improves discoverability while maintaining quality.
        """
        content = context.get('humanization', {}).get('content', '')
        keyword = article.keyword.keyword
        
        # TODO: Implement SEO optimization chain
        # Placeholder implementation
        
        seo_score = 82.0  # Simulated score
        
        return {
            'seo_score': seo_score,
            'passed': seo_score >= self.config['quality_thresholds']['min_seo_score'],
            'optimized_content': content,
            'recommendations': []
        }
    
    async def _generate_meta(self, article, context: Dict) -> Dict[str, Any]:
        """
        Stage 12: Generate SEO meta tags.
        
        Creates optimized meta title, description, and keywords.
        """
        title = context.get('content_generation', {}).get('title', '')
        content = context.get('seo_optimization', {}).get('optimized_content', '')
        keyword = article.keyword.keyword
        
        # TODO: Implement meta generation chain
        # Placeholder implementation
        
        return {
            'meta_title': title[:60],
            'meta_description': f"Objective analysis of {keyword}"[:160],
            'focus_keywords': [keyword],
            'og_title': title[:60],
            'og_description': f"Data-driven insights on {keyword}"[:160]
        }
    
    async def _generate_image(self, article, context: Dict) -> Dict[str, Any]:
        """
        Stage 13: Generate featured image with Google Imagen 3.
        
        Creates professional, news-appropriate imagery using Gemini's image generation.
        """
        title = context.get('content_generation', {}).get('title', '')
        keyword = article.keyword.keyword
        outline = context.get('outline', {}).get('outline', {})
        
        if not title:
            title = keyword
        
        # Create a detailed image prompt optimized for news articles
        prompt_template = f"""Create a professional, high-quality featured image for a news article about: {keyword}

Article Title: {title}

Style Requirements:
- Professional news/journalism aesthetic
- Modern, clean design
- Suitable for news website header
- No text or watermarks
- Photorealistic or clean illustration style
- Neutral and objective visual tone
- High resolution, landscape orientation (16:9)

The image should visually represent the main topic while maintaining a professional, credible news publication appearance."""

        try:
            # Use Google Generative AI for image generation
            if not self.config.get('gemini_api_key'):
                logger.warning("Gemini API key not configured, skipping image generation")
                return {
                    'image_generated': False,
                    'image_url': '',
                    'image_prompt': prompt_template,
                    'alt_text': title,
                    'error': 'No API key configured'
                }
            
            # Import Gemini image generation
            import google.generativeai as genai
            import requests
            import base64
            from io import BytesIO
            from PIL import Image as PILImage
            from django.core.files.base import ContentFile
            
            # Configure Gemini
            genai.configure(api_key=self.config['gemini_api_key'])
            
            # Use Imagen 3 model for image generation
            model = genai.GenerativeModel('imagen-3.0-generate-001')
            
            # Generate image
            logger.info(f"Generating image with prompt: {prompt_template[:100]}...")
            
            response = model.generate_images(
                prompt=prompt_template,
                number_of_images=1,
                safety_filter_level="block_some",
                person_generation="allow_adult",
                aspect_ratio="16:9",
            )
            
            # Get the first generated image
            if response.images:
                generated_image = response.images[0]
                
                # Save image to media directory
                image_filename = f"ai_article_{article.id}.png"
                image_path = f"ai_generated/{image_filename}"
                
                # Convert PIL Image to Django file
                img_buffer = BytesIO()
                generated_image._pil_image.save(img_buffer, format='PNG', quality=95)
                img_buffer.seek(0)
                
                # Save to article
                from asgiref.sync import sync_to_async
                
                @sync_to_async
                def save_image():
                    from news.ai_models import AIArticle
                    art = AIArticle.objects.get(id=article.id)
                    art.image.save(image_filename, ContentFile(img_buffer.read()), save=True)
                    return art.image.url
                
                image_url = await save_image()
                
                logger.info(f"✅ Image generated successfully: {image_url}")
                
                return {
                    'image_generated': True,
                    'image_url': image_url,
                    'image_local_path': image_path,
                    'image_prompt': prompt_template,
                    'alt_text': title,
                    'model': 'imagen-3.0'
                }
            else:
                logger.warning("No images generated from Imagen")
                return {
                    'image_generated': False,
                    'image_url': '',
                    'image_prompt': prompt_template,
                    'alt_text': title,
                    'error': 'No images returned from API'
                }
                
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            # Continue pipeline even if image generation fails
            return {
                'image_generated': False,
                'image_url': '',
                'image_prompt': prompt_template,
                'alt_text': title,
                'error': str(e)
            }
    
    async def _finalize(self, article, context: Dict) -> Dict[str, Any]:
        """
        Stage 14: Finalize article and save all data.
        
        Consolidates all pipeline outputs and calculates final scores.
        """
        # Gather all quality scores
        quality_scores = {
            'ai_score': context.get('ai_detection', {}).get('ai_score'),
            'plagiarism_score': context.get('plagiarism_check', {}).get('plagiarism_score'),
            'seo_score': context.get('seo_optimization', {}).get('seo_score'),
            'bias_score': context.get('bias_detection', {}).get('bias_score'),
            'fact_check_score': context.get('fact_verification', {}).get('fact_check_score'),
            'readability_score': 70.0,  # TODO: Calculate actual readability
        }
        
        # Save to article
        await self._save_article_data(article.id, context, quality_scores)
        
        return {
            'finalized': True,
            'quality_scores': quality_scores,
            'ready_for_review': all([
                quality_scores['bias_score'] < 20,
                quality_scores['plagiarism_score'] < 5,
                quality_scores['fact_check_score'] >= 80,
            ])
        }
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    async def _invoke_llm(self, llm, system: str, prompt: str) -> str:
        """Invoke language model with system and user prompts."""
        try:
            messages = [
                SystemMessage(content=system),
                HumanMessage(content=prompt)
            ]
            response = await llm.ainvoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"LLM invocation failed: {e}")
            raise
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from LLM response, handling markdown code blocks."""
        import json
        import re
        
        # Remove markdown code blocks if present
        response = re.sub(r'```json\s*|\s*```', '', response)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON response: {response[:200]}")
            return {}
    
    def _clean_llm_response(self, response: str) -> str:
        """Clean unwanted preamble and code blocks from LLM responses."""
        import re
        
        # Remove common LLM preamble patterns
        preamble_patterns = [
            r"^(?:Okay|Sure|Here's|Here is)[^:]*:?\s*",
            r"^I've\s+(?:revised|created|generated)[^:]*:?\s*",
            r"^This\s+(?:is|will be)[^:]*:?\s*",
            r"^Let me[^:]*:?\s*",
        ]
        
        cleaned = response
        for pattern in preamble_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE | re.MULTILINE)
        
        # Remove markdown code blocks (```html, ```markdown, etc.)
        cleaned = re.sub(r'^\s*```(?:html|markdown|md)?\s*\n', '', cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r'\n\s*```\s*$', '', cleaned, flags=re.MULTILINE)
        
        # Remove any remaining code block markers
        cleaned = re.sub(r'```\s*', '', cleaned)
        
        return cleaned.strip()
    
    def _parse_article_content(self, response: str) -> Dict[str, Any]:
        """Parse article content from LLM response and convert Markdown to HTML."""
        import markdown
        
        # Clean unwanted preamble first
        cleaned_response = self._clean_llm_response(response)
        
        # Convert Markdown to HTML with extensions for better formatting
        html_content = markdown.markdown(
            cleaned_response,
            extensions=[
                'markdown.extensions.extra',      # Tables, footnotes, etc.
                'markdown.extensions.nl2br',      # Convert newlines to <br>
                'markdown.extensions.sane_lists', # Better list handling
                'markdown.extensions.toc',        # Table of contents
            ]
        )
        
        return {
            'title': 'Generated Article Title',
            'content': html_content,
            'references': []
        }
    
    def _count_words(self, text: str) -> int:
        """Count words in text."""
        return len(text.split())
    
    def _determine_template(self, analysis: Dict) -> str:
        """Determine best article template based on analysis."""
        # Simple logic - can be enhanced
        angle = analysis.get('angle', '').lower()
        
        if 'breaking' in angle or 'urgent' in angle:
            return 'breaking_news'
        elif 'data' in angle or 'statistics' in angle:
            return 'data_driven'
        elif 'explain' in angle or 'understanding' in angle:
            return 'explainer'
        else:
            return 'analysis'
    
    # ========================================================================
    # Database Operations (Django Integration)
    # ========================================================================
    
    async def _load_article(self, article_id: str):
        """Load article from database."""
        # TODO: Implement async database access
        # For now, return mock object
        class MockArticle:
            id = article_id
            keyword = type('obj', (object,), {'keyword': 'AI in Healthcare'})()
            target_word_count = 1500
            template_type = 'analysis'
            focus_keywords = []
            retry_count = 0
        
        return MockArticle()
    
    async def _update_article_status(self, article_id: str, **kwargs):
        """Update article status in database."""
        from news.ai_models import AIArticle
        from asgiref.sync import sync_to_async
        
        logger.info(f"Updating article {article_id}: {kwargs}")
        
        @sync_to_async
        def update_db():
            article = AIArticle.objects.get(id=article_id)
            for key, value in kwargs.items():
                setattr(article, key, value)
            article.save()
        
        await update_db()
    
    async def _create_workflow_log(self, article_id: str, stage: str, status: str) -> str:
        """Create workflow log entry."""
        logger.info(f"Creating log for {article_id}, stage: {stage}, status: {status}")
        # Workflow logging simplified - just return a dummy ID
        return f"log-{article_id}-{stage}"
    
    async def _complete_workflow_log(self, log_id: str, output_data: Dict, duration: float):
        """Mark workflow log as completed."""
        logger.info(f"Completing log {log_id}, duration: {duration}s")
        # Simplified logging - just log to console
        pass
    
    async def _fail_workflow_log(self, log_id: str, error: str):
        """Mark workflow log as failed."""
        logger.error(f"Failing log {log_id}: {error}")
        # Simplified logging - just log to console
        pass
    
    async def _save_article_data(self, article_id: str, context: Dict, quality_scores: Dict):
        """Save final article data to database."""
        from news.ai_models import AIArticle
        from asgiref.sync import sync_to_async
        
        logger.info(f"Saving article data for {article_id}")
        
        @sync_to_async
        def save_data():
            article = AIArticle.objects.get(id=article_id)
            
            # Save content from final stages (use humanized content if available, otherwise raw)
            final_content = ''
            content_source = None
            
            if 'humanization' in context and context['humanization'].get('content'):
                final_content = context['humanization'].get('content', '')
                article.content_json = context['humanization']
                content_source = 'humanization'
            elif 'content_generation' in context:
                final_content = context['content_generation'].get('content', '')
                article.content_json = context['content_generation']
                content_source = 'content_generation'
            
            article.raw_content = final_content
            
            # Debug logging
            logger.info(f"Content saved from: {content_source}")
            logger.info(f"Content length: {len(final_content)} chars")
            logger.info(f"Content preview: {final_content[:200]}..." if final_content else "Content is EMPTY!")
            
            # Save outline
            if 'outline' in context:
                article.outline = context['outline'].get('outline', {})
            
            # Save SEO data
            if 'seo_optimization' in context:
                seo = context['seo_optimization']
                article.meta_title = seo.get('title', '')
                article.meta_description = seo.get('description', '')
                # Handle focus_keyword as single string or list
                focus_kw = seo.get('focus_keyword', '')
                if isinstance(focus_kw, str):
                    article.focus_keywords = [focus_kw] if focus_kw else []
                else:
                    article.focus_keywords = focus_kw
            
            # Save quality scores
            article.quality_metrics = quality_scores
            
            # Save image data if generated
            if 'image_generation' in context:
                img_data = context['image_generation']
                if img_data.get('image_generated') and img_data.get('image_url'):
                    article.image_url = img_data.get('image_url', '')
                    if img_data.get('image_local_path'):
                        article.image_local_path = img_data.get('image_local_path', '')
                    logger.info(f"Image saved: {article.image_url}")
            
            # Calculate word count from raw_content
            if article.raw_content:
                # Simple word count (remove HTML tags and count)
                import re
                text = re.sub(r'<[^>]+>', '', article.raw_content)
                article.actual_word_count = len(text.split())
            
            article.save()
        
        await save_data()
    
    # ========================================================================
    # Public Methods
    # ========================================================================
    
    async def retry_article(self, article_id: str, failed_stage: str) -> Dict[str, Any]:
        """
        Retry article generation from a specific stage.
        
        Args:
            article_id: UUID of the AIArticle to retry
            failed_stage: Stage name where failure occurred
            
        Returns:
            Dictionary with retry results
        """
        logger.info(f"Retrying article {article_id} from stage {failed_stage}")
        
        # Load article
        article = await self._load_article(article_id)
        
        # Find stage index
        stage_names = list(self.stages.keys())
        if failed_stage not in stage_names:
            raise ValueError(f"Invalid stage: {failed_stage}")
        
        start_index = stage_names.index(failed_stage)
        
        # Execute from failed stage onwards
        context = {}
        for stage_name in stage_names[start_index:]:
            logger.info(f"Executing stage: {stage_name}")
            stage_func = self.stages[stage_name]
            context = await stage_func(article_id, context)
        
        return context
    
    def get_pipeline_status(self, article_id: str) -> Dict[str, Any]:
        """Get current status of article in pipeline."""
        # TODO: Implement status tracking
        return {
            'article_id': article_id,
            'current_stage': 'unknown',
            'status': 'unknown',
            'progress_percentage': 0
        }