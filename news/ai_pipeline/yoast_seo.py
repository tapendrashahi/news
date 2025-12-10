"""
YoastSEO Integration Service

Integrates with self-hosted WordPress + YoastSEO plugin for:
- SEO Score analysis
- Keyword Density check
- Readability Score
- Passive Voice detection
- Sentence Length analysis
- Focus Keyword optimization
- Meta Description analysis

Setup Requirements:
1. Install WordPress on your server/VPS/Docker
2. Install YoastSEO plugin
3. Expose REST API endpoint
4. Set YOAST_SEO_URL in environment variables
"""

import os
import requests
import logging
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class YoastSEOService:
    """Service for analyzing content using self-hosted YoastSEO."""
    
    def __init__(self):
        """Initialize YoastSEO service with configuration."""
        self.base_url = os.getenv('YOAST_SEO_URL', '')
        self.api_endpoint = f"{self.base_url}/wp-json/yoast/v1/analyze"
        self.timeout = 30
        self.enabled = bool(self.base_url)
        
        if not self.enabled:
            logger.warning("YoastSEO not configured. Set YOAST_SEO_URL environment variable.")
    
    def analyze_content(
        self,
        content: str,
        title: str,
        focus_keyword: str,
        meta_description: Optional[str] = None,
        slug: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze content using YoastSEO.
        
        Args:
            content: Article HTML content
            title: Article title
            focus_keyword: Primary keyword to optimize for
            meta_description: Meta description (optional)
            slug: URL slug (optional)
        
        Returns:
            Dictionary with SEO analysis results
        """
        if not self.enabled:
            return self._get_fallback_analysis(content, title, focus_keyword)
        
        try:
            # Prepare payload for YoastSEO API
            payload = {
                'text': content,
                'title': title,
                'keyword': focus_keyword,
                'description': meta_description or '',
                'slug': slug or '',
                'locale': 'en_US'
            }
            
            # Call YoastSEO API
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Parse and return results
            return self._parse_yoast_response(result)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"YoastSEO API error: {e}")
            return self._get_fallback_analysis(content, title, focus_keyword)
        except Exception as e:
            logger.error(f"Unexpected error in YoastSEO analysis: {e}")
            return self._get_fallback_analysis(content, title, focus_keyword)
    
    def _parse_yoast_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse YoastSEO API response into standardized format.
        
        Args:
            response: Raw response from YoastSEO API
        
        Returns:
            Standardized analysis results
        """
        return {
            'seo_score': response.get('score', 0),
            'seo_rating': response.get('rating', 'needs_improvement'),
            'keyword_density': response.get('keywordDensity', 0),
            'readability_score': response.get('readabilityScore', 0),
            'readability_rating': response.get('readabilityRating', 'needs_improvement'),
            'passive_voice_percentage': response.get('passiveVoice', 0),
            'sentence_length_score': response.get('sentenceLengthScore', 0),
            'focus_keyword_found': response.get('focusKeywordFound', False),
            'keyword_in_title': response.get('keywordInTitle', False),
            'keyword_in_description': response.get('keywordInDescription', False),
            'keyword_in_url': response.get('keywordInUrl', False),
            'meta_description_length': response.get('metaDescriptionLength', 0),
            'title_length': response.get('titleLength', 0),
            'issues': response.get('problems', []),
            'improvements': response.get('improvements', []),
            'good_results': response.get('goodResults', []),
            'raw_response': response
        }
    
    def _get_fallback_analysis(
        self,
        content: str,
        title: str,
        focus_keyword: str
    ) -> Dict[str, Any]:
        """
        Provide basic SEO analysis when YoastSEO is unavailable.
        
        Args:
            content: Article content
            title: Article title
            focus_keyword: Focus keyword
        
        Returns:
            Basic SEO analysis results
        """
        logger.info("Using fallback SEO analysis (YoastSEO unavailable)")
        
        # Strip HTML tags for text analysis
        text = BeautifulSoup(content, 'html.parser').get_text()
        words = text.lower().split()
        word_count = len(words)
        
        # Calculate keyword density
        keyword_count = text.lower().count(focus_keyword.lower())
        keyword_density = (keyword_count / word_count * 100) if word_count > 0 else 0
        
        # Check keyword in title
        keyword_in_title = focus_keyword.lower() in title.lower()
        
        # Basic readability (simplified Flesch Reading Ease)
        sentences = text.count('.') + text.count('!') + text.count('?')
        avg_sentence_length = word_count / sentences if sentences > 0 else word_count
        
        # Estimate scores
        seo_score = 50  # Neutral baseline
        if keyword_in_title:
            seo_score += 15
        if 1 <= keyword_density <= 3:
            seo_score += 15
        if 600 <= word_count <= 2500:
            seo_score += 10
        
        readability_score = 60  # Baseline
        if 15 <= avg_sentence_length <= 25:
            readability_score += 20
        
        issues = []
        improvements = []
        
        if not keyword_in_title:
            issues.append("Focus keyword not found in title")
        if keyword_density < 0.5:
            improvements.append("Consider using focus keyword more frequently")
        elif keyword_density > 3:
            improvements.append("Keyword density too high - reduce keyword stuffing")
        if word_count < 300:
            issues.append("Content too short - aim for at least 600 words")
        if avg_sentence_length > 25:
            improvements.append("Sentences too long - improve readability")
        
        return {
            'seo_score': min(100, max(0, seo_score)),
            'seo_rating': 'ok' if seo_score >= 60 else 'needs_improvement',
            'keyword_density': round(keyword_density, 2),
            'readability_score': min(100, max(0, readability_score)),
            'readability_rating': 'good' if readability_score >= 60 else 'needs_improvement',
            'passive_voice_percentage': 0,  # Not calculated in fallback
            'sentence_length_score': 100 - min(100, abs(avg_sentence_length - 20) * 5),
            'focus_keyword_found': keyword_count > 0,
            'keyword_in_title': keyword_in_title,
            'keyword_in_description': False,  # Not available in fallback
            'keyword_in_url': False,  # Not available in fallback
            'meta_description_length': 0,
            'title_length': len(title),
            'word_count': word_count,
            'avg_sentence_length': round(avg_sentence_length, 1),
            'issues': issues,
            'improvements': improvements,
            'good_results': [],
            'fallback_mode': True
        }
    
    def optimize_content(
        self,
        content: str,
        title: str,
        focus_keyword: str,
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Suggest optimizations based on SEO analysis.
        
        Args:
            content: Original content
            title: Original title
            focus_keyword: Focus keyword
            analysis: SEO analysis results
        
        Returns:
            Dictionary with optimization suggestions
        """
        suggestions = {
            'title_suggestions': [],
            'content_suggestions': [],
            'meta_suggestions': [],
            'overall_priority': []
        }
        
        # Title optimizations
        if not analysis.get('keyword_in_title'):
            suggestions['title_suggestions'].append(
                f"Add focus keyword '{focus_keyword}' to the title"
            )
            suggestions['overall_priority'].append('HIGH: Keyword missing in title')
        
        if analysis.get('title_length', 0) > 60:
            suggestions['title_suggestions'].append(
                "Shorten title to under 60 characters for better display in search results"
            )
        elif analysis.get('title_length', 0) < 30:
            suggestions['title_suggestions'].append(
                "Lengthen title to 30-60 characters for better SEO"
            )
        
        # Content optimizations
        keyword_density = analysis.get('keyword_density', 0)
        if keyword_density < 0.5:
            suggestions['content_suggestions'].append(
                f"Increase keyword density (current: {keyword_density}%, target: 1-2%)"
            )
            suggestions['overall_priority'].append('MEDIUM: Low keyword density')
        elif keyword_density > 3:
            suggestions['content_suggestions'].append(
                f"Reduce keyword density to avoid keyword stuffing (current: {keyword_density}%)"
            )
            suggestions['overall_priority'].append('HIGH: Keyword stuffing detected')
        
        # Readability
        if analysis.get('readability_score', 100) < 60:
            suggestions['content_suggestions'].append(
                "Improve readability: use shorter sentences and simpler words"
            )
            suggestions['overall_priority'].append('MEDIUM: Poor readability')
        
        # Meta description
        if analysis.get('meta_description_length', 0) == 0:
            suggestions['meta_suggestions'].append(
                "Add a meta description (120-160 characters)"
            )
        elif analysis.get('meta_description_length', 0) > 160:
            suggestions['meta_suggestions'].append(
                "Shorten meta description to 120-160 characters"
            )
        
        if not analysis.get('keyword_in_description'):
            suggestions['meta_suggestions'].append(
                f"Include focus keyword '{focus_keyword}' in meta description"
            )
        
        # Add analysis issues and improvements
        for issue in analysis.get('issues', []):
            suggestions['overall_priority'].append(f'HIGH: {issue}')
        
        for improvement in analysis.get('improvements', []):
            suggestions['content_suggestions'].append(improvement)
        
        return suggestions
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if YoastSEO service is available and working.
        
        Returns:
            Health check status
        """
        if not self.enabled:
            return {
                'status': 'disabled',
                'message': 'YoastSEO not configured',
                'using_fallback': True
            }
        
        try:
            # Try a simple request to check connectivity
            response = requests.get(
                f"{self.base_url}/wp-json/",
                timeout=5
            )
            response.raise_for_status()
            
            return {
                'status': 'healthy',
                'message': 'YoastSEO service is available',
                'endpoint': self.api_endpoint,
                'using_fallback': False
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'YoastSEO service unavailable: {str(e)}',
                'using_fallback': True
            }


# Singleton instance
_yoast_service = None

def get_yoast_service() -> YoastSEOService:
    """Get or create YoastSEO service instance."""
    global _yoast_service
    if _yoast_service is None:
        _yoast_service = YoastSEOService()
    return _yoast_service
