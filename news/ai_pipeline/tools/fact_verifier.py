"""
Fact Verification Tool

Task 3.8: Fact Verification Tool Implementation
- FactVerificationTool class
- Extract factual claims
- Check for citations
- Verify source credibility
- verify_facts() method

CRITICAL: AI Analitica requires >80% of factual claims to be cited
"""

import re
from typing import Dict, List, Any, Tuple
from decimal import Decimal
import logging

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)


class FactVerificationTool:
    """
    Verifies facts and citations in news articles.
    
    Target: >80% fact verification score
    
    Checks:
    - Factual claims identified
    - Citations present for claims
    - Source credibility
    - Data accuracy
    """
    
    # Trusted news sources (high credibility)
    TRUSTED_SOURCES = {
        'tier_1': [  # Highest credibility
            'reuters.com', 'ap.org', 'apnews.com', 'bbc.com', 'bbc.co.uk',
            'npr.org', 'pbs.org', 'c-span.org'
        ],
        'tier_2': [  # High credibility
            'nytimes.com', 'washingtonpost.com', 'wsj.com', 'bloomberg.com',
            'economist.com', 'ft.com', 'theguardian.com', 'latimes.com'
        ],
        'tier_3': [  # Good credibility
            'usatoday.com', 'politico.com', 'thehill.com', 'axios.com',
            'propublica.org', 'abcnews.go.com', 'cbsnews.com', 'nbcnews.com'
        ]
    }
    
    # Academic and research sources
    ACADEMIC_SOURCES = [
        '.edu', '.gov', 'nih.gov', 'cdc.gov', 'who.int', 'nature.com',
        'science.org', 'nejm.org', 'thelancet.com', 'bmj.com', 'plos.org'
    ]
    
    # Fact-check claim indicators
    CLAIM_INDICATORS = [
        r'\d+%',  # Percentages
        r'\$[\d,]+',  # Money amounts
        r'\d{1,3}(?:,\d{3})*(?:\.\d+)?',  # Large numbers with commas
        r'\d+ (people|million|billion|thousand|hundred)',  # Quantities
        r'in \d{4}',  # Years
        r'(increased|decreased|rose|fell|dropped) by',  # Changes
        r'(study|research|report|survey|poll) (found|showed|revealed|indicated)',
    ]
    
    # Citation patterns
    CITATION_PATTERNS = [
        r'according to ([^,\.]+)',
        r'([^,\.]+) (said|stated|reported|announced|confirmed)',
        r'\[([^\]]+)\]',  # [Source]
        r'\(([^)]+)\)',  # (Source)
        r'source:\s*([^,\.]+)',
        r'via ([^,\.]+)',
        r'per ([^,\.]+)',
    ]
    
    def __init__(self, llm: ChatOpenAI = None):
        """
        Initialize fact verifier.
        
        Args:
            llm: Optional LLM for claim extraction
        """
        self.llm = llm
        self._init_prompts()
    
    def _init_prompts(self):
        """Initialize LLM prompts for fact extraction."""
        self.claim_extraction_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a fact-checking expert who extracts verifiable factual claims from text.
            
A factual claim is a statement that can be verified as true or false, such as:
- Statistics and data points
- Specific events that happened
- Quotes from named individuals
- Scientific findings
- Historical facts
- Measurements and quantities

NOT factual claims:
- Opinions
- Predictions about the future
- Subjective assessments
- General statements without specific data"""),
            ("human", """Extract all factual claims from this text:

TEXT: {content}

For each claim, provide:
1. The exact claim text
2. Type of claim (statistic/event/quote/scientific/historical/other)
3. Whether it has a citation in the text
4. The citation if present

