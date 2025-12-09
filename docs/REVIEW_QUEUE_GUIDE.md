# Review Queue Implementation

## Overview

The Review Queue is a comprehensive article review and publishing system that allows you to:
- View all AI-generated articles that are ready for review
- Review article quality metrics (SEO, bias, AI detection, plagiarism)
- Approve articles for publishing
- Reject articles with optional regeneration
- Publish approved articles to the live site

## How It Works

### Workflow States

1. **Reviewing** - Articles that completed all 15 pipeline stages and are ready for manual review
2. **Approved** - Articles that passed review and are ready to be published
3. **Published** - Articles that are live on the website
4. **Rejected** - Articles that failed review

### API Polling

The Review Queue automatically polls the API every 5 seconds to check for new articles and status updates. This ensures you always see the latest state without manual refresh.

### Features

#### 1. Article List (Left Panel)

- Shows all articles with status `reviewing` or `approved`
- Displays:
  - Article title
  - Status badge (blue for reviewing, green for approved)
  - Keyword used for generation
  - Creation timestamp
  - Word count
  - Quality score and SEO score badges (color-coded)
- Click any article to view details in the right panel

#### 2. Article Details (Right Panel)

**Article Information:**
- Keyword and category
- Word count
- AI model used (e.g., gemini-2.0-flash-exp)

**Quality Metrics:**
- Overall Quality Score (⭐)
- SEO Score (🎯)
- Bias Score (⚖️) - inverted display (lower is better)
- AI Detection Score (🤖) - inverted display (lower is better)
- Plagiarism Score (📋) - inverted display (lower is better)

Each metric shows:
- Icon and label
- Percentage value with color coding:
  - Green: 80%+ (excellent)
  - Yellow: 60-79% (good)
  - Red: <60% (needs improvement)
- Visual progress bar

**SEO Metadata:**
- Meta title
- Meta description
- Focus keywords (as tags)

**Content Preview/Full View:**
- Preview mode: First 300px of content with fade effect
- Full mode: Complete article content
- Toggle button to switch between views
- Properly formatted HTML rendering

#### 3. Review Actions

**For "Reviewing" Status:**
- ✓ Approve for Publishing
  - Changes status to `approved`
  - Marks you as reviewer
  - Adds timestamp
  - Shows success notification

- ✕ Reject Article
  - Opens modal for rejection notes (required)
  - Option to regenerate article automatically
  - Changes status to `rejected`
  - If regenerate is checked, creates new queued article

**For "Approved" Status:**
- 🚀 Publish to Live Site
  - Creates `News` object in database
  - Copies all content, metadata, and SEO fields
  - Sets author to current user
  - Links AI article to published article
  - Changes status to `published`
  - Shows success with article URL

## API Endpoints

### Get Review Queue
```
GET /api/admin/ai/articles/?status=reviewing
GET /api/admin/ai/articles/?status=approved
```

Returns articles ready for review or already approved.

### Approve Article
```
POST /api/admin/ai/articles/{id}/approve/
Body: { "notes": "Looks good" }
```

Changes status from `reviewing` to `approved`.

**Response:**
```json
{
  "detail": "Article approved.",
  "can_publish": true
}
```

### Reject Article
```
POST /api/admin/ai/articles/{id}/reject/
Body: { 
  "notes": "Needs more data",
  "regenerate": true
}
```

Changes status to `rejected`. If `regenerate=true`, creates new article.

**Response (with regeneration):**
```json
{
  "detail": "Article rejected. New generation started.",
  "new_article_id": "uuid-here"
}
```

**Response (without regeneration):**
```json
{
  "detail": "Article rejected."
}
```

### Publish Article
```
POST /api/admin/ai/articles/{id}/publish/
Body: { "visibility": "public" }
```

Publishes approved article to live site.

**Requirements:**
- Article must have status `approved`
- Article must not already be published

**Response:**
```json
{
  "detail": "Article published successfully.",
  "article_id": 123,
  "article_url": "/news/article-slug/"
}
```

## User Workflow

### Typical Review Process

1. **Access Review Queue**
   - Navigate to AI Content > Review Queue in admin menu
   - See list of articles ready for review

2. **Review Article**
   - Click on article in left panel
   - Review quality metrics (should be 60%+ for most metrics)
   - Check SEO metadata (title, description, keywords)
   - Read content preview or full content
   - Verify article meets quality standards

