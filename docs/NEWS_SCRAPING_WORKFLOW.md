# News Scraping & Content Generation Workflow

## Overview

This document describes the two-phase workflow for AI content generation based on news scraping.

## Phase 1: Setup Keywords & News Sources

**Purpose**: Define what topics you want to cover and which news websites to scrape from.

### Database Model: `NewsSourceConfig`

Configure your content research parameters:

- **Name**: Configuration name (e.g., "Tech News - Daily")
- **Keywords**: List of topics/keywords to search for
  - Example: ["artificial intelligence", "machine learning", "ChatGPT"]
- **Source Websites**: List of news site URLs to scrape
  - Example: ["https://techcrunch.com", "https://theverge.com"]
- **Category**: Content category (Politics, Technology, Business, etc.)
- **Max Articles**: How many articles to scrape per run
- **Scrape Frequency**: How often to scrape (in hours)

### API Endpoints

```
POST   /api/admin/ai/news-sources/              - Create new config
GET    /api/admin/ai/news-sources/              - List all configs
GET    /api/admin/ai/news-sources/{id}/         - Get config details
PATCH  /api/admin/ai/news-sources/{id}/         - Update config
DELETE /api/admin/ai/news-sources/{id}/         - Delete config
POST   /api/admin/ai/news-sources/{id}/trigger_scrape/ - Manual scrape
```

### Example Configuration

```json
{
  "name": "AI & Tech News Daily",
  "keywords": [
    "artificial intelligence",
    "machine learning",
    "tech startups",
    "cryptocurrency"
  ],
  "source_websites": [
    "https://techcrunch.com",
    "https://www.theverge.com",
    "https://arstechnica.com"
  ],
  "category": "Technology",
  "max_articles_per_scrape": 20,
  "scrape_frequency_hours": 24,
  "status": "active"
}
```

## Phase 2: Scrape & Review Articles

**Purpose**: Scrape articles from configured sources, review them, and approve for AI generation.

### Database Model: `ScrapedArticle`

Articles scraped from news websites contain:

- **Title**: Article headline
- **Content**: Full article text
- **Summary**: Brief summary (if available)
- **Source URL**: Original article URL
- **Source Website**: Website domain
- **Author**: Article author
- **Published Date**: When it was published
- **Matched Keywords**: Which keywords matched this article
- **Image URLs**: All images found in article
- **Reference URLs**: Links/citations from article
- **Category**: Article category
- **Status**: pending → approved → generated

### Workflow Steps

#### 1. Scraping Process

When scraping is triggered (manually or by schedule):

1. System reads `NewsSourceConfig`
2. For each keyword + website combination:
   - Searches website for keyword
   - Extracts article metadata:
     - Title
     - Content
     - Images
     - References
     - Author
     - Date
3. Saves to `ScrapedArticle` with status="pending"

#### 2. Review & Approval

Admin reviews scraped articles:

```
GET /api/admin/ai/scraped-articles/?status=pending
```

For each article, admin can:

**Approve**: Send to AI generation pipeline
```
POST /api/admin/ai/scraped-articles/{id}/approve/
Body: {"auto_generate": true}
```

What happens:
1. Article status → "approved"
2. Creates `KeywordSource` from article title
3. Creates `AIArticle` for generation pipeline
4. Links scraped article to AI article
5. Optionally triggers Celery task for generation

**Reject**: Mark as not relevant
```
POST /api/admin/ai/scraped-articles/{id}/reject/
Body: {"reason": "Not relevant to our audience"}
```

**Bulk Approve**: Approve multiple articles at once
```
POST /api/admin/ai/scraped-articles/bulk_approve/
Body: {
  "article_ids": ["uuid1", "uuid2", "uuid3"],
  "auto_generate": true
}
```

### API Endpoints

```
GET    /api/admin/ai/scraped-articles/              - List scraped articles
GET    /api/admin/ai/scraped-articles/{id}/         - Get article details
POST   /api/admin/ai/scraped-articles/{id}/approve/ - Approve for generation
POST   /api/admin/ai/scraped-articles/{id}/reject/  - Reject article
POST   /api/admin/ai/scraped-articles/bulk_approve/ - Bulk approve
DELETE /api/admin/ai/scraped-articles/{id}/         - Delete article
```

### Filtering & Search

