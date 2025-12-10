"""
SEO Optimization Prompt Templates

Educational Content SEO Focused on Nepal
Optimized for Google ranking and student discoverability
"""

from langchain_core.prompts import ChatPromptTemplate

# ============================================================================
# SEO ANALYSIS PROMPT
# ============================================================================

SEO_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert SEO analyst specializing in educational content optimization for the Nepali market.
Your analysis must be thorough, actionable, and focused on improving search visibility for students in Nepal."""),
    ("human", """Perform a comprehensive SEO analysis of this educational blog article:

ARTICLE DATA:
- Title: {title}
- Meta Description: {meta_description}
- URL Slug: {slug}
- Word Count: {word_count}
- Primary Keyword: {primary_keyword}
- Target Audience: Students in Nepal
- Category: {category}

CONTENT:
{content}

Analyze the following aspects and provide scores (0-100):

1. **KEYWORD OPTIMIZATION** (0-100)
   - Primary keyword in title (first 60 chars)? (Yes +20)
   - Keyword in first 100 words? (Yes +20)
   - Keyword density (1-2% is ideal) (+20)
   - Keyword in at least one H2 heading? (Yes +15)
   - LSI/related keywords present (+15)
   - Natural integration (not keyword stuffing) (+10)

2. **ON-PAGE SEO** (0-100)
   - Title tag length (50-60 chars ideal) (+15)
   - Title compelling for students? (+10)
   - Meta description length (120-155 chars ideal) (+15)
   - Meta description includes keyword + CTA? (+10)
   - URL structure (short, keyword-rich) (+10)
   - Heading hierarchy (H1 → H2 → H3) proper (+15)
   - Internal linking opportunities identified (+15)
   - Content uniqueness and value (+10)

3. **CONTENT QUALITY FOR STUDENTS** (0-100)
   - Word count (600-2500 words, sweet spot 1200-1800) (+20)
   - Nepal-specific examples included? (+15)
   - Practical, actionable advice for students? (+15)
   - Addresses common student questions? (+10)
   - Clear explanations (not too technical)? (+15)
   - Step-by-step guides where appropriate? (+15)
   - Engaging and motivational tone? (+10)

4. **READABILITY FOR STUDENTS** (0-100)
   - Reading level: Grade 8-10 (appropriate for students) (+25)
   - Average sentence length (12-20 words) (+20)
   - Short paragraphs (2-4 sentences) (+15)
   - Use of bullet points and lists (+15)
   - Clear subheadings for scannability (+15)
   - Conversational "you" language (+10)

5. **USER ENGAGEMENT SIGNALS** (0-100)
   - Engaging introduction (relatable hook) (+20)
   - Clear value proposition for students (+20)
   - Logical flow and structure (+15)
   - FAQ section included? (+10)
   - Strong conclusion with CTA (+15)
   - Encouraging/motivational elements (+10)
   - Estimated time-on-page potential (+10)

6. **NEPAL-SPECIFIC SEO** (0-100)
   - Nepal context included? (+25)
   - Local examples (colleges, exams, opportunities)? (+20)
   - Addresses challenges of Nepali students? (+15)
   - Mentions relevant Nepali institutions? (+15)
   - Local keywords and phrases used? (+15)
   - Available resources in Nepal mentioned? (+10)

7. **TECHNICAL SEO INDICATORS** (0-100)
   - URL length (<75 characters) (+15)
   - URL includes keyword (+15)
   - Mobile-friendly formatting (+20)
   - Schema markup potential (Article, FAQ) (+15)
   - Social sharing optimization (+15)
   - Featured snippet opportunities (+10)
   - Image optimization (if images present) (+10)

