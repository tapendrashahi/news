"""
Perspective Analyzer Tool

Task 3.9: Perspective Analyzer Implementation
- PerspectiveAnalyzer class
- Identify main perspectives on topic
- Check article coverage
- analyze_perspectives() method
- Balance scoring

CRITICAL: AI Analitica requires ≥ 2 distinct viewpoints per article
"""

import re
from typing import Dict, List, Any
import logging

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)


class PerspectiveAnalyzer:
    """
    Analyzes whether article presents multiple perspectives.
    
    Target: ≥ 2 distinct viewpoints
    
    Checks:
    - Different stakeholder viewpoints
    - Pro/con balance
    - Multiple expert opinions
    - Diverse source representation
    """
    
    # Perspective indicator phrases
    PERSPECTIVE_INDICATORS = [
        r'on the other hand',
        r'however',
        r'in contrast',
        r'alternatively',
        r'opponents argue',
        r'critics say',
        r'supporters claim',
        r'proponents believe',
        r'while (some|others)',
        r'from (another|different) (perspective|viewpoint)',
        r'some (experts|analysts) (argue|believe|say)',
        r'other (experts|analysts) (argue|believe|say)',
    ]
    
    def __init__(self, llm: ChatOpenAI = None):
        """
        Initialize perspective analyzer.
        
        Args:
            llm: Optional LLM for semantic analysis
        """
        self.llm = llm
        self._init_prompts()
    
    def _init_prompts(self):
        """Initialize LLM prompts for perspective analysis."""
        self.perspective_analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in analyzing journalistic balance and perspective coverage.
            
Your task is to identify all distinct perspectives, viewpoints, or positions presented in an article.

For controversial topics, good journalism presents:
1. Multiple stakeholder viewpoints
2. Pro and con arguments
3. Different expert opinions
4. Affected parties' perspectives

AI Analitica standard: Minimum 2 distinct perspectives required."""),
            ("human", """Analyze the perspectives in this article:

TOPIC: {topic}
CONTENT: {content}

Identify all distinct perspectives/viewpoints and provide JSON:
{{
    "perspectives_found": [
        {{
            "viewpoint": "...",
            "coverage_percentage": 40,
            "key_arguments": ["...", "..."],
            "sources": ["...", "..."]
        }}
    ],
    "total_perspectives": 2,
    "balance_score": 75,
    "missing_perspectives": ["...", "..."],
    "recommendations": ["...", "..."]
}}""")
        ])
    
    def analyze_perspectives(self, content: str, topic: str = "") -> Dict[str, Any]:
        """
        Comprehensive perspective analysis.
        
        Args:
            content: Article content
            topic: Article topic/keyword
            
        Returns:
            Dictionary with perspective analysis results
        """
        logger.info("Starting perspective analysis")
        
        # Rule-based analysis
        rule_results = self._rule_based_analysis(content)
        
        # LLM-based semantic analysis (if available)
        if self.llm:
            llm_results = self._llm_based_analysis(content, topic)
            total_perspectives = max(rule_results['perspective_count'], llm_results['total_perspectives'])
            balance_score = (rule_results['balance_score'] + llm_results['balance_score']) / 2
        else:
            llm_results = None
            total_perspectives = rule_results['perspective_count']
            balance_score = rule_results['balance_score']
        
        return {
            'perspective_count': total_perspectives,
            'balance_score': round(balance_score, 2),
            'passes_threshold': total_perspectives >= 2,
            'rule_based_analysis': rule_results,
            'llm_analysis': llm_results,
            'recommendations': self._generate_recommendations(total_perspectives, balance_score, llm_results)
        }
    
    def _rule_based_analysis(self, content: str) -> Dict[str, Any]:
        """
        Rule-based perspective detection using patterns.
        
        Returns:
            Dictionary with analysis results
        """
        # Count perspective transition indicators
        transition_count = sum(
            len(re.findall(pattern, content, re.IGNORECASE))
            for pattern in self.PERSPECTIVE_INDICATORS
        )
        
        # Count distinct quotes
        quote_count = content.count('"') // 2
        
        # Estimate perspective count
        perspective_estimate = 1 + min(transition_count, 3)
        perspective_estimate = min(perspective_estimate, 5)
        
        # Calculate balance score
        balance_score = 0
        if transition_count >= 3:
            balance_score += 40
        elif transition_count >= 1:
            balance_score += 20
        
        if quote_count >= 4:
            balance_score += 40
        elif quote_count >= 2:
            balance_score += 20
        
        return {
            'perspective_count': perspective_estimate,
            'balance_score': min(balance_score + 20, 100),
            'indicators': {
                'transition_phrases': transition_count,
                'quote_count': quote_count
            }
        }
    
    def _llm_based_analysis(self, content: str, topic: str) -> Dict[str, Any]:
        """LLM-based semantic perspective analysis."""
        try:
            messages = self.perspective_analysis_prompt.format_messages(
                topic=topic,
                content=content[:4000]
            )
            
            response = self.llm.invoke(messages)
            import json
            return json.loads(response.content)
            
        except Exception as e:
            logger.error(f"LLM perspective analysis failed: {e}")
            return {'total_perspectives': 1, 'balance_score': 50, 'error': str(e)}
    
    def _generate_recommendations(self, perspective_count: int, balance_score: float, llm_analysis: Dict = None) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if perspective_count >= 2:
            recommendations.append(f"✓ Adequate perspective coverage: {perspective_count} viewpoints")
        else:
            recommendations.append(f"✗ Insufficient perspectives: Only {perspective_count} - need minimum 2")
        
        if balance_score >= 75:
            recommendations.append(f"✓ Well-balanced: {balance_score:.1f}/100")
        else:
            recommendations.append(f"⚠ Needs better balance: {balance_score:.1f}/100")
        
        return recommendations
