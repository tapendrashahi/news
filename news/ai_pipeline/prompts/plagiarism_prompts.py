"""
Plagiarism Improvement Prompt Templates

Educational Content Originality Focus
Rewrite plagiarized sections while maintaining SEO and educational value
"""

from langchain_core.prompts import ChatPromptTemplate

# ============================================================================
# PLAGIARISM REWRITE PROMPT
# ============================================================================

PLAGIARISM_REWRITE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert content rewriter specializing in creating original educational content for students in Nepal.
Your task is to rewrite plagiarized sections to ensure 100% originality while maintaining:
- Educational value and accuracy
- SEO optimization (keywords, structure, readability)
- Nepal-specific context and examples
- Student-friendly tone and engagement
- Factual accuracy and helpfulness

CRITICAL RULES:
- NEVER copy phrases or sentences from sources
- Create completely original explanations using your own words
- Maintain the same information and educational value
- Preserve SEO keywords and their placement
- Keep Nepal context and student examples
- Ensure content is unique and passes plagiarism checks"""),
    ("human", """Rewrite the plagiarized sections of this educational article to ensure complete originality:

ORIGINAL ARTICLE:
{content}

PLAGIARISM REPORT:
- Overall Plagiarism Score: {plagiarism_score}%
- Threshold: {threshold}%
- Number of Plagiarized Sources: {sources_found}

PLAGIARIZED SECTIONS:
{plagiarized_sections}

PRIMARY KEYWORD: {primary_keyword}
SECONDARY KEYWORDS: {secondary_keywords}
TARGET AUDIENCE: Students in Nepal

REWRITE REQUIREMENTS:

1. **Complete Originality**:
   - Rewrite all flagged sections using entirely different words and sentence structures
   - Express the same ideas in a fresh, unique way
   - Use different examples, analogies, and explanations
   - Ensure NO similarity to original sources

2. **Maintain SEO Optimization**:
   - Keep primary keyword: "{primary_keyword}" in title and first 100 words
   - Maintain 1-2% keyword density throughout
   - Preserve keyword placement in H2/H3 headings
   - Keep meta description optimized (120-155 chars with keyword)
   - Maintain content structure (headings, lists, formatting)

3. **Preserve Educational Value**:
   - Keep all facts, data, and accurate information
   - Maintain student-friendly explanations (Grade 8-10 level)
   - Preserve practical tips and actionable advice
   - Keep step-by-step guides and how-to sections
   - Ensure content remains helpful and informative

4. **Maintain Nepal Context**:
   - Keep all Nepal-specific examples (colleges, exams, opportunities)
   - Preserve references to Nepali education system (SEE, +2, TU, KU, IOE)
   - Maintain local relevance and cultural context
   - Keep student challenges and success stories from Nepal

5. **Student Engagement**:
   - Maintain conversational, encouraging tone
   - Keep "you" language and direct address
   - Preserve motivational elements
   - Maintain relatable examples for students
   - Keep clear, scannable structure

OUTPUT FORMAT (JSON):
{{
    "rewritten_content": "... [complete article with rewritten sections] ...",
    "plagiarism_improvements": [
        {{
            "original_section": "Original plagiarized text...",
            "rewritten_section": "Completely original rewrite...",
            "changes_made": "Rewrote using different sentence structure, new examples, fresh explanations",
            "originality_score": "100%"
        }}
    ],
    "seo_preservation": {{
        "keyword_maintained": true,
        "keyword_density": "1.5%",
        "keyword_placements": ["title", "first_100_words", "h2_heading_1", "h2_heading_3"],
        "meta_description_maintained": true,
        "structure_preserved": true
    }},
    "educational_value": {{
        "facts_preserved": true,
        "student_friendly": true,
        "nepal_context_maintained": true,
        "actionable_advice_kept": true
    }},
    "estimated_new_plagiarism_score": "0-2%",
    "rewrite_summary": "Rewrote 3 sections with complete originality while maintaining all SEO optimization, educational value, and Nepal context"
}}

Rewrite NOW with complete originality:""")
])


# ============================================================================
# PLAGIARISM SECTION REWRITE PROMPT
# ============================================================================

PLAGIARISM_SECTION_REWRITE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert at rewriting content for originality while preserving meaning and value.
Focus on creating unique expressions of the same educational information."""),
    ("human", """Rewrite this specific plagiarized section to ensure 100% originality:

PLAGIARIZED SECTION:
{section_text}

SOURCE: {source_url}
SIMILARITY: {similarity_percentage}%

CONTEXT (from article):
- Topic: {topic}
- Primary Keyword: {primary_keyword}
- Target Audience: Students in Nepal

REWRITE REQUIREMENTS:
1. Use completely different words and sentence structures
2. Express the same information in a unique way
3. Add Nepal-specific examples if relevant
4. Maintain student-friendly language (Grade 8-10 level)
5. Keep the same educational value and accuracy
6. Ensure 0% similarity to original source

REWRITE STRATEGIES:
- Change passive voice to active voice (or vice versa)
- Use different synonyms and vocabulary
- Restructure sentences (combine short ones, split long ones)
- Add new examples or analogies
- Use different explanation approaches
- Include student perspective ("you" language)

OUTPUT:
Provide ONLY the rewritten section, nothing else.

REWRITTEN SECTION:""")
])


