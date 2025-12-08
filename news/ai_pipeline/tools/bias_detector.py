"""
Bias Detection Tool (AI Analitica Specific)

Task 3.7: Bias Detection Tool Implementation
- BiasDetectionTool class
- Detect politically charged language
- Detect emotionally loaded words
- Check for one-sided presentation
- Flag missing perspectives
- detect_bias() method
- suggest_neutralizations() method

CRITICAL: Align with AI Analitica mission of unbiased, data-driven news
Target: < 20% bias score
"""

import re
from typing import Dict, List, Any, Tuple
from decimal import Decimal
import logging

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)


class BiasDetectionTool:
    """
    Detects bias in news articles according to AI Analitica standards.
    
    Target: Bias score < 20%
    
    Analyzes:
    - Politically charged language
    - Emotionally loaded words
    - One-sided presentation
    - Missing perspectives
    - Unbalanced source citation
    """
    
    # Bias indicator word lists
    POLITICAL_BIAS_WORDS = {
        'left': [
            'progressive', 'socialist', 'liberal agenda', 'woke', 
            'social justice warrior', 'radical left', 'far-left',
            'leftist', 'marxist', 'communist'
        ],
        'right': [
            'conservative', 'right-wing extremist', 'fascist', 
            'alt-right', 'far-right', 'reactionary', 'nationalist',
            'ultra-conservative', 'tea party', 'maga'
        ]
    }
    
    EMOTIONAL_WORDS = [
        # Negative emotional language
        'shocking', 'outrageous', 'disgusting', 'horrifying', 'terrifying',
        'devastating', 'catastrophic', 'nightmare', 'disaster', 'crisis',
        'scandal', 'shameful', 'appalling', 'disturbing', 'alarming',
        
        # Positive emotional language
        'amazing', 'incredible', 'wonderful', 'fantastic', 'remarkable',
        'extraordinary', 'miraculous', 'spectacular', 'brilliant',
        
        # Sensational language
        'bombshell', 'explosive', 'unprecedented', 'historic', 'epic',
        'game-changing', 'revolutionary', 'groundbreaking'
    ]
    
    ABSOLUTIST_WORDS = [
        'always', 'never', 'everyone', 'no one', 'all', 'none',
        'every', 'completely', 'totally', 'absolutely', 'definitely',
        'certainly', 'obviously', 'clearly', 'undoubtedly'
    ]
    
    HEDGE_WORDS = [
        'allegedly', 'reportedly', 'supposedly', 'claimed', 'suggested',
        'according to', 'sources say', 'it is believed'
    ]
    
    def __init__(self, llm: ChatOpenAI = None):
        """
        Initialize bias detector.
        
        Args:
            llm: Optional LLM for deep semantic bias analysis
        """
        self.llm = llm
        self._init_prompts()
    
    def _init_prompts(self):
        """Initialize LLM prompts for semantic bias detection."""
        self.bias_analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in detecting bias in news articles.
Your goal is to identify subtle and overt bias that violates journalistic objectivity.

Focus on:
1. Political bias (left or right leaning)
2. Emotional manipulation
3. One-sided presentation
4. Loaded language
5. Missing counter-perspectives
6. Unbalanced source citation

Rate bias on scale of 0-100 where:
- 0-20: Acceptable (objective journalism)
- 21-40: Moderate bias (needs improvement)
- 41-60: Significant bias (major rewrite needed)
- 61-100: Extreme bias (unacceptable)"""),
            ("human", """Analyze this article for bias:

TITLE: {title}
CONTENT: {content}