```
# Filter by status
GET /api/admin/ai/scraped-articles/?status=pending
GET /api/admin/ai/scraped-articles/?status=approved
GET /api/admin/ai/scraped-articles/?status=rejected

# Filter by category
GET /api/admin/ai/scraped-articles/?category=Technology

# Filter by source config
GET /api/admin/ai/scraped-articles/?source_config={config_id}

# Search in title/content
GET /api/admin/ai/scraped-articles/?search=artificial+intelligence
```

## Integration with AI Generation Pipeline

When a scraped article is approved:

1. **Keyword Source Created**
   ```python
   keyword = KeywordSource.objects.create(
       keyword=article.title,
       source='scraper',
       category=article.category,
       status='approved',
       source_url=article.source_url,
       notes=f'From scraped article: {article.source_url}'
   )
   ```

2. **AI Article Queued**
   ```python
   ai_article = AIArticle.objects.create(
       keyword=keyword,
       status='queued',
       template_type='news_report',
       source_reference=article.content[:1000],  # Use as context
       target_tone='professional'
   )
   ```

3. **Link Established**
   ```python
   article.ai_article = ai_article
   article.status = 'generated'
   article.save()
   ```

4. **Celery Task Triggered** (when implemented)
   ```python
   from .ai_tasks import generate_article_pipeline
   generate_article_pipeline.delay(str(ai_article.id))
   ```

## Complete Workflow Example

### Step 1: Create Source Configuration

```bash
POST /api/admin/ai/news-sources/

{
  "name": "Daily Tech News",
  "keywords": ["AI", "blockchain", "quantum computing"],
  "source_websites": [
    "https://techcrunch.com",
    "https://www.wired.com"
  ],
  "category": "Technology",
  "max_articles_per_scrape": 15,
  "scrape_frequency_hours": 12
}
```

### Step 2: Trigger Scraping

```bash
POST /api/admin/ai/news-sources/{config_id}/trigger_scrape/
```

System scrapes articles matching keywords from specified websites.

### Step 3: Review Scraped Articles

```bash
GET /api/admin/ai/scraped-articles/?status=pending

Response:
{
  "count": 12,
  "results": [
    {
      "id": "uuid-1",
      "title": "New AI Breakthrough in Natural Language Processing",
      "source_website": "techcrunch.com",
      "source_url": "https://techcrunch.com/2025/...",
      "matched_keywords": ["AI"],
      "category": "Technology",
      "scraped_at": "2025-12-08T10:30:00Z",
      "image_urls": ["https://...jpg", "https://...png"],
      "reference_urls": ["https://arxiv.org/..."]
    },
    ...
  ]
}
```

### Step 4: Approve Articles for Generation

```bash
# Single approval
POST /api/admin/ai/scraped-articles/uuid-1/approve/
{
  "auto_generate": true
}

# Bulk approval
POST /api/admin/ai/scraped-articles/bulk_approve/
{
  "article_ids": ["uuid-1", "uuid-2", "uuid-3"],
  "auto_generate": true
}
```

### Step 5: Monitor Generation

Articles move to AI generation pipeline:

```bash
GET /api/admin/ai/articles/?status=queued
GET /api/admin/ai/articles/?status=generating
GET /api/admin/ai/articles/?status=ready
```

## Data Flow Diagram

```
┌─────────────────────────┐
│ NewsSourceConfig        │
│ - Keywords              │
│ - Source Websites       │
│ - Category              │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Scraping Process        │
│ - Search keywords       │
│ - Extract content       │
│ - Get images/refs       │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ ScrapedArticle          │
│ status: pending         │
│ - Title                 │
│ - Content               │
│ - Images                │
│ - References            │
└───────────┬─────────────┘
            │
       Admin Review
            │
    ┌───────┴───────┐
    │               │
 Approve         Reject
    │               │
    ▼               ▼
┌─────────┐    [Rejected]
│KeywordSource│
└─────┬───┘
      │
      ▼
┌─────────────┐
│ AIArticle   │
│ status:queued│
└─────┬───────┘
      │
      ▼
┌─────────────────┐
│ Generation      │
│ Pipeline        │
│ (LangChain)     │
└─────┬───────────┘
      │
      ▼
┌─────────────────┐
│ Published News  │
└─────────────────┘
```

## Database Schema

### news_newssourceconfig
- id (UUID, PK)
- name (VARCHAR)
- keywords (JSON array)
- source_websites (JSON array)
- category (VARCHAR)
- max_articles_per_scrape (INT)
- scrape_frequency_hours (INT)
- status (VARCHAR: active/paused/disabled)
- notes (TEXT)
- created_by_id (FK → User)
- created_at (DATETIME)
- updated_at (DATETIME)
- last_scraped_at (DATETIME, nullable)