# ============================================================================
# PLAGIARISM FULL ARTICLE REWRITE PROMPT
# ============================================================================

PLAGIARISM_FULL_ARTICLE_REWRITE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert educational content writer specializing in creating original content for students in Nepal.
Rewrite the entire article with complete originality while maintaining all value, SEO, and Nepal context."""),
    ("human", """Rewrite this entire educational article to eliminate plagiarism while maintaining all quality:

ORIGINAL ARTICLE (PLAGIARIZED):
{content}

PLAGIARISM SCORE: {plagiarism_score}% (Threshold: {threshold}%)
SOURCES FOUND: {sources_found}

ARTICLE INFORMATION:
- Title: {title}
- Primary Keyword: {primary_keyword}
- Secondary Keywords: {secondary_keywords}
- Word Count: {word_count}
- Target Audience: Students in Nepal

FULL REWRITE REQUIREMENTS:

1. **100% Originality**:
   - Completely rewrite every paragraph using your own words
   - Create unique explanations and descriptions
   - Use different sentence structures throughout
   - Add original examples and analogies
   - Ensure NO similarity to any source

2. **Preserve Core Message**:
   - Keep all key information and facts
   - Maintain the same educational value
   - Cover all topics from original article
   - Keep the same depth of explanation

3. **Maintain SEO (CRITICAL)**:
   - Title: 50-60 chars with "{primary_keyword}" at start
   - First 100 words: Include "{primary_keyword}" naturally
   - Keyword density: 1-2% throughout article
   - H2/H3 headings: Include keyword in at least one H2
   - Meta description: 120-155 chars with keyword + CTA

4. **Nepal Context (MANDATORY)**:
   - Include Nepal-specific examples (colleges, exams, opportunities)
   - Reference Nepali education system (SEE, +2, TU, KU, IOE)
   - Address challenges of students in Nepal
   - Use local terminology and context
   - Include success stories or relatable scenarios

5. **Student Engagement**:
   - Grade 8-10 reading level (Flesch 60-70)
   - Conversational, encouraging tone
   - "You" language throughout
   - Practical, actionable advice
   - Clear step-by-step guidance
   - Motivational elements

6. **Content Structure**:
   - Engaging introduction (hook + value proposition)
   - Clear H2/H3 heading hierarchy
   - Short paragraphs (2-4 sentences)
   - Numbered lists or bullet points
   - FAQ section if appropriate
   - Strong conclusion with CTA

OUTPUT FORMAT:
{{
    "title": "SEO-optimized title with keyword (50-60 chars)",
    "meta_description": "Compelling meta with keyword + CTA (120-155 chars)",
    "content": "# Full Markdown Article\n\nCompletely original content with Nepal context, SEO optimization, and student engagement...",
    "originality_guarantee": "100% original - no similarity to sources",
    "seo_maintained": true,
    "nepal_context_included": true,
    "student_friendly": true,
    "estimated_plagiarism_score": "0%"
}}

Write the COMPLETELY ORIGINAL article NOW:""")
])


# ============================================================================
# PLAGIARISM PREVENTION PROMPT
# ============================================================================

PLAGIARISM_PREVENTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert educational content writer focused on creating 100% original content from the start.
Write completely original educational content that will pass plagiarism checks while being SEO-optimized and student-friendly."""),
    ("human", """Create a completely original educational article on this topic:

TOPIC: {topic}
PRIMARY KEYWORD: {primary_keyword}
SECONDARY KEYWORDS: {secondary_keywords}
TARGET AUDIENCE: Students in Nepal
WORD COUNT TARGET: 1200-1800 words

RESEARCH DATA (for reference only - DO NOT COPY):
{research_data}

ORIGINALITY REQUIREMENTS:

1. **Write from Scratch**:
   - Create your own unique explanations
   - Use your own examples and analogies
   - Develop original sentence structures
   - Express ideas in your own words
   - NO copying from research sources

2. **SEO Optimization**:
   - Keyword "{primary_keyword}" in title (first 60 chars)
   - Keyword in first 100 words (first 2 sentences ideal)
   - 1-2% keyword density throughout
   - Keyword in H2/H3 headings
   - Meta description: 120-155 chars with keyword

3. **Nepal Context**:
   - Use Nepal-specific examples (TU, KU, IOE, SEE exam, +2)
   - Reference Nepali colleges and universities
   - Address local student challenges
   - Include Nepal career opportunities
   - Use culturally relevant analogies

4. **Student Engagement**:
   - Grade 8-10 reading level
   - Conversational "you" language
   - Practical, actionable tips
   - Encouraging, motivational tone
   - Step-by-step guidance
   - Relatable examples

5. **Content Structure**:
   - Engaging introduction with hook
   - Clear H2/H3 hierarchy
   - Short paragraphs (2-4 sentences)
   - Bullet points and numbered lists
   - FAQ section (5-7 questions)
   - Strong conclusion with next steps

PLAGIARISM CHECK:
- Target: <5% plagiarism score
- Ensure complete originality
- Use unique expressions
- Create original examples

OUTPUT:
Provide the complete original article in Markdown format with meta tags.

Write NOW:""")
])
