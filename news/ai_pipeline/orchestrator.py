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
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

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
        """Load default configuration from database or fallback to environment."""
        from news.ai_models import AIGenerationConfig
        
        try:
            # Try to get the default config from database
            default_config = AIGenerationConfig.objects.filter(
                is_default=True,
                enabled=True
            ).first()
            
            if default_config:
                logger.info(f"Loaded config from database: {default_config.name} ({default_config.ai_provider}/{default_config.model_name})")
                return {
                    'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
                    'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY', ''),
                    'gemini_api_key': os.getenv('GEMINI_API_KEY', ''),
                    'groq_api_key': os.getenv('GROQ_API_KEY', ''),
                    'naturalwrite_api_key': os.getenv('NATURALWRITE_API_KEY', ''),
                    'hf_api_key': os.getenv('HF_API_KEY', ''),
                    'default_provider': default_config.ai_provider,
                    'default_model': default_config.model_name,
                    'temperature': float(default_config.temperature),
                    'max_tokens': int(default_config.max_tokens),
                    'max_retries': int(default_config.max_retries),
                    'stage_configs': default_config.stage_configs or {},
                    'quality_thresholds': {
                        'max_ai_score': 50.0,
                        'max_plagiarism': 5.0,
                        'min_seo_score': 75.0,
                        'min_readability': 60.0,
                        'max_bias_score': 20.0,
                        'min_fact_check': 80.0,
                    }
                }
        except Exception as e:
            logger.warning(f"Failed to load config from database: {e}")
        
        # Fallback to environment/hardcoded defaults
        logger.info("Using fallback configuration")
        return {
            'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
            'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY', ''),
            'gemini_api_key': os.getenv('GEMINI_API_KEY', ''),
            'groq_api_key': os.getenv('GROQ_API_KEY', ''),
            'naturalwrite_api_key': os.getenv('NATURALWRITE_API_KEY', ''),
            'default_provider': 'google',
            'default_model': 'gemini-exp-1206',
            'temperature': 0.7,
            'max_tokens': 32000,
            'max_retries': 3,
            'stage_configs': {},
            'quality_thresholds': {
                'max_ai_score': 50.0,
                'max_plagiarism': 5.0,
                'min_seo_score': 75.0,
                'min_readability': 60.0,
                'max_bias_score': 20.0,
                'min_fact_check': 80.0,
            }
        }
    
    def _init_llms(self):
        """Initialize Language Model instances with automatic fallback."""
        primary_initialized = False
        provider = self.config.get('default_provider', 'google')
        
        # Try to initialize primary LLM with fallback logic
        try:
            if provider == 'google' and self.config.get('gemini_api_key'):
                try:
                    self.llm_primary = ChatGoogleGenerativeAI(
                        model=self.config['default_model'],
                        temperature=self.config['temperature'],
                        max_output_tokens=self.config['max_tokens'],
                        google_api_key=self.config['gemini_api_key']
                    )
                    logger.info(f"Primary LLM: Gemini ({self.config['default_model']})")
                    primary_initialized = True
                except Exception as gemini_error:
                    logger.error(f"Gemini initialization failed: {gemini_error}")
                    if "expired" in str(gemini_error).lower() or "invalid" in str(gemini_error).lower():
                        logger.warning("Gemini API key expired or invalid, falling back to Groq")
                    else:
                        logger.warning(f"Gemini error, falling back to Groq: {gemini_error}")
                        
            if not primary_initialized and self.config.get('groq_api_key'):
                # Fallback to Groq
                logger.info("Falling back to Groq API")
                self.llm_primary = ChatGroq(
                    model='llama-3.3-70b-versatile',
                    temperature=self.config['temperature'],
                    max_tokens=min(self.config['max_tokens'], 32000),
                    groq_api_key=self.config['groq_api_key']
                )
                logger.info(f"Primary LLM: Groq (llama-3.3-70b-versatile) [FALLBACK]")
                primary_initialized = True
                
            if not primary_initialized and provider == 'groq' and self.config.get('groq_api_key'):
                self.llm_primary = ChatGroq(
                    model=self.config['default_model'],
                    temperature=self.config['temperature'],
                    max_tokens=self.config['max_tokens'],
                    groq_api_key=self.config['groq_api_key']
                )
                logger.info(f"Primary LLM: Groq ({self.config['default_model']})")
                primary_initialized = True
                
            if not primary_initialized and provider == 'openai' and self.config.get('openai_api_key'):
                self.llm_primary = ChatOpenAI(
                    model=self.config.get('default_model', 'gpt-4-turbo-preview'),
                    temperature=self.config['temperature'],
                    max_tokens=self.config['max_tokens'],
                    openai_api_key=self.config['openai_api_key']
                )
                logger.info(f"Primary LLM: OpenAI ({self.config['default_model']})")
                primary_initialized = True
                
            if not primary_initialized and provider == 'anthropic' and self.config.get('anthropic_api_key'):
                self.llm_primary = ChatAnthropic(
                    model=self.config.get('default_model', 'claude-3-5-sonnet-20241022'),
                    temperature=self.config['temperature'],
                    anthropic_api_key=self.config['anthropic_api_key']
                )
                logger.info(f"Primary LLM: Claude ({self.config['default_model']})")
                primary_initialized = True
                
            if not primary_initialized:
                raise ValueError(f"Failed to initialize any LLM provider. Tried: {provider}")
            
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
    
    def _get_llm_for_stage(self, stage_name: str):
        """Get the appropriate LLM for a specific pipeline stage."""
        stage_config = self.config.get('stage_configs', {}).get(stage_name, {})
        
        if not stage_config:
            # Use default/primary LLM
            return self.llm_primary
        
        provider = stage_config.get('provider')
        model = stage_config.get('model')
        
        if not provider or not model:
            return self.llm_primary
        
        # Create stage-specific LLM instance
        try:
            if provider == 'google' and self.config.get('gemini_api_key'):
                from langchain_google_genai import ChatGoogleGenerativeAI
                return ChatGoogleGenerativeAI(
                    model=model,
                    temperature=self.config['temperature'],
                    max_output_tokens=self.config['max_tokens'],
                    google_api_key=self.config['gemini_api_key']
                )
            elif provider == 'groq' and self.config.get('groq_api_key'):
                from langchain_groq import ChatGroq
                return ChatGroq(
                    model=model,
                    temperature=self.config['temperature'],
                    max_tokens=self.config['max_tokens'],
                    groq_api_key=self.config['groq_api_key']
                )
            elif provider == 'openai' and self.config.get('openai_api_key'):
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(
                    model=model,
                    temperature=self.config['temperature'],
                    max_tokens=self.config['max_tokens'],
                    openai_api_key=self.config['openai_api_key']
                )
            elif provider == 'anthropic' and self.config.get('anthropic_api_key'):
                from langchain_anthropic import ChatAnthropic
                return ChatAnthropic(
                    model=model,
                    temperature=self.config['temperature'],
                    anthropic_api_key=self.config['anthropic_api_key']
                )
            else:
                logger.warning(f"Invalid provider '{provider}' for stage {stage_name}, using default")
                return self.llm_primary
        except Exception as e:
            logger.error(f"Failed to create LLM for stage {stage_name}: {e}")
            return self.llm_primary
    
    # ========================================================================
    # SEO Refinement Methods
    # ========================================================================
    
    def _load_seo_refinement_config(self) -> Dict[str, Any]:
        """Load SEO refinement configuration from JSON file."""
        import json
        from django.conf import settings
        
        config_path = os.path.join(settings.BASE_DIR, 'seo_refinement_config.json')
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    return config.get('seo_refinement', {})
            except Exception as e:
                logger.error(f"Failed to load SEO refinement config: {e}")
        
        # Return default configuration
        return {
            'enabled': True,
            'targetScore': 80,
            'maxRetries': 3,
            'refinementOptions': {
                'keywordDensity': {'enabled': True, 'targetRange': {'min': 0.5, 'max': 2.5}, 'priority': 'high'},
                'internalLinking': {'enabled': True, 'minLinks': 2, 'maxLinks': 5, 'priority': 'medium'},
                'metaDescription': {'enabled': True, 'minLength': 120, 'maxLength': 160, 'includeKeyword': True, 'priority': 'high'},
                'readability': {'enabled': True, 'targetScore': 60, 'maxSentenceLength': 25, 'maxParagraphLength': 150, 'priority': 'medium'},
                'titleOptimization': {'enabled': True, 'minLength': 30, 'maxLength': 60, 'includeKeyword': True, 'priority': 'high'},
                'contentStructure': {'enabled': True, 'minWordCount': 600, 'maxWordCount': 2500, 'headingDistribution': True, 'priority': 'low'}
            },
            'rewriteStages': {
                'contentGeneration': {'rewrite': True, 'includeSuggestions': True},
                'humanization': {'rewrite': True, 'includeSuggestions': True},
                'seoOptimization': {'rewrite': False, 'includeSuggestions': True}
            }
        }
    
    def _build_seo_refinement_prompt(self, seo_config: Dict, yoast_analysis: Dict, suggestions: Dict) -> str:
        """Build a detailed prompt with SEO refinement suggestions."""
        prompt_parts = [
            "IMPORTANT SEO REFINEMENT REQUIREMENTS:",
            "",
            "The article needs to be rewritten to meet these SEO standards:"
        ]
        
        # Add target score
        prompt_parts.append(f"\n✓ Target SEO Score: {seo_config.get('targetScore', 80)}/100")
        prompt_parts.append(f"  Current Score: {yoast_analysis.get('seo_score', 0)}/100")
        
        # Keyword density
        if seo_config.get('refinementOptions', {}).get('keywordDensity', {}).get('enabled'):
            kd_config = seo_config['refinementOptions']['keywordDensity']
            current_density = yoast_analysis.get('keyword_density', 0)
            target_range = kd_config.get('targetRange', {})
            
            prompt_parts.append(f"\n✓ Keyword Density [{kd_config.get('priority', 'medium').upper()} PRIORITY]:")
            prompt_parts.append(f"  Current: {current_density:.2f}%")
            prompt_parts.append(f"  Target: {target_range.get('min', 0.5)}% - {target_range.get('max', 2.5)}%")
            
            if current_density < target_range.get('min', 0.5):
                prompt_parts.append("  → Increase focus keyword usage naturally throughout the content")
            elif current_density > target_range.get('max', 2.5):
                prompt_parts.append("  → Reduce keyword usage to avoid keyword stuffing")
        
        # Readability
        if seo_config.get('refinementOptions', {}).get('readability', {}).get('enabled'):
            read_config = seo_config['refinementOptions']['readability']
            current_read = yoast_analysis.get('readability_score', 0)
            target_read = read_config.get('targetScore', 60)
            
            prompt_parts.append(f"\n✓ Readability [{read_config.get('priority', 'medium').upper()} PRIORITY]:")
            prompt_parts.append(f"  Current Score: {current_read}/100")
            prompt_parts.append(f"  Target Score: {target_read}/100")
            prompt_parts.append(f"  → Keep sentences under {read_config.get('maxSentenceLength', 25)} words")
            prompt_parts.append(f"  → Keep paragraphs under {read_config.get('maxParagraphLength', 150)} words")
        
        # Title optimization
        if seo_config.get('refinementOptions', {}).get('titleOptimization', {}).get('enabled'):
            title_config = seo_config['refinementOptions']['titleOptimization']
            prompt_parts.append(f"\n✓ Title Optimization [{title_config.get('priority', 'high').upper()} PRIORITY]:")
            prompt_parts.append(f"  → Length: {title_config.get('minLength', 30)}-{title_config.get('maxLength', 60)} characters")
            if title_config.get('includeKeyword'):
                prompt_parts.append("  → MUST include focus keyword in title")
        
        # Meta description
        if seo_config.get('refinementOptions', {}).get('metaDescription', {}).get('enabled'):
            meta_config = seo_config['refinementOptions']['metaDescription']
            prompt_parts.append(f"\n✓ Meta Description [{meta_config.get('priority', 'high').upper()} PRIORITY]:")
            prompt_parts.append(f"  → Length: {meta_config.get('minLength', 120)}-{meta_config.get('maxLength', 160)} characters")
            if meta_config.get('includeKeyword'):
                prompt_parts.append("  → MUST include focus keyword")
        
        # Content structure
        if seo_config.get('refinementOptions', {}).get('contentStructure', {}).get('enabled'):
            struct_config = seo_config['refinementOptions']['contentStructure']
            prompt_parts.append(f"\n✓ Content Structure [{struct_config.get('priority', 'low').upper()} PRIORITY]:")
            prompt_parts.append(f"  → Word count: {struct_config.get('minWordCount', 600)}-{struct_config.get('maxWordCount', 2500)} words")
            if struct_config.get('headingDistribution'):
                prompt_parts.append("  → Use proper heading distribution (H2, H3)")
        
        # Add YoastSEO issues
        if yoast_analysis.get('issues'):
            prompt_parts.append("\n✗ CRITICAL ISSUES TO FIX:")
            for issue in yoast_analysis['issues'][:5]:
                prompt_parts.append(f"  - {issue}")
        
        # Add improvements
        if yoast_analysis.get('improvements'):
            prompt_parts.append("\n⚠ IMPROVEMENTS NEEDED:")
            for improvement in yoast_analysis['improvements'][:5]:
                prompt_parts.append(f"  - {improvement}")
        
        # Add priority suggestions
        if suggestions.get('overall_priority'):
            prompt_parts.append("\n🔥 HIGH PRIORITY FIXES:")
            for priority in suggestions['overall_priority'][:5]:
                prompt_parts.append(f"  - {priority}")
        
        prompt_parts.append("\nRewrite the content to address ALL the above requirements while maintaining factual accuracy and objectivity.")
        
        return "\n".join(prompt_parts)
    
    async def _check_seo_refinement_needed(self, context: Dict) -> tuple[bool, str]:
        """
        Check if SEO refinement is needed based on current scores.
        
        Returns:
            Tuple of (needs_refinement: bool, reason: str)
        """
        seo_config = self._load_seo_refinement_config()
        
        if not seo_config.get('enabled', False):
            return False, "SEO refinement disabled"
        
        seo_data = context.get('seo_optimization', {})
        seo_score = seo_data.get('seo_score', 0)
        target_score = seo_config.get('targetScore', 80)
        
        if seo_score >= target_score:
            return False, f"SEO score ({seo_score}) meets target ({target_score})"
        
        return True, f"SEO score ({seo_score}) below target ({target_score})"
    
    async def _refine_article_for_seo(self, article, context: Dict, retry_attempt: int = 0) -> Dict[str, Any]:
        """
        Refine article to meet SEO standards by rewriting specified stages.
        
        Args:
            article: AIArticle instance
            context: Current pipeline context
            retry_attempt: Current retry attempt number
            
        Returns:
            Updated context with refined content
        """
        seo_config = self._load_seo_refinement_config()
        max_retries = seo_config.get('maxRetries', 3)
        
        if retry_attempt >= max_retries:
            logger.warning(f"Max SEO refinement retries ({max_retries}) reached")
            return context
        
        logger.info(f"Starting SEO refinement attempt {retry_attempt + 1}/{max_retries}")
        
        # Get YoastSEO analysis and suggestions
        seo_data = context.get('seo_optimization', {})
        yoast_analysis = seo_data.get('yoast_analysis', {})
        
        # Get optimization suggestions
        from .yoast_seo import get_yoast_service
        yoast = get_yoast_service()
        
        content = context.get('humanization', {}).get('content', '')
        title = context.get('content_generation', {}).get('title', '')
        keyword = context.get('keyword')
        
        suggestions = yoast.optimize_content(
            content=content,
            title=title,
            focus_keyword=keyword,
            analysis=yoast_analysis
        )
        
        # Build refinement prompt
        refinement_prompt = self._build_seo_refinement_prompt(seo_config, yoast_analysis, suggestions)
        
        # Determine which stages to rewrite
        rewrite_stages = seo_config.get('rewriteStages', {})
        
        # Rewrite content generation if configured
        if rewrite_stages.get('contentGeneration', {}).get('rewrite'):
            logger.info("Rewriting content generation stage with SEO refinement")
            
            # Create workflow log
            log_id = await self._create_workflow_log(
                str(article.id), 'content_generation_seo_refinement', 'started'
            )
            
            try:
                # Store original prompt enhancement if configured
                original_context = context.copy()
                
                if rewrite_stages['contentGeneration'].get('includeSuggestions'):
                    # Add SEO refinement prompt to the content generation
                    context['seo_refinement_prompt'] = refinement_prompt
                
                # Re-execute content generation
                result = await self._generate_content(article, context)
                context['content_generation'] = result
                
                await self._complete_workflow_log(log_id, result, 0)
                
            except Exception as e:
                logger.error(f"Content generation refinement failed: {e}")
                await self._fail_workflow_log(log_id, str(e))
                context = original_context
        
        # Rewrite humanization if configured
        if rewrite_stages.get('humanization', {}).get('rewrite'):
            logger.info("Rewriting humanization stage with SEO refinement")
            
            log_id = await self._create_workflow_log(
                str(article.id), 'humanization_seo_refinement', 'started'
            )
            
            try:
                if rewrite_stages['humanization'].get('includeSuggestions'):
                    context['seo_refinement_prompt'] = refinement_prompt
                
                result = await self._humanize_content(article, context)
                context['humanization'] = result
                
                await self._complete_workflow_log(log_id, result, 0)
                
            except Exception as e:
                logger.error(f"Humanization refinement failed: {e}")
                await self._fail_workflow_log(log_id, str(e))
        
        # Re-run SEO optimization to check if score improved
        logger.info("Re-analyzing SEO after refinement")
        seo_result = await self._optimize_seo(article, context)
        context['seo_optimization'] = seo_result
        
        new_score = seo_result.get('seo_score', 0)
        target_score = seo_config.get('targetScore', 80)
        
        logger.info(f"SEO score after refinement: {new_score}/100 (target: {target_score})")
        
        # Check if we need another iteration
        if new_score < target_score and retry_attempt + 1 < max_retries:
            logger.info(f"SEO score still below target, retrying refinement")
            return await self._refine_article_for_seo(article, context, retry_attempt + 1)
        
        return context
    
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
            # Load article from database (includes keyword via select_related)
            article = await self._load_article(article_id)
            
            # Extract all needed data from article to avoid async DB queries later
            article_data = await self._extract_article_data(article)
            
            # Update status
            await self._update_article_status(
                article_id,
                status='generating',
                workflow_stage=start_stage
            )
            
            # Execute pipeline stages sequentially
            context = {
                'article_id': article_id,
                'keyword': article_data['keyword'],
                'template_type': article_data['template_type'],
                'target_word_count': article_data['target_word_count'],
                'focus_keywords': article_data['focus_keywords'],
                'related_keywords': article_data['related_keywords'],
            }
            
            # Skip stages before start_stage
            stage_names = list(self.stages.keys())
            start_index = stage_names.index(start_stage) if start_stage in stage_names else 0
            
            for i, (stage_name, stage_func) in enumerate(self.stages.items()):
                # Skip stages before the start_stage
                if i < start_index:
                    logger.info(f"⏭️  [DEBUG] Skipping stage: {stage_name}")
                    continue
                    
                logger.info(f"🔄 [DEBUG] ========== Starting Stage: {stage_name.upper()} ==========")
                logger.info(f"🔄 [DEBUG] Article: {context.get('keyword')}")
                
                # Create workflow log entry
                log_id = await self._create_workflow_log(
                    article_id, stage_name, 'started'
                )
                
                try:
                    # Execute stage
                    stage_start = datetime.now()
                    logger.info(f"▶️  [DEBUG] Executing {stage_name}...")
                    
                    result = await stage_func(article, context)
                    stage_duration = (datetime.now() - stage_start).total_seconds()
                    
                    logger.info(f"✓ [DEBUG] {stage_name} completed in {stage_duration:.2f}s")
                    logger.info(f"✓ [DEBUG] Result keys: {list(result.keys()) if isinstance(result, dict) else 'non-dict'}")
                    
                    # Update context with stage results
                    context[stage_name] = result
                    
                    # Save intermediate data for critical stages and quality checks
                    save_stages = [
                        'research', 'outline', 'content_generation', 'humanization',
                        'ai_detection', 'plagiarism_check', 'bias_detection',
                        'fact_verification', 'seo_optimization', 'quality_check'
                    ]
                    if stage_name in save_stages:
                        logger.info(f"💾 [DEBUG] Saving intermediate data for {stage_name}...")
                        await self._save_intermediate_data(article_id, stage_name, result, context)
                    
                    # Log success
                    await self._complete_workflow_log(
                        log_id, result, stage_duration
                    )
                    
                    # Update article workflow stage
                    await self._update_article_status(
                        article_id,
                        workflow_stage=stage_name
                    )
                    
                    logger.info(f"✅ [DEBUG] Stage {stage_name} COMPLETE")
                    logger.info(f"✅ [DEBUG] ================================================\n")
                    
                    # Check for SEO refinement after SEO optimization stage
                    if stage_name == 'seo_optimization':
                        needs_refinement, reason = await self._check_seo_refinement_needed(context)
                        
                        if needs_refinement:
                            logger.info(f"SEO refinement needed: {reason}")
                            
                            # Create workflow log for refinement
                            refinement_log_id = await self._create_workflow_log(
                                article_id, 'seo_refinement', 'started'
                            )
                            
                            try:
                                # Perform SEO refinement
                                refinement_start = datetime.now()
                                context = await self._refine_article_for_seo(article, context)
                                refinement_duration = (datetime.now() - refinement_start).total_seconds()
                                
                                await self._complete_workflow_log(
                                    refinement_log_id, 
                                    {'refined': True, 'final_seo_score': context.get('seo_optimization', {}).get('seo_score', 0)},
                                    refinement_duration
                                )
                                
                                logger.info(f"SEO refinement completed in {refinement_duration:.2f}s")
                                
                            except Exception as e:
                                logger.error(f"SEO refinement failed: {e}")
                                await self._fail_workflow_log(refinement_log_id, str(e))
                                # Continue with pipeline even if refinement fails
                        else:
                            logger.info(f"SEO refinement skipped: {reason}")
                    
                except Exception as e:
                    import traceback
                    error_type = type(e).__name__
                    error_msg = str(e)
                    tb = traceback.format_exc()
                    
                    logger.error(f"❌ [DEBUG] ========== STAGE FAILED: {stage_name.upper()} ==========")
                    logger.error(f"❌ [DEBUG] Error Type: {error_type}")
                    logger.error(f"❌ [DEBUG] Error Message: {error_msg}")
                    logger.error(f"❌ [DEBUG] Traceback:\n{tb}")
                    logger.error(f"❌ [DEBUG] =====================================================")
                    
                    # Log failure
                    await self._fail_workflow_log(log_id, error_msg)
                    
                    # Update article as failed with detailed error
                    await self._update_article_status(
                        article_id,
                        status='failed',
                        workflow_stage=stage_name,
                    )
                    
                    # Save detailed error to database
                    try:
                        from news.ai_models import AIArticle
                        from asgiref.sync import sync_to_async
                        
                        @sync_to_async
                        def save_error():
                            article = AIArticle.objects.get(id=article_id)
                            article.last_error = f"{error_type} at {stage_name}: {error_msg}\n\nTraceback:\n{tb}"[:5000]
                            article.failed_stage = stage_name
                            
                            if not article.error_log:
                                article.error_log = []
                            article.error_log.append({
                                'timestamp': datetime.now().isoformat(),
                                'stage': stage_name,
                                'error_type': error_type,
                                'error_message': error_msg,
                                'traceback': tb[:2000]
                            })
                            article.save()
                        
                        await save_error()
                        logger.info(f"✓ [DEBUG] Error details saved to database")
                    except Exception as save_error:
                        logger.error(f"❌ [DEBUG] Failed to save error to database: {save_error}")
                    
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
        keyword = context.get('keyword')
        
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
        
        llm = self._get_llm_for_stage('keyword_analysis')
        
        response = await self._invoke_llm(
            llm,
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
        keyword = context.get('keyword')
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
        keyword = context.get('keyword')
        analysis = context.get('keyword_analysis', {}).get('keyword_analysis', {})
        research = context.get('research', {}).get('research_data', {})
        
        prompt = f"""Create a detailed outline for an unbiased news analysis article about: "{keyword}"

Article Requirements:
- Target Word Count: {context.get('target_word_count', 1500)} words
- Template: {context.get('template_type', 'analysis')}
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
        
        llm = self._get_llm_for_stage('outline')
        
        response = await self._invoke_llm(
            llm,
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
        keyword = context.get('keyword')
        outline = context.get('outline', {}).get('outline', {})
        research = context.get('research', {}).get('research_data', {})
        
        # Import prompts
        from .prompts.article_templates import SYSTEM_PROMPT, ARTICLE_GENERATION_PROMPT
        
        # Build base prompt
        prompt = f"""Generate a comprehensive news article based on the following:

KEYWORD: {keyword}
WORD COUNT TARGET: {context.get('target_word_count', 1500)}
TEMPLATE TYPE: {context.get('template_type', 'analysis')}

OUTLINE:
{outline}

RESEARCH DATA:
{research}

FOCUS KEYWORDS: {context.get('focus_keywords') or [keyword]}

Please generate a well-structured, objective news article following AI Analitica standards.
"""
        
        # Add SEO refinement requirements if available
        if context.get('seo_refinement_prompt'):
            prompt += f"\n\n{context['seo_refinement_prompt']}"
            logger.info("Including SEO refinement requirements in content generation")
        
        llm = self._get_llm_for_stage('content_generation')
        
        response = await self._invoke_llm(
            llm,
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
        
        Uses NaturalWrite API if configured, otherwise falls back to LLM humanization.
        
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
        
        # Check if NaturalWrite API is configured
        naturalwrite_key = self.config.get('naturalwrite_api_key')
        
        if naturalwrite_key:
            try:
                import requests
                
                logger.info("Using NaturalWrite API for humanization")
                
                # NaturalWrite API endpoint
                url = "https://api.naturalwrite.com/v1/humanize"
                
                headers = {
                    "Authorization": f"Bearer {naturalwrite_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "text": content,
                    "mode": "enhanced",  # Options: standard, enhanced, creative
                    "preserve_formatting": True,
                    "preserve_links": True
                }
                
                response = requests.post(url, json=payload, headers=headers, timeout=60)
                response.raise_for_status()
                
                result = response.json()
                humanized_content = result.get('humanized_text', content)
                
                logger.info(f"NaturalWrite humanization successful: {len(humanized_content)} chars")
                
                return {
                    'content': humanized_content,
                    'humanized': True,
                    'method': 'naturalwrite',
                    'ai_score_before': result.get('ai_score_before'),
                    'ai_score_after': result.get('ai_score_after')
                }
            except Exception as e:
                logger.error(f"NaturalWrite API failed: {e}, falling back to LLM humanization")
        
        # Fallback to LLM-based humanization
        logger.info("Using LLM for humanization")
        
        # Build base prompt
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
        
        # Add SEO refinement requirements if available
        if context.get('seo_refinement_prompt'):
            prompt += f"\n\n{context['seo_refinement_prompt']}"
            logger.info("Including SEO refinement requirements in humanization")
        
        llm = self._get_llm_for_stage('humanization')
        
        response = await self._invoke_llm(
            llm,
            system="You are an editor improving readability while maintaining journalistic objectivity. Return ONLY the improved article content without any preamble, explanations, or code block markers.",
            prompt=prompt
        )
        
        # Clean unwanted preamble and code blocks
        cleaned_response = self._clean_llm_response(response)
        
        return {
            'content': cleaned_response,
            'humanized': True,
            'method': 'llm'
        }
    
    async def _check_ai_detection(self, article, context: Dict) -> Dict[str, Any]:
        """
        Stage 6: Check if content appears AI-generated.
        
        Uses NaturalWrite API for detection if available.
        For AI Analitica, we embrace AI generation, but we want
        content to be readable and natural, not obviously robotic.
        """
        content = context.get('humanization', {}).get('content', '')
        
        if not content:
            return {'ai_score': 0, 'detected': False, 'bypassed': False}
        
        # Check if NaturalWrite API is configured
        naturalwrite_key = self.config.get('naturalwrite_api_key')
        
        if naturalwrite_key:
            try:
                import requests
                
                logger.info("Using NaturalWrite API for AI detection")
                
                url = "https://api.naturalwrite.com/v1/detect"
                
                headers = {
                    "Authorization": f"Bearer {naturalwrite_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "text": content
                }
                
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                ai_score = result.get('ai_probability', 0) * 100  # Convert to percentage
                
                logger.info(f"NaturalWrite AI detection: {ai_score:.2f}% AI-generated")
                
                return {
                    'ai_score': ai_score,
                    'detected': ai_score > self.config['quality_thresholds']['max_ai_score'],
                    'bypassed': ai_score <= 30.0,  # Good threshold for "human-like"
                    'method': 'naturalwrite',
                    'details': result.get('details', {})
                }
            except Exception as e:
                logger.error(f"NaturalWrite detection failed: {e}, skipping AI detection")
        
        # Fallback: Skip detection or use simple heuristic
        logger.info("Skipping AI detection (no API available)")
        return {
            'ai_score': 0,
            'detected': False,
            'bypassed': True,
            'method': 'skipped'
        }
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
        Stage 7: Check for plagiarism using Codequiry API.
        
        Critical for educational content - all content must be original.
        Automatically rewrites plagiarized sections if threshold exceeded.
        """
        from .plagiarism_checker import get_plagiarism_checker
        from .prompts.plagiarism_prompts import (
            PLAGIARISM_REWRITE_PROMPT,
            PLAGIARISM_SECTION_REWRITE_PROMPT
        )
        
        content = context.get('humanization', {}).get('content', '')
        title = context.get('content_generation', {}).get('title', context.get('keyword'))
        
        # Load plagiarism configuration
        plagiarism_config = self._load_plagiarism_config()
        
        if not plagiarism_config.get('enabled', True):
            logger.info("Plagiarism check disabled")
            return {
                'plagiarism_score': 0.0,
                'passed': True,
                'checked': False,
                'message': 'Plagiarism check disabled in configuration'
            }
        
        # Get plagiarism checker
        checker = get_plagiarism_checker()
        threshold = plagiarism_config.get('threshold', 5.0)
        check_web = plagiarism_config.get('checkOptions', {}).get('checkWeb', {}).get('enabled', True)
        check_database = plagiarism_config.get('checkOptions', {}).get('checkDatabase', {}).get('enabled', True)
        
        # Perform plagiarism check
        logger.info(f"Checking plagiarism with threshold {threshold}%")
        result = checker.check_plagiarism(
            content=content,
            title=title,
            threshold=threshold,
            check_web=check_web,
            check_database=check_database
        )
        
        # Handle check error
        if result.error:
            logger.error(f"Plagiarism check error: {result.error}")
            return {
                'plagiarism_score': 0.0,
                'passed': True,
                'checked': False,
                'error': result.error
            }
        
        # Log plagiarism result
        logger.info(
            f"Plagiarism check complete: {result.overall_score:.2f}% "
            f"(threshold: {threshold}%, sources: {result.sources_found})"
        )
        
        # If plagiarism is below threshold, pass
        if not result.is_plagiarized:
            return {
                'plagiarism_score': result.overall_score,
                'passed': True,
                'checked': True,
                'sources_found': result.sources_found,
                'report_url': result.report_url
            }
        
        # Plagiarism detected - check if auto-rewrite is enabled
        auto_rewrite = plagiarism_config.get('checkOptions', {}).get('autoRewrite', {}).get('enabled', True)
        
        if not auto_rewrite:
            logger.warning(f"Plagiarism detected ({result.overall_score}%) but auto-rewrite disabled")
            return {
                'plagiarism_score': result.overall_score,
                'passed': False,
                'checked': True,
                'sources_found': result.sources_found,
                'matches': result.matches,
                'report_url': result.report_url,
                'message': 'Plagiarism detected but auto-rewrite disabled'
            }
        
        # Attempt to rewrite plagiarized content
        max_retries = plagiarism_config.get('maxRetries', 3)
        rewrite_strategy = plagiarism_config.get('rewriteStrategy', {})
        
        for attempt in range(max_retries):
            logger.info(f"Plagiarism rewrite attempt {attempt + 1}/{max_retries}")
            
            try:
                # Determine rewrite strategy
                rewrite_sections = rewrite_strategy.get('rewriteSections', {}).get('enabled', True)
                rewrite_entire = rewrite_strategy.get('rewriteEntireArticle', {}).get('enabled', False)
                
                if rewrite_entire:
                    # Rewrite entire article
                    rewritten_content = await self._rewrite_entire_article_for_plagiarism(
                        article, context, result, plagiarism_config
                    )
                elif rewrite_sections:
                    # Rewrite only plagiarized sections
                    rewritten_content = await self._rewrite_plagiarized_sections(
                        article, context, result, plagiarism_config
                    )
                else:
                    logger.error("No rewrite strategy enabled")
                    break
                
                # Re-check plagiarism on rewritten content
                logger.info("Re-checking plagiarism after rewrite")
                recheck_result = checker.check_plagiarism(
                    content=rewritten_content,
                    title=title,
                    threshold=threshold,
                    check_web=check_web,
                    check_database=check_database
                )
                
                if recheck_result.error:
                    logger.error(f"Plagiarism recheck error: {recheck_result.error}")
                    break
                
                logger.info(
                    f"Plagiarism recheck: {recheck_result.overall_score:.2f}% "
                    f"(was {result.overall_score:.2f}%)"
                )
                
                # If rewrite successful, update context and return
                if not recheck_result.is_plagiarized:
                    context['humanization']['content'] = rewritten_content
                    context['plagiarism_rewrite'] = {
                        'original_score': result.overall_score,
                        'final_score': recheck_result.overall_score,
                        'attempts': attempt + 1,
                        'strategy': 'entire_article' if rewrite_entire else 'sections'
                    }
                    
                    logger.info(f"Plagiarism resolved after {attempt + 1} attempt(s)")
                    return {
                        'plagiarism_score': recheck_result.overall_score,
                        'passed': True,
                        'checked': True,
                        'rewritten': True,
                        'original_score': result.overall_score,
                        'rewrite_attempts': attempt + 1,
                        'sources_found': recheck_result.sources_found
                    }
                
                # Update result for next attempt
                result = recheck_result
                
            except Exception as e:
                logger.error(f"Plagiarism rewrite attempt {attempt + 1} failed: {str(e)}")
                continue
        
        # Max retries reached without success
        logger.error(f"Failed to resolve plagiarism after {max_retries} attempts")
        return {
            'plagiarism_score': result.overall_score,
            'passed': False,
            'checked': True,
            'rewritten': True,
            'rewrite_failed': True,
            'rewrite_attempts': max_retries,
            'sources_found': result.sources_found,
            'matches': result.matches,
            'report_url': result.report_url
        }
    
    def _load_plagiarism_config(self) -> Dict:
        """Load plagiarism check configuration"""
        import json
        import os
        from django.conf import settings
        
        config_path = os.path.join(settings.BASE_DIR, 'plagiarism_config.json')
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config.get('plagiarism_check', {})
        
        # Default configuration
        return {
            'enabled': True,
            'threshold': 5.0,
            'maxRetries': 3,
            'checkOptions': {
                'checkWeb': {'enabled': True},
                'checkDatabase': {'enabled': True},
                'autoRewrite': {'enabled': True}
            },
            'rewriteStrategy': {
                'rewriteSections': {'enabled': True},
                'rewriteEntireArticle': {'enabled': False},
                'maintainSEO': {'enabled': True},
                'maintainNepalContext': {'enabled': True}
            }
        }
    
    async def _rewrite_plagiarized_sections(
        self,
        article,
        context: Dict,
        plagiarism_result,
        config: Dict
    ) -> str:
        """
        Rewrite specific plagiarized sections while maintaining overall content.
        
        Args:
            article: AIArticle instance
            context: Pipeline context
            plagiarism_result: PlagiarismResult with matches
            config: Plagiarism configuration
            
        Returns:
            Rewritten content with original sections replaced
        """
        from .prompts.plagiarism_prompts import PLAGIARISM_REWRITE_PROMPT
        
        content = context.get('humanization', {}).get('content', '')
        keyword = context.get('keyword')
        
        # Extract plagiarized sections info
        from .plagiarism_checker import get_plagiarism_checker
        checker = get_plagiarism_checker()
        plagiarized_sections = checker.get_plagiarized_sections(plagiarism_result.matches)
        
        # Build plagiarized sections summary
        sections_text = "\n\n".join([
            f"SECTION {i+1}:\n"
            f"Text: {section['text']}\n"
            f"Source: {section['source']}\n"
            f"Similarity: {section['similarity']}%"
            for i, section in enumerate(plagiarized_sections[:5])  # Limit to top 5
        ])
        
        # Prepare rewrite prompt
        prompt_vars = {
            'content': content,
            'plagiarism_score': plagiarism_result.overall_score,
            'threshold': plagiarism_result.threshold,
            'sources_found': plagiarism_result.sources_found,
            'plagiarized_sections': sections_text or "See plagiarism report for details",
            'primary_keyword': keyword,
            'secondary_keywords': ', '.join(context.get('related_keywords', []) or []),
        }
        
        # Generate rewritten content
        rewrite_prompt = PLAGIARISM_REWRITE_PROMPT.format_messages(**prompt_vars)
        
        response = await self._invoke_llm(
            self.llm_primary,
            system=rewrite_prompt[0].content,
            prompt=rewrite_prompt[1].content
        )
        
        # Parse response
        rewrite_data = self._parse_json_response(response)
        rewritten_content = rewrite_data.get('rewritten_content', content)
        
        logger.info(f"Rewrote {len(plagiarized_sections)} plagiarized sections")
        return rewritten_content
    
    async def _rewrite_entire_article_for_plagiarism(
        self,
        article,
        context: Dict,
        plagiarism_result,
        config: Dict
    ) -> str:
        """
        Rewrite entire article to ensure complete originality.
        
        Args:
            article: AIArticle instance
            context: Pipeline context
            plagiarism_result: PlagiarismResult
            config: Plagiarism configuration
            
        Returns:
            Completely rewritten original content
        """
        from .prompts.plagiarism_prompts import PLAGIARISM_FULL_ARTICLE_REWRITE_PROMPT
        
        content = context.get('humanization', {}).get('content', '')
        title = context.get('content_generation', {}).get('title', '')
        keyword = context.get('keyword')
        
        # Prepare rewrite prompt
        prompt_vars = {
            'content': content,
            'plagiarism_score': plagiarism_result.overall_score,
            'threshold': plagiarism_result.threshold,
            'sources_found': plagiarism_result.sources_found,
            'title': title,
            'primary_keyword': keyword,
            'secondary_keywords': ', '.join(context.get('related_keywords', []) or []),
            'word_count': len(content.split())
        }
        
        # Generate completely rewritten content
        rewrite_prompt = PLAGIARISM_FULL_ARTICLE_REWRITE_PROMPT.format_messages(**prompt_vars)
        
        response = await self._invoke_llm(
            self.llm_primary,
            system=rewrite_prompt[0].content,
            prompt=rewrite_prompt[1].content
        )
        
        # Parse response
        rewrite_data = self._parse_json_response(response)
        rewritten_content = rewrite_data.get('content', content)
        
        # Update title if provided
        if rewrite_data.get('title'):
            context['content_generation']['title'] = rewrite_data['title']
        
        # Update meta description if provided
        if rewrite_data.get('meta_description'):
            context['meta_generation']['meta_description'] = rewrite_data['meta_description']
        
        logger.info("Rewrote entire article for plagiarism elimination")
        return rewritten_content
    
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
        keyword = context.get('keyword')
        
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
        Stage 11: Optimize for search engines using YoastSEO.
        
        Analyzes content with self-hosted YoastSEO for:
        - SEO Score
        - Keyword Density
        - Readability
        - Meta tags optimization
        """
        from .yoast_seo import get_yoast_service
        
        content = context.get('humanization', {}).get('content', '')
        title = context.get('content_generation', {}).get('title', '')
        keyword = context.get('keyword')
        meta_description = context.get('meta_generation', {}).get('meta_description', '')
        
        # Get YoastSEO service
        yoast = get_yoast_service()
        
        # Analyze content with YoastSEO
        analysis = yoast.analyze_content(
            content=content,
            title=title,
            focus_keyword=keyword,
            meta_description=meta_description
        )
        
        # Get optimization suggestions
        suggestions = yoast.optimize_content(
            content=content,
            title=title,
            focus_keyword=keyword,
            analysis=analysis
        )
        
        # Calculate final SEO score
        seo_score = analysis.get('seo_score', 70)
        readability_score = analysis.get('readability_score', 70)
        
        # Combine recommendations
        recommendations = []
        recommendations.extend(suggestions.get('title_suggestions', []))
        recommendations.extend(suggestions.get('content_suggestions', []))
        recommendations.extend(suggestions.get('meta_suggestions', []))
        
        return {
            'seo_score': seo_score,
            'readability_score': readability_score,
            'keyword_density': analysis.get('keyword_density', 0),
            'keyword_in_title': analysis.get('keyword_in_title', False),
            'keyword_in_description': analysis.get('keyword_in_description', False),
            'passed': seo_score >= self.config['quality_thresholds']['min_seo_score'],
            'optimized_content': content,
            'recommendations': recommendations,
            'priority_issues': suggestions.get('overall_priority', []),
            'yoast_analysis': analysis,
            'using_fallback': analysis.get('fallback_mode', False)
        }
    
    async def _generate_meta(self, article, context: Dict) -> Dict[str, Any]:
        """
        Stage 12: Generate SEO meta tags.
        
        Creates optimized meta title, description, and keywords.
        """
        title = context.get('content_generation', {}).get('title', '')
        content = context.get('seo_optimization', {}).get('optimized_content', '')
        keyword = context.get('keyword')
        
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
        Stage 13: Generate featured image for article.
        
        Supports multiple providers: Google (Imagen), Hugging Face (FLUX, SDXL, etc.), OpenAI (DALL-E)
        """
        title = context.get('content_generation', {}).get('title', '')
        keyword = context.get('keyword')
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

        # Get image generation stage config
        stage_config = self.config.get('stage_configs', {}).get('image_generation', {})
        provider = stage_config.get('provider', 'google')  # Default to Google
        model = stage_config.get('model', 'imagen-3.0-generate-001')
        
        logger.info(f"Image generation using: {provider} / {model}")

        try:
            from io import BytesIO
            from PIL import Image as PILImage
            from django.core.files.base import ContentFile
            from asgiref.sync import sync_to_async
            
            if provider == 'huggingface':
                # ========== HUGGING FACE IMAGE GENERATION ==========
                hf_api_key = self.config.get('hf_api_key')
                
                if not hf_api_key:
                    logger.warning("Hugging Face API key not configured")
                    return {
                        'image_generated': False,
                        'image_url': '',
                        'image_prompt': prompt_template,
                        'alt_text': title,
                        'error': 'No HF API key configured'
                    }
                
                import requests
                
                logger.info(f"Generating image with Hugging Face model: {model}")
                
                # Hugging Face Inference API
                api_url = f"https://api-inference.huggingface.co/models/{model}"
                headers = {"Authorization": f"Bearer {hf_api_key}"}
                
                # Simplified prompt for better results
                simple_prompt = f"{title}. {keyword}"
                
                response = requests.post(
                    api_url,
                    headers=headers,
                    json={"inputs": simple_prompt},
                    timeout=60
                )
                
                if response.status_code == 200:
                    # Load image from response
                    img_buffer = BytesIO(response.content)
                    pil_image = PILImage.open(img_buffer)
                    
                    # Resize to 16:9 if needed
                    target_width = 1920
                    target_height = 1080
                    pil_image = pil_image.resize((target_width, target_height), PILImage.Resampling.LANCZOS)
                    
                    # Save to Django file
                    image_filename = f"ai_article_{article.id}.png"
                    final_buffer = BytesIO()
                    pil_image.save(final_buffer, format='PNG', quality=95)
                    final_buffer.seek(0)
                    
                    @sync_to_async
                    def save_image():
                        from news.ai_models import AIArticle
                        art = AIArticle.objects.get(id=article.id)
                        art.image.save(image_filename, ContentFile(final_buffer.read()), save=True)
                        return art.image.url
                    
                    image_url = await save_image()
                    
                    logger.info(f"✅ Image generated successfully with Hugging Face: {image_url}")
                    
                    return {
                        'image_generated': True,
                        'image_url': image_url,
                        'image_prompt': prompt_template,
                        'alt_text': title,
                        'provider': 'huggingface',
                        'model': model
                    }
                else:
                    error_msg = response.text
                    logger.error(f"Hugging Face API error: {response.status_code} - {error_msg}")
                    return {
                        'image_generated': False,
                        'image_url': '',
                        'image_prompt': prompt_template,
                        'alt_text': title,
                        'error': f"HF API error: {error_msg[:100]}"
                    }
            
            elif provider == 'google':
                # ========== GOOGLE IMAGEN GENERATION ==========
                gemini_api_key = self.config.get('gemini_api_key')
                
                if not gemini_api_key:
                    logger.warning("Gemini API key not configured")
                    return {
                        'image_generated': False,
                        'image_url': '',
                        'image_prompt': prompt_template,
                        'alt_text': title,
                        'error': 'No Gemini API key configured'
                    }
                
                import google.generativeai as genai
                
                # Configure Gemini
                genai.configure(api_key=gemini_api_key)
                
                # Use specified Imagen model
                imagen_model = genai.GenerativeModel(model)
                
                logger.info(f"Generating image with Google Imagen: {model}")
                
                response = imagen_model.generate_images(
                    prompt=prompt_template,
                    number_of_images=1,
                    safety_filter_level="block_some",
                    person_generation="allow_adult",
                    aspect_ratio="16:9",
                )
                
                if response.images:
                    generated_image = response.images[0]
                    
                    # Save image
                    image_filename = f"ai_article_{article.id}.png"
                    image_path = f"ai_generated/{image_filename}"
                    img_buffer = BytesIO()
                    generated_image._pil_image.save(img_buffer, format='PNG', quality=95)
                    img_buffer.seek(0)
                    
                    @sync_to_async
                    def save_image():
                        from news.ai_models import AIArticle
                        art = AIArticle.objects.get(id=article.id)
                        art.image.save(image_filename, ContentFile(img_buffer.read()), save=True)
                        return art.image.url
                    
                    image_url = await save_image()
                    
                    logger.info(f"✅ Image generated successfully with Google Imagen: {image_url}")
                    
                    return {
                        'image_generated': True,
                        'image_url': image_url,
                        'image_local_path': image_path,
                        'image_prompt': prompt_template,
                        'alt_text': title,
                        'provider': 'google',
                        'model': model
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
            
            elif provider == 'openai':
                # ========== OPENAI DALL-E GENERATION ==========
                openai_api_key = self.config.get('openai_api_key')
                
                if not openai_api_key:
                    logger.warning("OpenAI API key not configured")
                    return {
                        'image_generated': False,
                        'image_url': '',
                        'image_prompt': prompt_template,
                        'alt_text': title,
                        'error': 'No OpenAI API key configured'
                    }
                
                import requests
                
                logger.info(f"Generating image with OpenAI DALL-E: {model}")
                
                api_url = "https://api.openai.com/v1/images/generations"
                headers = {
                    "Authorization": f"Bearer {openai_api_key}",
                    "Content-Type": "application/json"
                }
                
                # DALL-E 3 parameters
                payload = {
                    "model": model,
                    "prompt": prompt_template[:1000],  # DALL-E has prompt limits
                    "n": 1,
                    "size": "1792x1024",  # Closest to 16:9
                    "quality": "hd" if "dall-e-3" in model else "standard",
                    "style": "natural"
                }
                
                response = requests.post(api_url, headers=headers, json=payload, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    image_url_remote = result['data'][0]['url']
                    
                    # Download and save image
                    img_response = requests.get(image_url_remote)
                    img_buffer = BytesIO(img_response.content)
                    pil_image = PILImage.open(img_buffer)
                    
                    image_filename = f"ai_article_{article.id}.png"
                    final_buffer = BytesIO()
                    pil_image.save(final_buffer, format='PNG', quality=95)
                    final_buffer.seek(0)
                    
                    @sync_to_async
                    def save_image():
                        from news.ai_models import AIArticle
                        art = AIArticle.objects.get(id=article.id)
                        art.image.save(image_filename, ContentFile(final_buffer.read()), save=True)
                        return art.image.url
                    
                    image_url = await save_image()
                    
                    logger.info(f"✅ Image generated successfully with DALL-E: {image_url}")
                    
                    return {
                        'image_generated': True,
                        'image_url': image_url,
                        'image_prompt': prompt_template,
                        'alt_text': title,
                        'provider': 'openai',
                        'model': model
                    }
                else:
                    error_msg = response.text
                    logger.error(f"OpenAI API error: {response.status_code} - {error_msg}")
                    return {
                        'image_generated': False,
                        'image_url': '',
                        'image_prompt': prompt_template,
                        'alt_text': title,
                        'error': f"OpenAI API error: {error_msg[:100]}"
                    }
            
            else:
                logger.error(f"Unsupported image provider: {provider}")
                return {
                    'image_generated': False,
                    'image_url': '',
                    'image_prompt': prompt_template,
                    'alt_text': title,
                    'error': f'Unsupported provider: {provider}'
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
        # Gather all quality scores from context
        quality_scores = {}
        
        # AI Detection score
        if 'ai_detection' in context:
            ai_score = context['ai_detection'].get('ai_score')
            if ai_score is not None:
                quality_scores['ai_score'] = ai_score
        
        # Plagiarism score
        if 'plagiarism_check' in context:
            plag_score = context['plagiarism_check'].get('plagiarism_percentage') or context['plagiarism_check'].get('plagiarism_score')
            if plag_score is not None:
                quality_scores['plagiarism_score'] = plag_score
        
        # SEO score
        if 'seo_optimization' in context:
            seo_score = context['seo_optimization'].get('seo_score')
            if seo_score is not None:
                quality_scores['seo_score'] = seo_score
        
        # Bias score
        if 'bias_detection' in context:
            bias_score = context['bias_detection'].get('bias_score')
            if bias_score is not None:
                quality_scores['bias_score'] = bias_score
        
        # Fact check score
        if 'fact_verification' in context:
            fact_score = context['fact_verification'].get('fact_score') or context['fact_verification'].get('accuracy_score')
            if fact_score is not None:
                quality_scores['fact_check_score'] = fact_score
        
        # Calculate readability score (simple heuristic based on word count and content length)
        content = context.get('humanization', {}).get('content') or context.get('content_generation', {}).get('content', '')
        if content:
            import re
            # Remove markdown/HTML
            text = re.sub(r'[#*_\[\]()>`]', '', content)
            text = re.sub(r'<[^>]+>', '', text)
            
            words = text.split()
            sentences = re.split(r'[.!?]+', text)
            sentences = [s for s in sentences if s.strip()]
            
            if words and sentences:
                avg_sentence_length = len(words) / len(sentences)
                # Readability score: 100 - (penalty for long sentences)
                # Target: 15-20 words per sentence = good (score ~70-80)
                if avg_sentence_length <= 20:
                    readability = min(100, 70 + (20 - avg_sentence_length))
                else:
                    readability = max(30, 70 - (avg_sentence_length - 20) * 2)
                quality_scores['readability_score'] = readability
            else:
                quality_scores['readability_score'] = 50.0
        else:
            quality_scores['readability_score'] = 50.0
        
        logger.info(f"Final quality scores: {quality_scores}")
        
        # Save to article
        await self._save_article_data(article.id, context, quality_scores)
        
        return {
            'finalized': True,
            'quality_scores': quality_scores,
            'ready_for_review': True
        }
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    async def _invoke_llm(self, llm, system: str, prompt: str, retry_count: int = 0) -> str:
        """Invoke language model with system and user prompts, with automatic fallback."""
        max_retries = 2
        
        try:
            messages = [
                SystemMessage(content=system),
                HumanMessage(content=prompt)
            ]
            response = await llm.ainvoke(messages)
            return response.content
            
        except Exception as e:
            error_str = str(e).lower()
            
            # Check if it's an API key/quota issue
            if any(keyword in error_str for keyword in ['expired', 'invalid', 'quota', 'rate limit', '429', '403', '401']):
                logger.error(f"API error detected: {e}")
                
                # Try to fall back to Groq if not already using it
                if retry_count < max_retries and self.config.get('groq_api_key'):
                    if not isinstance(llm, ChatGroq):
                        logger.warning("Primary API failed, falling back to Groq")
                        try:
                            fallback_llm = ChatGroq(
                                model='llama-3.3-70b-versatile',
                                temperature=self.config.get('temperature', 0.7),
                                max_tokens=min(self.config.get('max_tokens', 32000), 32000),
                                groq_api_key=self.config['groq_api_key']
                            )
                            return await self._invoke_llm(fallback_llm, system, prompt, retry_count + 1)
                        except Exception as fallback_error:
                            logger.error(f"Fallback to Groq also failed: {fallback_error}")
                            raise
                    else:
                        logger.error("Already using Groq, no fallback available")
                        raise
                else:
                    logger.error(f"Max retries ({max_retries}) reached or no fallback available")
                    raise
            else:
                # Non-API errors, re-raise immediately
                logger.error(f"LLM invocation failed with non-API error: {e}")
                raise
        except Exception as e:
            logger.error(f"Unexpected error in _invoke_llm: {e}", exc_info=True)
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
        from news.ai_models import AIArticle
        from asgiref.sync import sync_to_async
        
        @sync_to_async
        def load_from_db():
            return AIArticle.objects.select_related('keyword').get(id=article_id)
        
        return await load_from_db()
    
    async def _extract_article_data(self, article):
        """Extract article data to avoid async DB queries later."""
        from asgiref.sync import sync_to_async
        
        @sync_to_async
        def extract_data():
            return {
                'keyword': article.keyword.keyword,
                'template_type': article.template_type,
                'target_word_count': article.target_word_count,
                'focus_keywords': article.focus_keywords or [],
                'related_keywords': article.keyword.related_keywords or [],
            }
        
        return await extract_data()
    
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
    
    async def _save_intermediate_data(self, article_id: str, stage_name: str, result: Dict, context: Dict):
        """Save intermediate data after critical stages to prevent data loss."""
        from news.ai_models import AIArticle
        from asgiref.sync import sync_to_async
        
        logger.info(f"Saving intermediate data for stage: {stage_name}")
        
        @sync_to_async
        def save_data():
            article = AIArticle.objects.get(id=article_id)
            
            if stage_name == 'research':
                # Save research data
                research_data = result.get('research_data', {})
                article.research_data = research_data
                logger.info(f"Saved research data: {research_data.get('source_count', 0)} sources")
                
            elif stage_name == 'outline':
                # Save outline
                outline_data = result.get('outline', {})
                article.outline = outline_data
                logger.info(f"Saved outline with {len(outline_data.get('sections', []))} sections")
                
            elif stage_name == 'content_generation':
                # Save raw content
                content = result.get('content', '')
                article.raw_content = content
                article.actual_word_count = result.get('word_count', 0)
                logger.info(f"Saved content: {len(content)} chars, {article.actual_word_count} words")
                
            elif stage_name == 'humanization':
                # Update with humanized content
                humanized_content = result.get('content', '')
                if humanized_content:
                    article.raw_content = humanized_content
                    logger.info(f"Updated with humanized content: {len(humanized_content)} chars")
            
            elif stage_name == 'ai_detection':
                # Save AI detection score
                ai_score = result.get('ai_score')
                if ai_score is not None:
                    article.ai_score = ai_score
                    logger.info(f"Saved AI detection score: {ai_score}%")
            
            elif stage_name == 'plagiarism_check':
                # Save plagiarism score
                plagiarism_score = result.get('plagiarism_percentage')
                if plagiarism_score is not None:
                    article.plagiarism_score = plagiarism_score
                    logger.info(f"Saved plagiarism score: {plagiarism_score}%")
            
            elif stage_name == 'bias_detection':
                # Save bias score
                bias_score = result.get('bias_score')
                if bias_score is not None:
                    article.bias_score = bias_score
                    logger.info(f"Saved bias score: {bias_score}%")
            
            elif stage_name == 'fact_verification':
                # Save fact check score
                fact_score = result.get('fact_score') or result.get('accuracy_score')
                if fact_score is not None:
                    article.fact_check_score = fact_score
                    logger.info(f"Saved fact check score: {fact_score}%")
            
            elif stage_name == 'seo_optimization':
                # Save SEO score and metadata
                seo_score = result.get('seo_score')
                if seo_score is not None:
                    article.seo_score = seo_score
                    logger.info(f"Saved SEO score: {seo_score}%")
                
                # Save meta data
                if result.get('meta_title'):
                    article.meta_title = result.get('meta_title')
                if result.get('meta_description'):
                    article.meta_description = result.get('meta_description')
                if result.get('focus_keywords'):
                    article.focus_keywords = result.get('focus_keywords')
            
            elif stage_name == 'quality_check':
                # Save overall quality and readability scores
                overall_score = result.get('overall_score')
                if overall_score is not None:
                    article.overall_quality_score = overall_score
                    logger.info(f"Saved overall quality score: {overall_score}%")
                
                readability_score = result.get('readability_score')
                if readability_score is not None:
                    article.readability_score = readability_score
                    logger.info(f"Saved readability score: {readability_score}%")
            
            article.save()
            logger.info(f"✅ Intermediate data saved for {stage_name}")
        
        try:
            await save_data()
        except Exception as e:
            logger.error(f"Failed to save intermediate data for {stage_name}: {e}")
            # Don't raise - continue pipeline even if save fails
    
    async def _save_article_data(self, article_id: str, context: Dict, quality_scores: Dict):
        """Save final article data to database."""
        from news.ai_models import AIArticle
        from asgiref.sync import sync_to_async
        import markdown
        
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
            
            # Convert Markdown to HTML for publishing
            if final_content:
                html_content = markdown.markdown(
                    final_content,
                    extensions=[
                        'markdown.extensions.extra',      # Tables, footnotes, etc.
                        'markdown.extensions.nl2br',      # Convert newlines to <br>
                        'markdown.extensions.sane_lists', # Better list handling
                        'markdown.extensions.toc',        # Table of contents
                        'markdown.extensions.codehilite', # Code syntax highlighting
                        'markdown.extensions.fenced_code', # Fenced code blocks
                    ]
                )
                article.raw_content = html_content
            else:
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
            
            # Save quality scores to individual fields
            if quality_scores.get('ai_score') is not None:
                article.ai_score = quality_scores['ai_score']
                logger.info(f"Saved AI score: {article.ai_score}")
            
            if quality_scores.get('plagiarism_score') is not None:
                article.plagiarism_score = quality_scores['plagiarism_score']
                logger.info(f"Saved plagiarism score: {article.plagiarism_score}")
            
            if quality_scores.get('seo_score') is not None:
                article.seo_score = quality_scores['seo_score']
                logger.info(f"Saved SEO score: {article.seo_score}")
            
            if quality_scores.get('bias_score') is not None:
                article.bias_score = quality_scores['bias_score']
                logger.info(f"Saved bias score: {article.bias_score}")
            
            if quality_scores.get('fact_check_score') is not None:
                article.fact_check_score = quality_scores['fact_check_score']
                logger.info(f"Saved fact check score: {article.fact_check_score}")
            
            if quality_scores.get('readability_score') is not None:
                article.readability_score = quality_scores['readability_score']
                logger.info(f"Saved readability score: {article.readability_score}")
            
            # Calculate overall quality score (weighted average)
            scores = []
            weights = []
            
            if article.seo_score is not None:
                scores.append(float(article.seo_score))
                weights.append(0.25)  # 25% weight
            
            if article.ai_score is not None:
                # Invert AI score (lower is better, so 100 - score)
                scores.append(100 - float(article.ai_score))
                weights.append(0.15)  # 15% weight
            
            if article.plagiarism_score is not None:
                # Invert plagiarism (lower is better)
                scores.append(100 - float(article.plagiarism_score))
                weights.append(0.20)  # 20% weight
            
            if article.bias_score is not None:
                # Invert bias (lower is better)
                scores.append(100 - float(article.bias_score))
                weights.append(0.15)  # 15% weight
            
            if article.fact_check_score is not None:
                scores.append(float(article.fact_check_score))
                weights.append(0.15)  # 15% weight
            
            if article.readability_score is not None:
                scores.append(float(article.readability_score))
                weights.append(0.10)  # 10% weight
            
            # Calculate weighted average
            if scores and weights:
                article.overall_quality_score = sum(s * w for s, w in zip(scores, weights)) / sum(weights)
                logger.info(f"Calculated overall quality score: {article.overall_quality_score}")
            
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
        context = {'article_id': article_id}
        for stage_name in stage_names[start_index:]:
            logger.info(f"Executing stage: {stage_name}")
            stage_func = self.stages[stage_name]
            result = await stage_func(article, context)
            context[stage_name] = result
        
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