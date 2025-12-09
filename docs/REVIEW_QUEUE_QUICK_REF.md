# Review Queue - Quick Reference

## Access
Navigate to: **AI Content > Review Queue**

## Status Flow
```
queued → generating → reviewing → approved → published
                          ↓
                      rejected
```

## Actions

### Approve Article
- **When**: Article status is `reviewing`
- **Action**: Click "✓ Approve for Publishing"
- **Result**: Status changes to `approved`
- **Next**: You can now publish it

### Reject Article
- **When**: Article status is `reviewing` or `approved`
- **Action**: Click "✕ Reject Article"
- **Required**: Rejection notes
- **Optional**: Check "Regenerate article" to create new version
- **Result**: Status changes to `rejected`

### Publish Article
- **When**: Article status is `approved`
- **Action**: Click "🚀 Publish to Live Site"
- **Result**: Article published to website, status changes to `published`
- **Note**: Cannot be undone easily

## Quality Metrics

| Metric | Icon | Good Score | Meaning |
|--------|------|------------|---------|
| Overall Quality | ⭐ | 70%+ | General article quality |
| SEO Score | 🎯 | 80%+ | Search engine optimization |
| Bias Score | ⚖️ | 70%+ (inverted) | Political/social neutrality |
| AI Detection | 🤖 | 60%+ (inverted) | How human-like it sounds |
| Plagiarism | 📋 | 80%+ (inverted) | Content originality |

**Note**: Inverted scores show better values higher (e.g., 10% plagiarism shows as 90%)

## Color Coding
- 🟢 Green: 80%+ (Excellent)
- 🟡 Yellow: 60-79% (Good)
- 🔴 Red: <60% (Needs Improvement)

## API Endpoints

```bash
# Get articles in review
GET /api/admin/ai/articles/?status=reviewing

# Get approved articles
GET /api/admin/ai/articles/?status=approved

# Approve article
POST /api/admin/ai/articles/{id}/approve/
{ "notes": "Approved" }

# Reject article
POST /api/admin/ai/articles/{id}/reject/
{ "notes": "Reason", "regenerate": false }

# Publish article
POST /api/admin/ai/articles/{id}/publish/
{ "visibility": "public" }
```

## Keyboard Shortcuts (Future)
- `a` - Approve selected article
- `r` - Reject selected article
- `p` - Publish selected article
- `↑`/`↓` - Navigate articles
- `Esc` - Close modal/deselect

## Tips
1. Review quality metrics before approving
2. Always provide detailed rejection notes
3. Use regenerate for good topics with poor execution
4. Check SEO metadata before publishing
5. Read full content, not just preview

## Common Issues

**Can't approve**: Check article is in `reviewing` status
**Can't publish**: Must approve article first
**Empty queue**: No articles completed pipeline yet
**Polling stopped**: Refresh page or check console for errors

## Workflow Example

1. Open Review Queue
2. See article "10 Tips for Better Sleep" (reviewing)
3. Click to view details
4. Check metrics: Quality 85%, SEO 90%, Bias 95% ✓
5. Read full content ✓
6. Click "✓ Approve for Publishing"
7. Click "🚀 Publish to Live Site"
8. Confirm publication
9. Article goes live!

## Status Badges

| Badge | Color | Meaning |
|-------|-------|---------|
| Ready for Review | Blue | Status: reviewing |
| Approved | Green | Status: approved |

## Auto-Polling
- **Interval**: Every 5 seconds
- **Purpose**: Get latest article updates
- **Behavior**: Updates list and selected article automatically
- **Performance**: Optimized with Promise.all for parallel fetching