Provide detailed analysis in JSON format:
{{
    "overall_bias_score": 0-100,
    "political_lean": "left/right/center/unclear",
    "emotional_manipulation_score": 0-100,
    "one_sided_score": 0-100,
    "loaded_language_examples": ["...", "..."],
    "missing_perspectives": ["...", "..."],
    "source_balance": {{
        "pro_sources": 3,
        "con_sources": 1,
        "neutral_sources": 2,
        "balance_score": 0-100
    }},
    "biased_phrases": [
        {{"phrase": "...", "reason": "...", "suggestion": "..."}}
    ],
    "improvements_needed": ["...", "..."]
}}""")
        ])
        
        self.neutralization_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert editor specializing in neutral, objective journalism.
Your task is to rewrite biased text to be factual and balanced while preserving information."""),
            ("human", """Neutralize this biased text:

BIASED TEXT: {biased_text}
BIAS TYPE: {bias_type}
REASON: {reason}

Provide:
1. Neutralized version (factual, balanced, objective)
2. Explanation of changes made

Format:
{{
    "original": "...",
    "neutralized": "...",
    "changes_made": ["Removed emotional word 'shocking'", "Added balancing perspective", "..."]
}}""")
        ])
    
    def detect_bias(self, content: str, title: str = "") -> Dict[str, Any]:
        """
        Comprehensive bias detection analysis.
        
        Args:
            content: Article content to analyze
            title: Article title
            
        Returns:
            Dictionary with bias analysis results
        """
        logger.info("Starting bias detection analysis")
        
        # Combine rule-based and LLM analysis
        rule_based_results = self._rule_based_detection(content, title)
        
        if self.llm:
            llm_results = self._llm_based_detection(content, title)
            # Merge results
            final_score = (rule_based_results['bias_score'] + llm_results['overall_bias_score']) / 2
        else:
            llm_results = None
            final_score = rule_based_results['bias_score']
        
        return {
            'bias_score': round(final_score, 2),
            'passes_threshold': final_score < 20.0,
            'rule_based_analysis': rule_based_results,
            'llm_analysis': llm_results,
            'recommendations': self._generate_recommendations(rule_based_results, llm_results)
        }
    
    def _rule_based_detection(self, content: str, title: str) -> Dict[str, Any]:
        """
        Rule-based bias detection using word lists and patterns.
        
        Returns:
            Dictionary with detection results
        """
        full_text = f"{title} {content}".lower()
        word_count = len(content.split())
        
        # Detect political bias
        political_left_count = sum(full_text.count(word.lower()) for word in self.POLITICAL_BIAS_WORDS['left'])
        political_right_count = sum(full_text.count(word.lower()) for word in self.POLITICAL_BIAS_WORDS['right'])
        political_bias_total = political_left_count + political_right_count
        
        # Detect emotional language
        emotional_count = sum(full_text.count(word.lower()) for word in self.EMOTIONAL_WORDS)
        
        # Detect absolutist language
        absolutist_count = sum(full_text.count(word.lower()) for word in self.ABSOLUTIST_WORDS)
        
        # Detect hedging (good for objectivity)
        hedge_count = sum(full_text.count(phrase.lower()) for phrase in self.HEDGE_WORDS)
        
        # Check for quotes and citations
        quote_count = content.count('"')
        citation_patterns = len(re.findall(r'according to|source:|citation|\[.*\]|\(.*\)', content, re.IGNORECASE))
        
        # Calculate component scores
        political_score = min((political_bias_total / max(word_count / 100, 1)) * 10, 40)
        emotional_score = min((emotional_count / max(word_count / 100, 1)) * 8, 30)
        absolutist_score = min((absolutist_count / max(word_count / 100, 1)) * 5, 20)
        
        # Hedging is good (reduces score)
        hedge_bonus = min(hedge_count * 2, 10)
        
        # Citations are good (reduces score)
        citation_bonus = min(citation_patterns * 1.5, 10)
        
        # Overall bias score (0-100 scale)
        raw_score = political_score + emotional_score + absolutist_score
        bias_score = max(raw_score - hedge_bonus - citation_bonus, 0)
        
        # Determine political lean
        if political_left_count > political_right_count * 1.5:
            political_lean = "left"
        elif political_right_count > political_left_count * 1.5:
            political_lean = "right"
        else:
            political_lean = "center"
        
        return {
            'bias_score': round(bias_score, 2),
            'political_lean': political_lean,
            'indicators': {
                'political_bias_words': political_bias_total,
                'emotional_words': emotional_count,
                'absolutist_words': absolutist_count,
                'hedge_words': hedge_count,
                'citations': citation_patterns,
                'quotes': quote_count
            },
            'component_scores': {
                'political_bias': round(political_score, 2),
                'emotional_language': round(emotional_score, 2),
                'absolutist_language': round(absolutist_score, 2)
            },
            'positive_factors': {
                'hedge_bonus': round(hedge_bonus, 2),
                'citation_bonus': round(citation_bonus, 2)
            }
        }
    
    def _llm_based_detection(self, content: str, title: str) -> Dict[str, Any]:
        """
        LLM-based semantic bias detection for nuanced analysis.
        
        Returns:
            Dictionary with LLM analysis results
        """
        try:
            messages = self.bias_analysis_prompt.format_messages(
                title=title,
                content=content[:4000]  # Limit for token constraints
            )
            
            response = self.llm.invoke(messages)
            
            # Parse JSON response
            import json
            result = json.loads(response.content)
            return result
            
        except Exception as e:
            logger.error(f"LLM bias detection failed: {e}")
            return {
                'overall_bias_score': 50,
                'error': str(e)
            }
    
    def suggest_neutralizations(self, content: str, bias_analysis: Dict) -> List[Dict[str, str]]:
        """
        Generate suggestions for neutralizing biased content.
        
        Args:
            content: Original content
            bias_analysis: Results from detect_bias()
            
        Returns:
            List of neutralization suggestions
        """
        suggestions = []
        
        # Get LLM-identified biased phrases if available
        if bias_analysis.get('llm_analysis') and bias_analysis['llm_analysis'].get('biased_phrases'):
            for phrase_data in bias_analysis['llm_analysis']['biased_phrases']:
                if self.llm:
                    try:
                        messages = self.neutralization_prompt.format_messages(
                            biased_text=phrase_data['phrase'],
                            bias_type=phrase_data.get('type', 'unknown'),
                            reason=phrase_data.get('reason', 'Contains bias')
                        )
                        
                        response = self.llm.invoke(messages)
                        import json
                        neutralization = json.loads(response.content)
                        suggestions.append(neutralization)
                        
                    except Exception as e:
                        logger.error(f"Neutralization generation failed: {e}")
        
        # Add rule-based suggestions
        rule_suggestions = self._generate_rule_based_suggestions(
            content,
            bias_analysis['rule_based_analysis']
        )
        suggestions.extend(rule_suggestions)
        
        return suggestions
    
    def _generate_rule_based_suggestions(self, content: str, analysis: Dict) -> List[Dict]:
        """Generate neutralization suggestions from rule-based analysis."""
        suggestions = []
        
        # Suggest removing emotional words
        if analysis['indicators']['emotional_words'] > 0:
            suggestions.append({
                'type': 'emotional_language',
                'issue': f"Found {analysis['indicators']['emotional_words']} emotional words",
                'suggestion': "Replace emotional language with neutral, factual descriptions",
                'examples': "Change 'shocking revelation' to 'new information' or 'devastating impact' to 'significant impact'"
            })
        
        # Suggest balancing absolutist language
        if analysis['indicators']['absolutist_words'] > 3:
            suggestions.append({
                'type': 'absolutist_language',
                'issue': f"Found {analysis['indicators']['absolutist_words']} absolutist words",
                'suggestion': "Add nuance and qualifiers to absolute statements",
                'examples': "Change 'always' to 'often' or 'frequently', 'never' to 'rarely' or 'seldom'"
            })
        
        # Suggest adding citations
        if analysis['indicators']['citations'] < 3:
            suggestions.append({
                'type': 'insufficient_citations',
                'issue': f"Only {analysis['indicators']['citations']} citations found",
                'suggestion': "Add more source attributions and citations",
                'examples': "Use phrases like 'according to [source]', 'studies show', 'experts indicate'"
            })
        
        return suggestions
    
    def _generate_recommendations(self, rule_analysis: Dict, llm_analysis: Dict = None) -> List[str]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []
        
        bias_score = rule_analysis['bias_score']
        
        if bias_score < 20:
            recommendations.append("✓ Bias score acceptable for AI Analitica standards")
        elif bias_score < 40:
            recommendations.append("⚠ Moderate bias detected - review and revise recommended")
        else:
            recommendations.append("✗ Significant bias detected - major rewrite required")
        
        # Political bias recommendations
        if rule_analysis['political_lean'] != 'center':
            recommendations.append(
                f"Balance political perspective (currently leans {rule_analysis['political_lean']})"
            )
        
        # Component-specific recommendations
        if rule_analysis['component_scores']['emotional_language'] > 10:
            recommendations.append("Reduce emotional language - use neutral descriptors")
        
        if rule_analysis['component_scores']['absolutist_language'] > 10:
            recommendations.append("Avoid absolutist statements - add nuance and qualifiers")
        
        if rule_analysis['indicators']['citations'] < 5:
            recommendations.append("Add more citations and source attributions")
        
        # LLM-based recommendations
        if llm_analysis and llm_analysis.get('improvements_needed'):
            recommendations.extend(llm_analysis['improvements_needed'][:3])
        
        return recommendations
