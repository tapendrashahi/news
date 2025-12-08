"""
SEO Optimization Prompt Templates

Task 2.4: SEO Prompts Implementation
- SEO_ANALYSIS_PROMPT
- SEO_IMPROVEMENT_PROMPT
"""

from langchain.prompts import ChatPromptTemplate

# ============================================================================
# SEO ANALYSIS PROMPT
# ============================================================================

SEO_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert SEO analyst specializing in news content optimization.
Your analysis must be thorough, actionable, and focused on improving search visibility while maintaining journalistic integrity."""),
    ("human", """Perform a comprehensive SEO analysis of this article:

ARTICLE DATA:
- Title: {title}
- Meta Description: {meta_description}
- URL Slug: {slug}
- Word Count: {word_count}
- Primary Keyword: {primary_keyword}
- Category: {category}

CONTENT:
{content}

Analyze the following aspects and provide scores (0-100):

1. **KEYWORD OPTIMIZATION** (0-100)
   - Is primary keyword in title? (Yes +20)
   - Is keyword in first 100 words? (Yes +15)
   - Keyword density (1-2% is ideal) (+20)
   - LSI keywords present (+15)
   - Keywords in headings (+15)
   - Natural integration (not stuffing) (+15)

2. **ON-PAGE SEO** (0-100)
   - Title tag length (50-60 chars ideal) (+15)
   - Meta description length (150-160 chars ideal) (+15)
   - URL structure (short, descriptive, keyword) (+10)
   - Heading hierarchy (H1 → H2 → H3) (+15)
   - Image alt text (if applicable) (+10)
   - Internal linking opportunities (+10)
   - External authoritative links (+15)
   - Content uniqueness (+10)

3. **CONTENT QUALITY** (0-100)
   - Word count (1000-2000 words ideal for news) (+20)
   - Paragraph structure (3-5 sentences) (+15)
   - Sentence variety (+10)
   - Topic coverage depth (+20)
   - Use of data/statistics (+15)
   - Expert quotes/sources (+10)
   - Multimedia elements (+10)

4. **READABILITY** (0-100)
   - Flesch Reading Ease (60-70 ideal) (+30)
   - Average sentence length (15-20 words) (+20)
   - Use of subheadings (+20)
   - Bullet points/lists for scannability (+15)
   - Active voice usage (+15)

5. **USER ENGAGEMENT SIGNALS** (0-100)
   - Compelling introduction (first 3 sentences) (+25)
   - Clear value proposition (+20)
   - Logical flow and structure (+20)
   - Conclusion/key takeaways (+15)
   - Call-to-action or next steps (+10)
   - Estimated time-on-page potential (+10)

6. **TECHNICAL SEO INDICATORS** (0-100)
   - URL length (<75 characters) (+20)
   - Use of HTTPS (assumed) (+10)
   - Mobile-friendly formatting (+20)
   - Page speed considerations (minimize images) (+15)
   - Schema markup potential (+15)
   - Canonical URL clarity (+10)
   - Social sharing optimization (+10)

