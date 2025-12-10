"""
Codequiry Plagiarism Detection Service

Integrates with Codequiry API for plagiarism checking of educational content.
Supports content analysis, similarity detection, and detailed plagiarism reports.
"""

import os
import requests
import json
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class PlagiarismResult:
    """Plagiarism check result data structure"""
    overall_score: float  # Plagiarism percentage (0-100)
    is_plagiarized: bool  # True if score > threshold
    threshold: float  # Threshold used for check
    sources_found: int  # Number of plagiarized sources
    matches: List[Dict]  # List of matching sources
    report_url: Optional[str] = None  # URL to detailed report
    error: Optional[str] = None  # Error message if check failed


class CodequiryPlagiarismChecker:
    """
    Codequiry API integration for plagiarism detection
    
    Features:
    - Text similarity analysis
    - Source detection
    - Detailed plagiarism reports
    - Automatic threshold checking
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Codequiry plagiarism checker
        
        Args:
            api_key: Codequiry API key (defaults to env var CODEQUIRY_API_KEY)
        """
        self.api_key = api_key or os.getenv('CODEQUIRY_API_KEY')
        if not self.api_key:
            logger.warning("CODEQUIRY_API_KEY not found in environment variables")
        
        self.base_url = "https://codequiry.com/api/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'apikey': self.api_key,
            'Content-Type': 'application/json'
        })
    
    def check_plagiarism(
        self,
        content: str,
        title: str = "Educational Article",
        threshold: float = 5.0,
        check_web: bool = True,
        check_database: bool = True
    ) -> PlagiarismResult:
        """
        Check content for plagiarism
        
        Args:
            content: Text content to check
            title: Title/identifier for the content
            threshold: Plagiarism threshold percentage (default: 5%)
            check_web: Check against web sources
            check_database: Check against Codequiry database
        
        Returns:
            PlagiarismResult with detailed plagiarism information
        """
        try:
            # Validate API key
            if not self.api_key:
                return PlagiarismResult(
                    overall_score=0.0,
                    is_plagiarized=False,
                    threshold=threshold,
                    sources_found=0,
                    matches=[],
                    error="Codequiry API key not configured"
                )
            
            # Prepare check request
            check_id = self._submit_check(content, title, check_web, check_database)
            
            if not check_id:
                return PlagiarismResult(
                    overall_score=0.0,
                    is_plagiarized=False,
                    threshold=threshold,
                    sources_found=0,
                    matches=[],
                    error="Failed to submit plagiarism check"
                )
            
            # Get check results
            results = self._get_results(check_id)
            
            if not results:
                return PlagiarismResult(
                    overall_score=0.0,
                    is_plagiarized=False,
                    threshold=threshold,
                    sources_found=0,
                    matches=[],
                    error="Failed to retrieve plagiarism results"
                )
            
            # Parse results
            overall_score = float(results.get('similarity', 0.0))
            matches = results.get('matches', [])
            sources_found = len(matches)
            report_url = results.get('report_url')
            
            is_plagiarized = overall_score > threshold
            
            logger.info(
                f"Plagiarism check complete: {overall_score:.2f}% "
                f"(threshold: {threshold}%, sources: {sources_found})"
            )
            
            return PlagiarismResult(
                overall_score=overall_score,
                is_plagiarized=is_plagiarized,
                threshold=threshold,
                sources_found=sources_found,
                matches=matches,
                report_url=report_url
            )
        
        except Exception as e:
            logger.error(f"Plagiarism check error: {str(e)}")
            return PlagiarismResult(
                overall_score=0.0,
                is_plagiarized=False,
                threshold=threshold,
                sources_found=0,
                matches=[],
                error=str(e)
            )
    
    def _submit_check(
        self,
        content: str,
        title: str,
        check_web: bool,
        check_database: bool
    ) -> Optional[str]:
        """
        Submit content for plagiarism check
        
        Args:
            content: Text to check
            title: Content title
            check_web: Check web sources
            check_database: Check database
        
        Returns:
            Check ID if successful, None otherwise
        """
        try:
            endpoint = f"{self.base_url}/check"
            
            payload = {
                "name": title,
                "content": content,
                "check_web": check_web,
                "check_database": check_database,
                "language": "text"
            }
            
            response = self.session.post(endpoint, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            check_id = result.get('check_id')
            
            logger.info(f"Plagiarism check submitted: {check_id}")
            return check_id
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to submit plagiarism check: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during check submission: {str(e)}")
            return None
    
    def _get_results(self, check_id: str, max_retries: int = 10) -> Optional[Dict]:
        """
        Get plagiarism check results
        
        Args:
            check_id: Check ID from submission
            max_retries: Maximum number of polling attempts
        
        Returns:
            Results dictionary if successful, None otherwise
        """
        try:
            import time
            endpoint = f"{self.base_url}/check/{check_id}"
            
            for attempt in range(max_retries):
                response = self.session.get(endpoint, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                status = result.get('status')
                
                if status == 'completed':
                    logger.info(f"Plagiarism check completed: {check_id}")
                    return result
                elif status == 'failed':
                    logger.error(f"Plagiarism check failed: {check_id}")
                    return None
                
                # Wait before next poll (exponential backoff)
                wait_time = min(2 ** attempt, 10)
                logger.debug(f"Check in progress, waiting {wait_time}s...")
                time.sleep(wait_time)
            
            logger.warning(f"Plagiarism check timeout: {check_id}")
            return None
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get plagiarism results: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting results: {str(e)}")
            return None
    
    def get_plagiarized_sections(self, matches: List[Dict]) -> List[Dict]:
        """
        Extract plagiarized sections from match results
        
        Args:
            matches: List of match dictionaries from plagiarism check
        
        Returns:
            List of plagiarized sections with source info
        """
        sections = []
        
        for match in matches:
            section = {
                'text': match.get('matched_text', ''),
                'source': match.get('source_url', 'Unknown'),
                'similarity': match.get('similarity', 0.0),
                'start_position': match.get('start', 0),
                'end_position': match.get('end', 0)
            }
            sections.append(section)
        
        return sections
    
    def health_check(self) -> Tuple[bool, str]:
        """
        Check if Codequiry API is accessible
        
        Returns:
            Tuple of (is_healthy, message)
        """
        try:
            if not self.api_key:
                return False, "API key not configured"
            
            endpoint = f"{self.base_url}/account"
            response = self.session.get(endpoint, timeout=10)
            
            if response.status_code == 200:
                return True, "Codequiry API is accessible"
            else:
                return False, f"API returned status {response.status_code}"
        
        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"


# Fallback plagiarism checker (when Codequiry is unavailable)
class FallbackPlagiarismChecker:
    """
    Simple fallback plagiarism checker using basic text analysis
    Used when Codequiry API is unavailable
    """
    
    def check_plagiarism(
        self,
        content: str,
        title: str = "Educational Article",
        threshold: float = 5.0,
        **kwargs
    ) -> PlagiarismResult:
        """
        Basic plagiarism check (always returns clean)
        
        This is a fallback that assumes content is original.
        In production, consider implementing basic similarity checks.
        """
        logger.warning("Using fallback plagiarism checker - no real check performed")
        
        return PlagiarismResult(
            overall_score=0.0,
            is_plagiarized=False,
            threshold=threshold,
            sources_found=0,
            matches=[],
            error="Codequiry API unavailable - using fallback (no check performed)"
        )
    
    def health_check(self) -> Tuple[bool, str]:
        """Health check for fallback checker"""
        return True, "Fallback checker active (no real plagiarism checking)"


# Factory function to get appropriate plagiarism checker
def get_plagiarism_checker() -> CodequiryPlagiarismChecker:
    """
    Get plagiarism checker instance
    
    Returns:
        CodequiryPlagiarismChecker if API key is available, FallbackPlagiarismChecker otherwise
    """
    api_key = os.getenv('CODEQUIRY_API_KEY')
    
    if api_key:
        checker = CodequiryPlagiarismChecker(api_key)
        is_healthy, message = checker.health_check()
        
        if is_healthy:
            logger.info("Codequiry plagiarism checker initialized successfully")
            return checker
        else:
            logger.warning(f"Codequiry health check failed: {message}")
    
    logger.warning("Falling back to basic plagiarism checker")
    return FallbackPlagiarismChecker()