3. **Make Decision**

   **Option A: Approve**
   - Click "✓ Approve for Publishing"
   - Article moves to approved status
   - You can now publish it

   **Option B: Reject**
   - Click "✕ Reject Article"
   - Provide detailed rejection notes
   - Decide if you want automatic regeneration
   - If regenerate is checked, new article will be queued
   - If not, article is just marked rejected

4. **Publish (for approved articles)**
   - Click "🚀 Publish to Live Site"
   - Confirm the action
   - Article is published to website
   - Removed from review queue

## Quality Standards

### Recommended Thresholds

- **Overall Quality Score**: 70%+
- **SEO Score**: 80%+
- **Bias Score**: <30% (shown as 70%+ in UI due to inversion)
- **AI Detection Score**: <40% (shown as 60%+ in UI due to inversion)
- **Plagiarism Score**: <20% (shown as 80%+ in UI due to inversion)

### What to Check

1. **Content Quality**
   - Does the article make sense?
   - Is it factually accurate?
   - Does it match the keyword intent?
   - Is it well-structured?

2. **SEO Optimization**
   - Is the meta title compelling (50-60 chars)?
   - Is the meta description clear (150-160 chars)?
   - Are focus keywords relevant?

3. **Ethical Standards**
   - Is the content unbiased?
   - Does it present balanced perspectives?
   - Is it free from harmful content?

4. **Originality**
   - Is plagiarism score low?
   - Does it sound human-written?
   - Is it unique content?

## Frontend Components

### ReviewQueue.jsx
Main component that manages the review interface.

**Key Features:**
- Dual-panel layout (list + details)
- Real-time polling every 5 seconds
- Article selection state management
- Action handling (approve, reject, publish)
- Reject modal with notes input
- Content toggle (preview/full)

### QualityMetrics.jsx
Displays quality scores in a visual grid.

**Metrics:**
- Overall quality
- SEO score
- Bias score (inverted)
- AI detection (inverted)
- Plagiarism (inverted)

Each metric shows icon, label, percentage, and color-coded progress bar.

### Service Layer (aiContentService.js)

New functions added:
```javascript
approveArticle(id, notes)
rejectArticle(id, notes, regenerate = false)
publishArticle(id, visibility = 'public')
```

## Error Handling

### Common Errors

**"Article must be in review status"**
- Trying to approve article that's not in `reviewing` status
- Solution: Refresh the page, article may have changed status

**"Article must be approved before publishing"**
- Trying to publish article that's not in `approved` status
- Solution: Approve the article first

**"Article is already published"**
- Trying to publish article that's already live
- Solution: Check if article link exists, may be duplicate action

**"Rejection notes are required"**
- Trying to reject without providing notes
- Solution: Add detailed rejection reason

## Tips

1. **Batch Review**: Open multiple articles in new tabs to review faster
2. **Quality First**: Don't publish articles with low quality scores
3. **Detailed Rejections**: Provide specific notes so you understand why articles failed
4. **Regeneration**: Use regenerate option when article topic is good but execution is poor
5. **SEO Check**: Always verify meta title and description before publishing

## Troubleshooting

### Articles not appearing in Review Queue

Check:
- Are there articles with status `reviewing` or `approved`?
- Run query: `AIArticle.objects.filter(status__in=['reviewing', 'approved'])`
- Check if articles completed all 15 pipeline stages

### Can't approve article

Check:
- Is article status `reviewing`?
- Do you have permission to review?
- Check browser console for API errors

### Can't publish article

Check:
- Is article status `approved`?
- Has article been approved first?
- Is article already published? (check `published_article` field)

### Polling not working

- Check network tab in browser DevTools
- Verify API endpoints are responding
- Check for JavaScript errors in console
- Verify useEffect cleanup on component unmount

## Next Steps

After implementing Review Queue, consider:

1. **Bulk Actions**: Approve/reject multiple articles at once
2. **Filters**: Filter by quality score, category, keyword
3. **Search**: Search articles by title or content
4. **Revision Requests**: Add revision workflow instead of reject
5. **Scheduled Publishing**: Schedule approved articles for later
6. **Analytics**: Track approval rates, rejection reasons
7. **Notifications**: Email/push notifications for new reviews
8. **Comments**: Add review comments/feedback system