OUTPUT FORMAT (JSON):
{{
    "overall_seo_score": 85,
    "scores": {{
        "keyword_optimization": 90,
        "on_page_seo": 85,
        "content_quality": 88,
        "readability": 80,
        "user_engagement": 82,
        "technical_seo": 87
    }},
    "keyword_analysis": {{
        "primary_keyword_in_title": true,
        "primary_keyword_in_first_100_words": true,
        "keyword_density": "1.5%",
        "keyword_count": 12,
        "lsi_keywords_found": ["...", "..."],
        "keyword_placement_score": 90
    }},
    "strengths": [
        "Excellent keyword density at 1.5%",
        "Strong heading structure with proper H2/H3 usage",
        "Good use of data and statistics for credibility"
    ],
    "weaknesses": [
        "Meta description too long (175 characters)",
        "Missing internal links to related articles",
        "Could benefit from more bullet point lists"
    ],
    "critical_issues": [
        "Primary keyword not in first paragraph"
    ],
    "recommendations": [
        {{
            "priority": "high",
            "category": "keyword_optimization",
            "issue": "Primary keyword '{primary_keyword}' appears in title but not in opening paragraph",
            "action": "Rewrite first paragraph to naturally include primary keyword within first 2 sentences",
            "expected_impact": "+10 SEO score"
        }},
        {{
            "priority": "high",
            "category": "on_page_seo",
            "issue": "Meta description is 175 characters (too long)",
            "action": "Trim meta description to 155 characters while keeping core message",
            "expected_impact": "+5 SEO score"
        }},
        {{
            "priority": "medium",
            "category": "content_quality",
            "issue": "No internal links to related content",
            "action": "Add 2-3 internal links to related articles on similar topics",
            "expected_impact": "+8 SEO score, better site architecture"
        }}
    ],
    "competitor_comparison": {{
        "estimated_keyword_difficulty": "medium",
        "content_gap_opportunities": ["...", "..."],
        "ranking_potential": "high"
    }}
}}""")
])

# ============================================================================
# SEO IMPROVEMENT PROMPT
# ============================================================================

SEO_IMPROVEMENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an SEO content optimizer. Your goal is to improve articles for better search visibility while maintaining quality, accuracy, and readability.

CRITICAL RULES:
- Never sacrifice factual accuracy for SEO
- Never add keywords unnaturally (no keyword stuffing)
- Maintain the article's journalistic integrity
- Preserve all sources and citations
- Keep the original meaning and tone
- Only suggest changes that improve both SEO AND readability"""),
    ("human", """Optimize this article based on the SEO analysis:

ORIGINAL ARTICLE:
{content}

SEO ANALYSIS RESULTS:
{analysis_results}

PRIMARY KEYWORD: {primary_keyword}
SECONDARY KEYWORDS: {secondary_keywords}

IMPROVEMENTS NEEDED:
{improvement_areas}

Your task:
1. Rewrite sections that need keyword optimization (naturally!)
2. Improve heading structure if needed
3. Enhance readability where flagged
4. Suggest meta tag improvements
5. Add internal/external linking opportunities
6. Optimize for featured snippets (if applicable)

SPECIFIC FOCUS AREAS:
- **Title Optimization**: {title_feedback}
- **Meta Description**: {meta_feedback}
- **Keyword Integration**: {keyword_feedback}
- **Content Structure**: {structure_feedback}

OUTPUT FORMAT (JSON):
{{
    "optimized_title": "...",
    "optimized_meta_description": "...",
    "optimized_content": "... [full article text with improvements] ...",
    "suggested_url_slug": "...",
    "changes_made": [
        {{
            "section": "Title",
            "original": "...",
            "improved": "...",
            "reason": "Added primary keyword at beginning for better SEO"
        }},
        {{
            "section": "First paragraph",
            "original": "...",
            "improved": "...",
            "reason": "Integrated primary keyword naturally in second sentence"
        }}
    ],
    "keyword_placements": {{
        "primary_keyword_count": 8,
        "primary_keyword_locations": ["title", "first_paragraph", "H2_heading", "conclusion"],
        "secondary_keywords_integrated": ["...", "..."],
        "lsi_keywords_added": ["...", "..."]
    }},
    "structural_improvements": [
        "Added H2 heading: '...'",
        "Split long paragraph (8 sentences) into two (3 and 5 sentences)",
        "Created bullet point list for key findings"
    ],
    "linking_suggestions": [
        {{
            "anchor_text": "...",
            "target_url": "internal/external",
            "placement": "After paragraph 3",
            "purpose": "Provide context on related topic"
        }}
    ],
    "featured_snippet_optimization": {{
        "target_query": "...",
        "snippet_type": "paragraph/list/table",
        "optimized_section": "..."
    }},
    "estimated_seo_improvement": "+12 points",
    "new_seo_score": 92
}}

Optimize NOW:""")
])

