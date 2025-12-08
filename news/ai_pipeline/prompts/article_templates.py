"""
Article Generation Prompt Templates

Task 2.4: Prompt Templates Implementation
- SYSTEM_PROMPT (AI Analitica mission-aligned)
- ARTICLE_TEMPLATE (news generation)
- RESEARCH_TEMPLATE
- OUTLINE_TEMPLATE

CRITICAL: All prompts must emphasize:
- Objectivity and neutrality
- Data-driven reporting
- Multi-perspective coverage
- Fact-based journalism
- Source transparency
"""

from langchain.prompts import PromptTemplate, ChatPromptTemplate

# ============================================================================
# SYSTEM PROMPT - AI Analitica Mission-Aligned
# ============================================================================

SYSTEM_PROMPT = """You are an AI journalist working for AI Analitica, a news platform committed to:

🎯 CORE MISSION:
- Unbiased, data-driven news analysis
- Multi-perspective coverage of every story
- Fact-based reporting with transparent sourcing
- Objectivity over sensationalism
- Empowering readers with comprehensive information

📋 QUALITY STANDARDS:
- Bias Score: Must be < 20% (strictly neutral language)
- Fact Verification: > 80% of claims must have citations
- Perspective Coverage: Include at least 2 different viewpoints
- Plagiarism: < 5% (original writing, proper attribution)
- SEO Score: > 75% (discoverable without clickbait)

✍️ WRITING GUIDELINES:
1. Use neutral, factual language (avoid emotionally charged words)
2. Present all sides of controversial topics equally
3. Cite credible sources for all factual claims
4. Distinguish between facts and opinions clearly
5. Include relevant data, statistics, and expert quotes
6. Maintain professional, informative tone
7. Structure content for readability (headings, short paragraphs)
8. Focus on "what happened" before "why it matters"

🚫 AVOID:
- Political bias or partisanship
- Sensational headlines
- One-sided narratives
- Uncited opinions presented as facts
- Inflammatory language
- Speculation without labeling it as such

Remember: Your goal is to inform, not persuade. Readers should be able to form their own opinions based on comprehensive, balanced information."""

# ============================================================================
# RESEARCH TEMPLATE
# ============================================================================

RESEARCH_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", """Conduct comprehensive research on the following topic:

TOPIC: {keyword}
TARGET AUDIENCE: {audience}
REQUIRED DEPTH: {depth}

Your task is to gather:
1. **Key Facts**: Core information, dates, people, events
2. **Multiple Perspectives**: At least 2-3 different viewpoints on the topic
3. **Credible Sources**: Identify authoritative sources for each claim
4. **Data Points**: Statistics, studies, reports relevant to the topic
5. **Context**: Historical background, related events, implications
6. **Controversies**: Any debates or disagreements about the topic

OUTPUT FORMAT (JSON):
{{
    "key_facts": [
        {{"fact": "...", "source": "...", "credibility": "high/medium/low"}}
    ],
    "perspectives": [
        {{"viewpoint": "...", "supporting_evidence": "...", "sources": [...]}}
    ],
    "data_points": [
        {{"statistic": "...", "source": "...", "date": "..."}}
    ],
    "context": "...",
    "controversies": [...],
    "recommended_sources": [
        {{"name": "...", "url": "...", "credibility": "...", "perspective": "..."}}
    ]
}}

Focus on: {focus_angle}""")
])

# ============================================================================
# OUTLINE TEMPLATE
# ============================================================================

OUTLINE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", """Create a detailed outline for a news article based on this research:

TOPIC: {keyword}
TEMPLATE TYPE: {template_type}
TARGET WORD COUNT: {word_count}
RESEARCH DATA: {research_summary}

Your outline should include:
1. **Headline** (factual, not clickbait, 50-70 characters)
2. **Lead Paragraph** (Who, What, When, Where, Why - first 50 words)
3. **Main Sections** (3-5 sections with clear headings)
4. **Key Points per Section** (what facts, quotes, data to include)
5. **Perspective Balance** (ensure multiple viewpoints)
6. **Source Integration** (where to cite which sources)
7. **Data Visualization Opportunities** (charts, stats to highlight)
8. **Call-outs or Sidebars** (context boxes, definitions, timelines)

TEMPLATE TYPE GUIDELINES:
- **breaking_news**: Focus on facts, timeline, immediate impact
- **analysis**: Deep dive into causes, implications, expert opinions
- **explainer**: Educational, define terms, provide context
- **data_driven**: Lead with statistics, visualize data, trend analysis
- **investigative**: Uncover details, connect dots, document trail

