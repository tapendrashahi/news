"""
Meta Tags Generation Prompt Templates

Educational Content SEO Focused on Nepal
Optimized for student search intent and Google ranking
"""

from langchain.prompts import ChatPromptTemplate

# ============================================================================
# META TITLE GENERATION
# ============================================================================

META_TITLE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an SEO expert specializing in educational blog optimization for students in Nepal.
Your task is to create compelling, student-friendly meta titles that:
- Are 50-60 characters (strict limit for Google search results)
- Include the main keyword naturally (preferably at the beginning)
- Are clear, informative, and helpful for students
- Make students want to click and learn
- Address student search intent (how-to, guides, exam prep, career advice)"""),
    ("human", """Create an optimized meta title for this educational blog article:

HEADLINE: {headline}
MAIN KEYWORD: {keyword}
ARTICLE SUMMARY: {summary}
TARGET AUDIENCE: Students in Nepal (high school, college, aspiring professionals)

REQUIREMENTS:
- Character count: 50-60 (STRICT - longer titles get cut off in Google search results)
- Include "{keyword}" naturally at the beginning if possible
- Be specific and helpful for students
- Use student-friendly language (clear, encouraging, practical)
- Include numbers or actionable words if relevant ("How to", "Guide", "Tips", "Steps")
- Front-load important keywords
- Mention "Nepal" if relevant to the topic

GOOD EXAMPLES FOR STUDENTS:
- "IOE Entrance Exam: Complete Preparation Guide 2025" (52 chars)
- "How to Choose College in Nepal: 7 Key Factors" (48 chars)
- "SEE Exam Tips: Score 3.6+ GPA in 90 Days" (42 chars)
- "Engineering Careers in Nepal: Salary & Scope" (46 chars)

BAD EXAMPLES:
- "You Won't Believe These College Selection Secrets!" (clickbait, unprofessional)
- "The Ultimate Comprehensive Guide to Preparing for Engineering Entrance Examinations in Nepal" (too long, will be cut off)
- "Article About Studying" (boring, vague, no keyword)
- "Everything Students Need to Know Right Now" (vague, no specific value)

OUTPUT FORMAT:
Just the meta title, nothing else. No quotes, no explanations.""")
])

# ============================================================================
# META DESCRIPTION GENERATION
# ============================================================================

META_DESCRIPTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an SEO expert specializing in educational blog meta descriptions for students in Nepal.
Your task is to create compelling descriptions that:
- Are 120-155 characters (strict limit for optimal mobile + desktop display)
- Summarize the article's practical value for students
- Include primary and secondary keywords naturally
- Encourage clicks from students searching for help
- Are clear, helpful, and action-oriented"""),
    ("human", """Create an optimized meta description for this educational blog article:

HEADLINE: {headline}
META TITLE: {meta_title}
ARTICLE SUMMARY: {summary}
PRIMARY KEYWORD: {primary_keyword}
SECONDARY KEYWORDS: {secondary_keywords}
TARGET AUDIENCE: Students in Nepal (high school, college, aspiring professionals)

REQUIREMENTS:
- Character count: 120-155 (STRICT - longer descriptions get truncated in Google search)
- Include primary keyword ({primary_keyword}) naturally
- Include 1-2 secondary keywords if they fit naturally
- Summarize what students will learn or gain
- Use active, encouraging language ("Learn", "Discover", "Master", "Get")
- Include a clear benefit or outcome for students
- Mention Nepal context if relevant
- Include subtle call-to-action if space permits ("Start now", "Read more", "Get started")
- Make every word count - no filler

GOOD EXAMPLES FOR STUDENTS:
- "Master IOE entrance exam prep with proven strategies, practice questions & tips. Score higher in Nepal's top engineering entrance." (132 chars)
- "Choose the right college in Nepal with our 7-factor guide. Compare programs, fees, placements & campus life. Make smart decisions." (135 chars)
- "Get 3.6+ GPA in SEE with effective study tips, time management & exam strategies. Proven methods for Nepali students. Start today!" (134 chars)

BAD EXAMPLES:
- "This article talks about IOE exam preparation and studying." (vague, wastes characters, no value proposition)
- "An extremely comprehensive and ultimate detailed guide to understanding and mastering all aspects of engineering entrance examination preparation for students" (too long, keyword stuffing, will be cut off)
- "Read this article to learn stuff." (vague, no keywords, unprofessional)

OUTPUT FORMAT:
Just the meta description, nothing else. No quotes, no explanations.""")
])

# ============================================================================
# KEYWORDS EXTRACTION
# ============================================================================

KEYWORDS_EXTRACTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an SEO keyword analyst specializing in educational content for students in Nepal.
Your task is to extract the most relevant keywords and phrases that students use when searching for educational information."""),
    ("human", """Extract SEO keywords from this educational blog article:

HEADLINE: {headline}
CONTENT: {content}
CATEGORY: {category}
TARGET AUDIENCE: Students in Nepal

Extract 3 types of keywords based on student search behavior:

1. **PRIMARY KEYWORD** (1 phrase):
   - The main topic students are searching for (2-5 words)
   - What the article is fundamentally about
   - Should appear in URL, title, first paragraph
   - Think: "What would a student type in Google?"

2. **SECONDARY KEYWORDS** (3-5 phrases):
   - Related topics students want to learn about
   - Subtopics and important concepts covered
   - Long-tail variations students might search
   - Include Nepal-specific terms if relevant

3. **LSI KEYWORDS** (5-7 phrases):
   - Latent Semantic Indexing - related terms students use
   - Words/phrases that commonly appear with the main topic in student searches
   - Help Google understand educational context
   - Include Nepal education system terms if relevant

EXAMPLES FOR EDUCATIONAL CONTENT:

For an article about "IOE Entrance Exam Preparation":

PRIMARY: "IOE entrance exam preparation"

SECONDARY:
- "IOE entrance exam syllabus"
- "engineering entrance Nepal"
- "IOE exam study tips"
- "best books for IOE entrance"
- "IOE entrance mock test"

LSI:
- "Tribhuvan University engineering"
- "entrance exam strategy"
- "Nepal engineering colleges"
- "IOE preparation course"
- "entrance exam practice questions"
- "engineering career Nepal"
- "college admission Nepal"

For an article about "How to Choose College in Nepal":

PRIMARY: "how to choose college in Nepal"

SECONDARY:
- "best colleges in Nepal"
- "college selection tips"
- "Nepal college comparison"
- "choosing right degree"

LSI:
- "higher education Nepal"
- "college admission process"
- "university programs Nepal"
- "career guidance students"
- "college fees Nepal"
- "campus facilities"
- "placement records"

OUTPUT FORMAT (JSON):
{{
    "primary_keyword": "...",
    "secondary_keywords": ["...", "...", "..."],
    "lsi_keywords": ["...", "...", "...", "..."],
    "recommended_slug": "ioe-entrance-exam-preparation-guide",
    "focus_keyphrases": ["IOE entrance exam", "engineering entrance Nepal", "exam preparation tips"],
    "nepal_specific_keywords": ["SEE exam", "TU colleges", "Kathmandu University"],
    "student_search_intent": "informational/how-to/exam-prep/career-guidance"
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