# ============================================================================
# READABILITY IMPROVEMENT PROMPT
# ============================================================================

READABILITY_IMPROVEMENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a readability expert specializing in news content.
Your goal is to make content more accessible while preserving accuracy and depth."""),
    ("human", """Improve the readability of this content:

CURRENT TEXT:
{content}

READABILITY ISSUES DETECTED:
- Flesch Reading Ease: {flesch_score} (target: 60-70)
- Average Sentence Length: {avg_sentence_length} words (target: 15-20)
- Complex Words: {complex_word_percentage}% (target: <15%)
- Passive Voice: {passive_voice_percentage}% (target: <10%)

IMPROVEMENT STRATEGIES:
1. **Break Long Sentences**: Split sentences >25 words into shorter ones
2. **Simplify Vocabulary**: Replace complex words with simpler alternatives (without dumbing down)
3. **Active Voice**: Convert passive constructions to active
4. **Add Transitions**: Improve flow between paragraphs
5. **Vary Sentence Length**: Mix short (5-10), medium (11-20), and longer (21-25) sentences
6. **Use Subheadings**: Break content into scannable sections
7. **Add Lists**: Convert dense paragraphs into bullet/numbered lists where appropriate

CONSTRAINTS:
- Maintain all facts and data accurately
- Preserve all source citations
- Keep technical terms if necessary (but explain them)
- Don't oversimplify complex topics

OUTPUT FORMAT (JSON):
{{
    "improved_content": "... [rewritten content] ...",
    "readability_improvements": {{
        "new_flesch_score": 68,
        "new_avg_sentence_length": 18,
        "sentences_split": 5,
        "passive_to_active_conversions": 8,
        "complex_words_simplified": 12
    }},
    "specific_changes": [
        {{
            "original": "The implementation of AI-driven diagnostic systems has facilitated...",
            "improved": "AI diagnostic systems have made it easier to...",
            "improvement": "Simplified vocabulary + active voice"
        }}
    ]
}}""")
])

# ============================================================================
# KEYWORD DENSITY ANALYZER
# ============================================================================

KEYWORD_DENSITY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a keyword density analyzer. Calculate precise keyword metrics for SEO optimization."""),
    ("human", """Analyze keyword usage in this content:

CONTENT:
{content}

PRIMARY KEYWORD: {primary_keyword}
SECONDARY KEYWORDS: {secondary_keywords}

Calculate:
1. **Primary Keyword Metrics**:
   - Total occurrences
   - Density percentage (occurrences / total words * 100)
   - Locations (which paragraphs/sections)
   - Variations found (plurals, synonyms)

2. **Secondary Keywords**:
   - Occurrences of each
   - Natural integration score

3. **Related Terms (LSI)**:
   - Semantically related terms found
   - Coverage score

4. **Keyword Distribution**:
   - In title?
   - In first 100 words?
   - In headings?
   - In last paragraph (conclusion)?
   - Even distribution or clustered?

OUTPUT FORMAT (JSON):
{{
    "primary_keyword": {{
        "keyword": "{primary_keyword}",
        "occurrences": 8,
        "density": "1.5%",
        "ideal_range": "1-2%",
        "status": "optimal/under-optimized/over-optimized",
        "locations": ["title", "paragraph_1", "paragraph_5", "heading_2", "conclusion"],
        "variations_found": ["...", "..."]
    }},
    "secondary_keywords": [
        {{
            "keyword": "...",
            "occurrences": 3,
            "density": "0.5%",
            "status": "good"
        }}
    ],
    "lsi_keywords_found": [
        "...", "...", "..."
    ],
    "distribution_analysis": {{
        "in_title": true,
        "in_first_100_words": true,
        "in_headings": true,
        "in_conclusion": true,
        "distribution_score": 90,
        "clustering_issues": false
    }},
    "recommendations": [
        "Add 1-2 more instances of primary keyword in middle sections",
        "Good natural integration - no keyword stuffing detected"
    ]
}}""")
])
