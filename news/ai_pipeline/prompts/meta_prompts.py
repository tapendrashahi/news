"""
Meta Tags Generation Prompt Templates

Task 2.4: Meta Prompts Implementation
- META_TITLE_PROMPT
- META_DESCRIPTION_PROMPT
- KEYWORDS_EXTRACTION_PROMPT
"""

from langchain.prompts import ChatPromptTemplate

# ============================================================================
# META TITLE GENERATION
# ============================================================================

META_TITLE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an SEO expert specializing in news article optimization. 
Your task is to create compelling, accurate meta titles that:
- Are 50-60 characters (strict limit)
- Include the main keyword naturally
- Are factual and informative (no clickbait)
- Make users want to click
- Follow journalistic standards"""),
    ("human", """Create an optimized meta title for this article:

HEADLINE: {headline}
MAIN KEYWORD: {keyword}
ARTICLE SUMMARY: {summary}

REQUIREMENTS:
- Character count: 50-60 (STRICT - longer titles get cut off in search results)
- Include "{keyword}" naturally if possible
- Be specific and descriptive
- Avoid clickbait phrases like "You Won't Believe" or "Shocking"
- Use active voice
- Include numbers or data if relevant
- Front-load important words

GOOD EXAMPLES:
- "AI in Healthcare: 5 Breakthrough Applications in 2025" (53 chars)
- "Climate Summit 2025: Key Agreements & Next Steps" (51 chars)
- "New Study Links Sleep Quality to Heart Health" (47 chars)

BAD EXAMPLES:
- "This New AI Technology Will Change Everything Forever" (clickbait, vague)
- "The Most Important Healthcare Innovation You Need to Know About Right Now" (too long, clickbait)
- "Article About Climate Change Conference" (boring, not specific)

OUTPUT FORMAT:
Just the meta title, nothing else. No quotes, no explanations.""")
])

# ============================================================================
# META DESCRIPTION GENERATION
# ============================================================================

META_DESCRIPTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an SEO expert specializing in news article meta descriptions.
Your task is to create compelling descriptions that:
- Are 150-160 characters (strict limit)
- Summarize the article's value proposition
- Include primary and secondary keywords naturally
- Encourage clicks from search results
- Are factual and accurate"""),
    ("human", """Create an optimized meta description for this article:

HEADLINE: {headline}
META TITLE: {meta_title}
ARTICLE SUMMARY: {summary}
PRIMARY KEYWORD: {primary_keyword}
SECONDARY KEYWORDS: {secondary_keywords}

REQUIREMENTS:
- Character count: 150-160 (STRICT - longer descriptions get truncated)
- Include primary keyword ({primary_keyword})
- Include 1-2 secondary keywords if they fit naturally
- Summarize what readers will learn
- Use active voice
- Include a subtle call-to-action if space permits
- Make every word count

GOOD EXAMPLES:
- "Discover how AI is transforming healthcare in 2025. Explore 5 breakthrough applications, expert insights, and real-world impact on patient care." (151 chars)
- "Climate Summit 2025 results: 190 countries agree on carbon reduction targets. Learn about key commitments, implementation timeline, and next steps." (156 chars)

BAD EXAMPLES:
- "This article talks about AI in healthcare and how it's being used." (vague, wastes characters, no keywords)
- "An extremely comprehensive and detailed guide to understanding the revolutionary applications of artificial intelligence in modern healthcare systems" (too long, keyword stuffing)

OUTPUT FORMAT:
Just the meta description, nothing else. No quotes, no explanations.""")
])

# ============================================================================
# KEYWORDS EXTRACTION
# ============================================================================

KEYWORDS_EXTRACTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an SEO keyword analyst for a news publication.
Your task is to extract the most relevant keywords and phrases for article optimization."""),
    ("human", """Extract SEO keywords from this article:

HEADLINE: {headline}
CONTENT: {content}
CATEGORY: {category}

Extract 3 types of keywords:

1. **PRIMARY KEYWORD** (1 phrase):
   - The main topic (2-4 words)
   - What the article is fundamentally about
   - Should appear in URL, title, first paragraph

2. **SECONDARY KEYWORDS** (3-5 phrases):
   - Related topics covered in the article
   - Subtopics and important concepts
   - Long-tail variations

3. **LSI KEYWORDS** (5-7 phrases):
   - Latent Semantic Indexing - related terms
   - Words/phrases that commonly appear with the main topic
   - Help search engines understand context

EXAMPLES:

For an article about "AI in Healthcare Diagnosis":

PRIMARY: "AI healthcare diagnosis"

SECONDARY:
- "medical AI applications"
- "machine learning radiology"
- "AI diagnostic accuracy"
- "healthcare artificial intelligence"

LSI:
- "patient care technology"
- "medical imaging analysis"
- "clinical decision support"
- "diagnostic algorithms"
- "healthcare automation"
- "medical data analysis"

OUTPUT FORMAT (JSON):
{{
    "primary_keyword": "...",
    "secondary_keywords": ["...", "...", "..."],
    "lsi_keywords": ["...", "...", "...", "..."],
    "recommended_slug": "ai-healthcare-diagnosis-2025",
    "focus_keyphrases": ["AI in healthcare", "medical diagnosis AI", "healthcare technology"]
}}