OUTPUT FORMAT (JSON):
{{
    "headline": "...",
    "subheadline": "...",
    "lead_paragraph": "...",
    "sections": [
        {{
            "heading": "...",
            "key_points": [...],
            "sources_to_cite": [...],
            "perspective": "neutral/viewpoint_A/viewpoint_B",
            "word_count_target": 200
        }}
    ],
    "data_visualizations": [...],
    "fact_check_priority": [...],
    "seo_keywords": [...]
}}""")
])

# ============================================================================
# ARTICLE GENERATION TEMPLATE
# ============================================================================

ARTICLE_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", """Write a complete news article following this outline:

OUTLINE: {outline}
RESEARCH DATA: {research_data}
TEMPLATE: {template_type}
TONE: {tone}
TARGET LENGTH: {word_count} words

WRITING REQUIREMENTS:
1. **Factual Accuracy**: Every claim must have a source
2. **Balanced Reporting**: Include multiple perspectives equally
3. **Clear Attribution**: Use "according to [source]" for all quotes/data
4. **Neutral Language**: Avoid bias indicators (amazing, terrible, shockingly, etc.)
5. **Structured Content**: Use headings (##), subheadings (###), bullet points
6. **Readability**: Short paragraphs (3-4 sentences), vary sentence length
7. **SEO Optimization**: Natural keyword inclusion, descriptive headings
8. **Engagement**: Lead with most important info, maintain reader interest

MARKDOWN FORMAT:
- Use ## for main section headings
- Use ### for subheadings
- Use **bold** for emphasis (sparingly)
- Use > for quotes
- Use bullet points or numbered lists for clarity
- Include [Source Name](URL) for citations (inline or footnotes)

EXAMPLE STRUCTURE:
```markdown
## [Section Heading]

[Opening paragraph with key fact and citation]

According to [Expert Name], [Professor at University], "[quote that adds credibility and perspective]" ([Source](URL)).

[Additional context paragraph with data]

### [Subheading for deeper detail]

[Paragraph exploring different angle]

> "[Contrasting quote from different perspective]" 
> — [Different Expert], [Credentials]

[Paragraph presenting data]

A recent study by [Organization] found that [statistic] ([Source](URL)). This represents [context/significance].

**Key Takeaways:**
- [Factual point 1]
- [Factual point 2]
- [Factual point 3]
```

NOW WRITE THE ARTICLE:""")
])

# ============================================================================
# TEMPLATE-SPECIFIC VARIATIONS
# ============================================================================

BREAKING_NEWS_TEMPLATE = """Focus on:
- What happened (facts only)
- When and where
- Who is involved
- Immediate consequences
- Official statements
- What's known vs. unknown (clearly distinguish)
- Expected updates

Keep sentences short and direct. Lead with the most newsworthy element."""

ANALYSIS_TEMPLATE = """Focus on:
- Context and background
- Why this matters now
- Multiple expert perspectives
- Historical precedents
- Possible implications
- Unanswered questions
- What to watch for next

Balance depth with readability. Use examples to illustrate complex points."""

EXPLAINER_TEMPLATE = """Focus on:
- Define key terms simply
- Explain the "why" and "how"
- Use analogies for complex concepts
- Address common misconceptions
- Provide historical context
- Connect to reader's life
- FAQ format for key questions

Educate without condescending. Assume intelligent but unfamiliar reader."""

DATA_DRIVEN_TEMPLATE = """Focus on:
- Lead with the most striking data point
- Visualize trends and patterns
- Compare multiple data sources
- Explain methodology
- Highlight outliers or surprises
- Put numbers in context (comparisons, historical)
- Note data limitations

Make statistics accessible. Use "1 in 5 people" rather than "20% of the population"."""

INVESTIGATIVE_TEMPLATE = """Focus on:
- Document trail (what evidence exists)
- Timeline of events
- Key players and relationships
- What documents/records show
- Discrepancies or red flags
- Official vs. reality
- What questions remain

Present findings methodically. Let evidence speak. Note what couldn't be verified."""

# ============================================================================
# Template Selection Helper
# ============================================================================

TEMPLATE_MAP = {
    'breaking_news': BREAKING_NEWS_TEMPLATE,
    'analysis': ANALYSIS_TEMPLATE,
    'explainer': EXPLAINER_TEMPLATE,
    'data_driven': DATA_DRIVEN_TEMPLATE,
    'investigative': INVESTIGATIVE_TEMPLATE,
}

def get_template_guidance(template_type: str) -> str:
    """Get specific guidance for article template type."""
    return TEMPLATE_MAP.get(template_type, ANALYSIS_TEMPLATE)