### news_scrapedarticle
- id (UUID, PK)
- source_config_id (FK → NewsSourceConfig)
- title (VARCHAR 500)
- content (TEXT)
- summary (TEXT)
- source_url (VARCHAR 1000)
- source_website (VARCHAR)
- author (VARCHAR)
- published_date (DATETIME, nullable)
- matched_keywords (JSON array)
- image_urls (JSON array)
- reference_urls (JSON array)
- category (VARCHAR)
- tags (JSON array)
- status (VARCHAR: pending/approved/rejected/generated)
- reviewed_by_id (FK → User, nullable)
- reviewed_at (DATETIME, nullable)
- rejection_reason (TEXT)
- ai_article_id (FK → AIArticle, nullable)
- scraped_at (DATETIME)
- updated_at (DATETIME)

## Status Transitions

### NewsSourceConfig
```
active → paused → active
active → disabled
```

### ScrapedArticle
```
pending → approved → generated
pending → rejected
```

## Frontend Integration

The frontend Keywords page now has:

1. **Manual Topic Entry Tab**
   - Add keywords manually
   - Specify reference URLs
   - Select category
   - Set priority

2. **Scrape from URLs Tab**
   - Enter news article URLs
   - System extracts topics automatically
   - Creates pending keywords for review

Both feed into the same review/approval workflow.

## Next Steps

1. **Implement Web Scraping**
   - Beautiful Soup or Scrapy for HTML parsing
   - Newspaper3k for article extraction
   - Respect robots.txt and rate limits

2. **Schedule Automated Scraping**
   - Celery Beat for periodic tasks
   - Based on `scrape_frequency_hours`

3. **Enhanced Matching**
   - NLP for better keyword matching
   - Sentiment analysis
   - Topic modeling

4. **Content Deduplication**
   - Check for similar articles
   - Prevent duplicate content generation

## API Authentication

All endpoints require admin authentication:

```bash
# Get CSRF token
GET /api/admin/auth/csrf/

# Login
POST /api/admin/auth/login/
{
  "username": "admin",
  "password": "password"
}

# Make authenticated requests
GET /api/admin/ai/news-sources/
Header: X-CSRFToken: {token}
Cookie: sessionid={session}
```

## Error Handling

### Common Errors

**403 Forbidden**
- User not authenticated or not admin
- Solution: Login with admin credentials

**400 Bad Request**
- Missing required fields
- Invalid data format
- Solution: Check request body matches expected schema

**404 Not Found**
- Resource doesn't exist
- Wrong URL or deleted resource

**500 Internal Server Error**
- Server-side error
- Check Django logs

## Performance Considerations

1. **Pagination**: All list endpoints support pagination
   ```
   GET /api/admin/ai/scraped-articles/?page=2&page_size=20
   ```

2. **Filtering**: Use filters to reduce data transfer
   ```
   GET /api/admin/ai/scraped-articles/?status=pending&category=Technology
   ```

3. **Selective Fields**: Request only needed fields
   ```
   GET /api/admin/ai/scraped-articles/?fields=id,title,status
   ```

4. **Caching**: Consider caching frequently accessed configs

5. **Async Processing**: Use Celery for scraping to avoid timeouts

## Security Best Practices

1. **Rate Limiting**: Respect source website rate limits
2. **User Agent**: Use identifiable user agent string
3. **robots.txt**: Always check and respect robots.txt
4. **Legal**: Ensure scraping complies with ToS and copyright
5. **Data Privacy**: Handle scraped data responsibly
6. **Authentication**: All endpoints require admin privileges
7. **CSRF Protection**: Use CSRF tokens for state-changing operations

## Monitoring & Logging

Track these metrics:

- Scraping success rate
- Articles per source
- Approval rate
- Generation success rate
- Processing time
- Errors and failures

## Conclusion

This two-phase workflow provides:

1. **Flexible Configuration**: Define what and where to scrape
2. **Quality Control**: Review before generation
3. **Full Traceability**: Link from source to published article
4. **Scalability**: Automated scraping with manual oversight
5. **Rich Context**: Use scraped content to enhance AI generation

The system is now ready for:
- Manual keyword entry
- URL-based topic extraction  
- Full news article scraping (when scraping logic is implemented)
- Review and approval workflow
- Integration with AI generation pipeline