OUTPUT FORMAT (JSON):
{{
    "overall_seo_score": 85,
    "seo_grade": "A",
    "scores": {{
        "keyword_optimization": 90,
        "on_page_seo": 85,
        "content_quality": 88,
        "readability": 92,
        "user_engagement": 87,
        "nepal_specific": 80,
        "technical_seo": 85
    }},
    "keyword_analysis": {{
        "primary_keyword_in_title": true,
        "keyword_position_in_title": 0,
        "primary_keyword_in_first_100_words": true,
        "keyword_density": "1.5%",
        "keyword_count": 12,
        "target_keyword_count": "10-14",
        "keyword_in_h2": true,
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
    ("system", """You are an SEO content optimizer specializing in educational blog content for students in Nepal.
Your goal is to improve articles for better Google ranking and student discoverability while maintaining educational value and accuracy.

CRITICAL RULES FOR EDUCATIONAL CONTENT:
- Never sacrifice factual accuracy for SEO (students trust this information)
- Never add keywords unnaturally (maintain conversational, student-friendly tone)
- Maintain educational integrity and helpfulness
- Preserve all facts, data, and accurate information
- Keep encouraging and motivational tone for students
- Only suggest changes that improve BOTH SEO AND student learning experience
- Nepal context must feel natural, not forced
- Focus on practical, actionable advice students can use"""),
    ("human", """Optimize this educational blog article based on the SEO analysis:

ORIGINAL ARTICLE:
{content}

SEO ANALYSIS RESULTS:
{analysis_results}

PRIMARY KEYWORD: {primary_keyword}
SECONDARY KEYWORDS: {secondary_keywords}
TARGET AUDIENCE: Students in Nepal (high school, college, aspiring professionals)

IMPROVEMENTS NEEDED:
{improvement_areas}

Your optimization tasks:
1. **Keyword Optimization**: Naturally integrate primary keyword in:
   - Title (first 60 characters)
   - First 100 words of content
   - At least one H2 heading
   - Maintain 1-2% keyword density throughout

2. **Content Structure**: Improve heading hierarchy and scannability for students

3. **Readability**: Enhance clarity for student comprehension (Grade 8-10 level)

4. **Student Engagement**: Add motivational elements, relatable examples, practical tips

5. **Nepal Context**: Weave in relevant Nepal-specific examples (colleges, exams, opportunities)

6. **Meta Tags**: Optimize title and description for student search intent

7. **Featured Snippets**: Structure content to win snippet positions (FAQ, How-to, Lists)

SPECIFIC FOCUS AREAS:
- **Title Optimization**: {title_feedback}
- **Meta Description**: {meta_feedback}
- **Keyword Integration**: {keyword_feedback}
- **Content Structure**: {structure_feedback}

OUTPUT FORMAT (JSON):
{{
    "optimized_title": "Primary Keyword in First 60 Chars | Student-Friendly",
    "optimized_meta_description": "120-155 char description with keyword + value prop + CTA for students",
    "optimized_content": "... [full article text with SEO improvements, Nepal context, student engagement] ...",
    "suggested_url_slug": "primary-keyword-short-descriptive",
    "changes_made": [
        {{
            "section": "Title",
            "original": "Old title without keyword",
            "improved": "Primary Keyword: Comprehensive Guide for Nepali Students",
            "reason": "Added primary keyword at beginning + student audience specification"
        }},
        {{
            "section": "First paragraph",
            "original": "Generic opening without keyword",
            "improved": "Para with keyword in first 2 sentences + Nepal context + student hook",
            "reason": "Integrated primary keyword naturally + relatable Nepal example + engaged students"
        }},
        {{
            "section": "H2 Heading 1",
            "original": "Generic heading",
            "improved": "Heading with primary/LSI keyword + student value",
            "reason": "Better SEO + clearer student benefit"
        }}
    ],
    "keyword_placements": {{
        "primary_keyword_count": 10,
        "primary_keyword_density": "1.5%",
        "primary_keyword_locations": ["title_position_0", "first_100_words", "h2_heading_1", "h2_heading_3", "conclusion"],
        "secondary_keywords_integrated": ["related term 1", "related term 2"],
        "lsi_keywords_added": ["LSI keyword 1", "LSI keyword 2", "LSI keyword 3"],
        "nepal_keywords_added": ["SEE exam", "TU colleges", "IOE entrance"]
    }},
    "structural_improvements": [
        "Added H2 heading: 'How to [Primary Keyword] in Nepal: Step-by-Step Guide'",
        "Split long explanation (10 sentences) into scannable sections with H3 subheadings",
        "Created numbered list for actionable steps (better readability + snippet potential)",
        "Added FAQ section at end (6 common student questions with concise answers)",
        "Inserted motivational callout box after challenging section"
    ],
    "nepal_context_additions": [
        "Example: How Tribhuvan University students approach [topic]",
        "Reference to Nepal education system: SEE, +2, Bachelor's pathway",
        "Mention of challenges specific to Nepali students (limited resources, exam pressure)",
        "Link to available opportunities in Nepal (scholarships, programs, institutions)"
    ],
    "student_engagement_elements": [
        "Relatable hook: 'If you're a student in Nepal feeling overwhelmed by...'",
        "Encouraging language: 'You've got this!' 'It's easier than you think'",
        "Practical tips: 'Here's exactly what you need to do...'",
        "Real success story: Brief example of Nepali student who succeeded",
        "Clear next steps: What to do after reading this article"
    ],
    "linking_suggestions": [
        {{
            "anchor_text": "preparing for IOE entrance exam",
            "target_url": "internal",
            "placement": "After paragraph 3",
            "purpose": "Link to related IOE exam guide for deeper learning"
        }},
        {{
            "anchor_text": "top engineering colleges in Nepal",
            "target_url": "internal",
            "placement": "In college selection section",
            "purpose": "Provide resource list for students"
        }}
    ],
    "featured_snippet_optimization": {{
        "target_query": "[Primary Keyword] in Nepal",
        "snippet_type": "numbered_list",
        "optimized_section": "Created '5 Steps to [Primary Keyword]' section with clear, concise steps (40-60 words each)"
    }},
    "readability_improvements": [
        "Reduced average sentence length from 22 to 16 words",
        "Used simpler vocabulary (replaced 'utilize' with 'use', 'endeavor' with 'try')",
        "Added transition words for better flow (However, Additionally, For example)",
        "Broke up dense paragraphs into 2-3 sentence chunks"
    ],
    "estimated_seo_improvement": "+15 points",
    "new_seo_score": 88,
    "student_value_score": "9/10"
}}

Optimize NOW:""")
])

# ============================================================================
# READABILITY IMPROVEMENT PROMPT
# ============================================================================

READABILITY_IMPROVEMENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a readability expert specializing in educational content for students.
Your goal is to make content more accessible and engaging for students (Grade 8-10 reading level) while preserving educational value and accuracy."""),
    ("human", """Improve the readability of this educational content for students in Nepal:

CURRENT TEXT:
{content}

READABILITY ISSUES DETECTED:
- Flesch Reading Ease: {flesch_score} (target: 60-70 for students)
- Average Sentence Length: {avg_sentence_length} words (target: 12-20)
- Complex Words: {complex_word_percentage}% (target: <12% for students)
- Passive Voice: {passive_voice_percentage}% (target: <8%)

IMPROVEMENT STRATEGIES FOR STUDENTS:
1. **Break Long Sentences**: Split sentences >20 words into shorter, digestible chunks
2. **Simplify Vocabulary**: Use student-friendly language (replace jargon, explain technical terms)
3. **Active Voice**: Students engage better with active constructions ("You can do X" vs "X can be done")
4. **Add Transitions**: Improve flow with words students know (However, Next, For example, Additionally)
5. **Vary Sentence Length**: Mix short (5-10), medium (11-18), occasional longer (19-22) sentences
6. **Use Subheadings**: Break content into clear, scannable sections with "you" language
7. **Add Lists**: Convert dense explanations into numbered steps or bullet points
8. **Use "You" Language**: Direct address makes content more engaging for students

STUDENT-SPECIFIC CONSTRAINTS:
- Maintain all facts and educational accuracy (students trust this information)
- Preserve all data, examples, and practical tips
- Keep technical terms if necessary BUT explain them simply
- Don't oversimplify complex topics, but make them understandable
- Add relatable examples for Nepali students where possible
- Maintain encouraging, motivational tone

OUTPUT FORMAT (JSON):
{{
    "improved_content": "... [rewritten content with student-friendly readability] ...",
    "readability_improvements": {{
        "new_flesch_score": 68,
        "new_avg_sentence_length": 16,
        "sentences_split": 7,
        "passive_to_active_conversions": 10,
        "complex_words_simplified": 15,
        "technical_terms_explained": 5
    }},
    "specific_changes": [
        {{
            "original": "The utilization of mnemonic devices facilitates enhanced retention...",
            "improved": "Using memory tricks helps you remember things better. For example, you can...",
            "improvement": "Simplified vocabulary + active voice + student-friendly explanation + practical example"
        }},
        {{
            "original": "It is recommended that students allocate sufficient time...",
            "improved": "You should set aside enough time to...",
            "explanation": "Passive to active voice + direct 'you' address for better student engagement"
        }}
    ],
    "student_engagement_additions": [
        "Added relatable example: 'Just like preparing for your SEE exam...'",
        "Inserted encouraging phrase: 'Don't worry, this is easier than it seems!'",
        "Included practical tip: 'Here's exactly how you can do this...'"
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