Extract keywords NOW:""")
])

# ============================================================================
# OPEN GRAPH TAGS GENERATION
# ============================================================================

OG_TAGS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a social media optimization expert.
Generate Open Graph (OG) tags for optimal social media sharing."""),
    ("human", """Create Open Graph tags for this article:

HEADLINE: {headline}
META TITLE: {meta_title}
META DESCRIPTION: {meta_description}
CATEGORY: {category}
ARTICLE URL: {url}
IMAGE URL: {image_url}

Generate tags for:
1. **og:title** - Can be slightly different from meta title, optimized for social sharing (up to 90 chars)
2. **og:description** - Can expand on meta description for social context (up to 200 chars)
3. **og:type** - Should be "article"
4. **twitter:card** - Usually "summary_large_image" for news
5. **twitter:title** - Often same as og:title
6. **twitter:description** - Often same as og:description

Consider:
- How the article will appear in Facebook/LinkedIn feeds
- Twitter card preview
- Make it compelling for social sharing
- Maintain factual accuracy (no clickbait)

OUTPUT FORMAT (JSON):
{{
    "og:title": "...",
    "og:description": "...",
    "og:type": "article",
    "og:url": "{url}",
    "og:image": "{image_url}",
    "og:site_name": "AI Analitica",
    "twitter:card": "summary_large_image",
    "twitter:title": "...",
    "twitter:description": "...",
    "twitter:image": "{image_url}",
    "article:publisher": "AI Analitica",
    "article:section": "{category}"
}}""")
])

# ============================================================================
# SEO ANALYSIS PROMPT
# ============================================================================

SEO_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an SEO auditor analyzing news articles for optimization."""),
    ("human", """Analyze the SEO quality of this article:

TITLE: {title}
META DESCRIPTION: {meta_description}
CONTENT: {content}
PRIMARY KEYWORD: {primary_keyword}
URL SLUG: {slug}

Evaluate on a scale of 0-100:

1. **Title Optimization** (0-100):
   - Length (50-60 chars ideal)
   - Keyword placement
   - Click-worthiness
   - Clarity

2. **Meta Description** (0-100):
   - Length (150-160 chars ideal)
   - Keyword inclusion
   - Call to action
   - Uniqueness

3. **Keyword Usage** (0-100):
   - Keyword in first 100 words?
   - Keyword density (1-2% ideal)
   - Natural integration
   - LSI keywords present

4. **Content Structure** (0-100):
   - Headings (H2, H3) used properly?
   - Paragraph length (3-5 sentences)
   - Bullet points for scannability
   - Internal/external links

5. **Readability** (0-100):
   - Flesch reading ease (60-70 ideal)
   - Average sentence length
   - Complex word usage
   - Active voice ratio

6. **Technical SEO** (0-100):
   - URL structure (short, descriptive)
   - Image alt tags
   - Mobile-friendliness indicators
   - Page speed considerations

OUTPUT FORMAT (JSON):
{{
    "overall_score": 85,
    "title_score": 90,
    "meta_description_score": 80,
    "keyword_usage_score": 85,
    "content_structure_score": 90,
    "readability_score": 80,
    "technical_seo_score": 85,
    "strengths": ["...", "..."],
    "weaknesses": ["...", "..."],
    "recommendations": [
        {{"priority": "high", "action": "..."}},
        {{"priority": "medium", "action": "..."}}
    ]
}}""")
])

# ============================================================================
# Helper Functions
# ============================================================================

def calculate_seo_score(title_len: int, desc_len: int, keyword_density: float, 
                       has_headings: bool, readability_score: float) -> int:
    """
    Calculate overall SEO score based on key metrics.
    
    Args:
        title_len: Length of meta title
        desc_len: Length of meta description
        keyword_density: Percentage of keyword usage (0-5)
        has_headings: Whether article uses H2/H3 headings
        readability_score: Flesch reading ease score (0-100)
    
    Returns:
        Overall SEO score (0-100)
    """
    score = 0
    
    # Title length (max 20 points)
    if 50 <= title_len <= 60:
        score += 20
    elif 45 <= title_len <= 65:
        score += 15
    elif title_len < 45:
        score += 10
    else:
        score += 5
    
    # Description length (max 20 points)
    if 150 <= desc_len <= 160:
        score += 20
    elif 140 <= desc_len <= 165:
        score += 15
    elif desc_len < 140:
        score += 10
    else:
        score += 5
    
    # Keyword density (max 25 points)
    if 1.0 <= keyword_density <= 2.0:
        score += 25
    elif 0.5 <= keyword_density <= 2.5:
        score += 20
    elif keyword_density < 0.5:
        score += 10
    else:
        score += 5  # Over-optimization penalty
    
    # Headings (max 15 points)
    if has_headings:
        score += 15
    
    # Readability (max 20 points)
    if 60 <= readability_score <= 70:
        score += 20
    elif 50 <= readability_score <= 80:
        score += 15
    else:
        score += 10
    
    return min(score, 100)