Format as JSON:
{{
    "claims": [
        {{
            "claim": "Unemployment dropped to 3.5% in 2023",
            "type": "statistic",
            "has_citation": true,
            "citation": "Bureau of Labor Statistics",
            "verification_needed": "high"
        }}
    ],
    "total_claims": 5,
    "cited_claims": 3,
    "uncited_claims": 2
}}""")
        ])
        
        self.source_credibility_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in evaluating source credibility for journalism.
            
Evaluate sources based on:
1. Editorial standards and fact-checking processes
2. Track record of accuracy
3. Transparency about methodology
4. Independence from conflicts of interest
5. Expert recognition in the field"""),
            ("human", """Evaluate the credibility of this source:

SOURCE: {source_name}
URL: {source_url}
CONTEXT: {context}

Provide credibility assessment:
{{
    "credibility_score": 0-100,
    "tier": "tier_1/tier_2/tier_3/questionable",
    "strengths": ["...", "..."],
    "concerns": ["...", "..."],
    "recommendation": "reliable/use_with_caution/verify_independently/avoid"
}}""")
        ])
    
    def verify_facts(self, content: str, title: str = "") -> Dict[str, Any]:
        """
        Comprehensive fact verification analysis.
        
        Args:
            content: Article content
            title: Article title
            
        Returns:
            Dictionary with fact verification results
        """
        logger.info("Starting fact verification analysis")
        
        # Extract claims
        if self.llm:
            claims = self._llm_extract_claims(content)
        else:
            claims = self._rule_based_claim_extraction(content)
        
        # Analyze citations
        citations = self._extract_citations(content)
        
        # Evaluate source credibility
        source_scores = self._evaluate_sources(citations)
        
        # Calculate verification score
        total_claims = len(claims['claims'])
        cited_claims = len([c for c in claims['claims'] if c.get('has_citation')])
        
        if total_claims > 0:
            verification_score = (cited_claims / total_claims) * 100
        else:
            verification_score = 100  # No claims to verify
        
        # Weighted score considering source credibility
        if source_scores['sources']:
            avg_source_credibility = sum(s['score'] for s in source_scores['sources']) / len(source_scores['sources'])
            weighted_score = (verification_score * 0.7) + (avg_source_credibility * 0.3)
        else:
            weighted_score = verification_score * 0.7  # Penalty for no sources
        
        return {
            'verification_score': round(weighted_score, 2),
            'passes_threshold': weighted_score >= 80.0,
            'total_claims': total_claims,
            'cited_claims': cited_claims,
            'uncited_claims': total_claims - cited_claims,
            'claims_analysis': claims,
            'citations': citations,
            'source_credibility': source_scores,
            'recommendations': self._generate_recommendations(claims, citations, source_scores)
        }
    
    def _rule_based_claim_extraction(self, content: str) -> Dict[str, Any]:
        """
        Extract potential factual claims using pattern matching.
        
        Returns:
            Dictionary with extracted claims
        """
        claims = []
        sentences = re.split(r'[.!?]+', content)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Check if sentence contains claim indicators
            claim_score = 0
            claim_type = 'other'
            
            for pattern in self.CLAIM_INDICATORS:
                if re.search(pattern, sentence, re.IGNORECASE):
                    claim_score += 1
                    if r'\d+%' in pattern:
                        claim_type = 'statistic'
                    elif r'study|research' in pattern:
                        claim_type = 'scientific'
            
            # If sentence looks like a claim (has numbers, data, etc.)
            if claim_score > 0:
                # Check for citation in same sentence
                has_citation = any(
                    re.search(pattern, sentence, re.IGNORECASE)
                    for pattern in self.CITATION_PATTERNS
                )
                
                claims.append({
                    'claim': sentence,
                    'type': claim_type,
                    'has_citation': has_citation,
                    'confidence': min(claim_score / len(self.CLAIM_INDICATORS), 1.0)
                })
        
        return {
            'claims': claims,
            'total_claims': len(claims),
            'cited_claims': len([c for c in claims if c['has_citation']]),
            'extraction_method': 'rule_based'
        }
    
    def _llm_extract_claims(self, content: str) -> Dict[str, Any]:
        """
        Use LLM to extract factual claims with better accuracy.
        
        Returns:
            Dictionary with extracted claims
        """
        try:
            messages = self.claim_extraction_prompt.format_messages(
                content=content[:4000]  # Token limit
            )
            
            response = self.llm.invoke(messages)
            
            import json
            result = json.loads(response.content)
            result['extraction_method'] = 'llm'
            return result
            
        except Exception as e:
            logger.error(f"LLM claim extraction failed: {e}")
            # Fallback to rule-based
            return self._rule_based_claim_extraction(content)
    
    def _extract_citations(self, content: str) -> List[Dict[str, str]]:
        """
        Extract all citations from content.
        
        Returns:
            List of citation dictionaries
        """
        citations = []
        seen_sources = set()
        
        for pattern in self.CITATION_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                source_text = match.group(1) if match.groups() else match.group(0)
                source_text = source_text.strip()
                
                # Avoid duplicates
                if source_text.lower() not in seen_sources:
                    seen_sources.add(source_text.lower())
                    citations.append({
                        'source': source_text,
                        'context': match.group(0),
                        'position': match.start()
                    })
        
        # Also extract URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, content)
        for url in urls:
            citations.append({
                'source': url,
                'type': 'url',
                'context': url
            })
        
        return citations
    
    def _evaluate_sources(self, citations: List[Dict]) -> Dict[str, Any]:
        """
        Evaluate credibility of cited sources.
        
        Returns:
            Dictionary with source evaluation results
        """
        evaluated_sources = []
        
        for citation in citations:
            source = citation['source']
            
            # Check against known trusted sources
            credibility_score = 50  # Default: unknown
            tier = 'unknown'
            
            source_lower = source.lower()
            
            # Check tier 1 (highest credibility)
            if any(trusted in source_lower for trusted in self.TRUSTED_SOURCES['tier_1']):
                credibility_score = 95
                tier = 'tier_1'
            # Check tier 2
            elif any(trusted in source_lower for trusted in self.TRUSTED_SOURCES['tier_2']):
                credibility_score = 85
                tier = 'tier_2'
            # Check tier 3
            elif any(trusted in source_lower for trusted in self.TRUSTED_SOURCES['tier_3']):
                credibility_score = 75
                tier = 'tier_3'
            # Check academic sources
            elif any(academic in source_lower for academic in self.ACADEMIC_SOURCES):
                credibility_score = 90
                tier = 'academic'
            
            evaluated_sources.append({
                'source': source,
                'score': credibility_score,
                'tier': tier,
                'type': citation.get('type', 'citation')
            })
        
        # Calculate average credibility
        if evaluated_sources:
            avg_credibility = sum(s['score'] for s in evaluated_sources) / len(evaluated_sources)
        else:
            avg_credibility = 0
        
        return {
            'sources': evaluated_sources,
            'average_credibility': round(avg_credibility, 2),
            'tier_1_count': len([s for s in evaluated_sources if s['tier'] == 'tier_1']),
            'tier_2_count': len([s for s in evaluated_sources if s['tier'] == 'tier_2']),
            'tier_3_count': len([s for s in evaluated_sources if s['tier'] == 'tier_3']),
            'academic_count': len([s for s in evaluated_sources if s['tier'] == 'academic']),
            'unknown_count': len([s for s in evaluated_sources if s['tier'] == 'unknown']),
        }
    
    def _generate_recommendations(self, claims: Dict, citations: List, sources: Dict) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        total_claims = claims['total_claims']
        cited_claims = claims['cited_claims']
        
        if total_claims == 0:
            recommendations.append("✓ No factual claims requiring verification")
            return recommendations
        
        citation_rate = (cited_claims / total_claims) * 100 if total_claims > 0 else 0
        
        if citation_rate >= 80:
            recommendations.append(f"✓ Good citation rate: {citation_rate:.1f}%")
        elif citation_rate >= 60:
            recommendations.append(f"⚠ Moderate citation rate: {citation_rate:.1f}% (target: >80%)")
            recommendations.append(f"Add citations for {total_claims - cited_claims} uncited claims")
        else:
            recommendations.append(f"✗ Low citation rate: {citation_rate:.1f}% (target: >80%)")
            recommendations.append(f"CRITICAL: Add citations for {total_claims - cited_claims} uncited claims")
        
        # Source quality recommendations
        if sources['average_credibility'] >= 80:
            recommendations.append(f"✓ High source credibility: {sources['average_credibility']:.1f}/100")
        elif sources['average_credibility'] >= 60:
            recommendations.append(f"⚠ Moderate source credibility: {sources['average_credibility']:.1f}/100")
            recommendations.append("Consider adding more tier-1 or academic sources")
        else:
            recommendations.append(f"✗ Low source credibility: {sources['average_credibility']:.1f}/100")
            recommendations.append("Replace low-credibility sources with trusted news/academic sources")
        
        # Specific source recommendations
        if sources['tier_1_count'] == 0:
            recommendations.append("Add at least one tier-1 source (Reuters, AP, BBC, NPR)")
        
        if sources['unknown_count'] > len(citations) * 0.3:
            recommendations.append(f"Verify credibility of {sources['unknown_count']} unknown sources")
        
        return recommendations
