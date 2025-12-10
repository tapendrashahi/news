# Stuck Article Generation Fix

## Problem
Articles get stuck in "generating" status when:
- Background thread crashes unexpectedly
- Server restarts while generation is running
- Unhandled exceptions in the pipeline
- Long-running API calls timeout

## Solutions Implemented

### 1. Management Command
```bash
# Reset all stuck articles (stuck > 1 hour)
python manage.py reset_stuck_articles

# Reset stuck articles with custom timeout
python manage.py reset_stuck_articles --hours 2

# Reset specific article by ID
python manage.py reset_stuck_articles --article-id <uuid>

# Reset to QUEUED instead of FAILED
python manage.py reset_stuck_articles --to-queued
```

### 2. API Endpoint
**POST** `/api/ai-articles/check_stuck/`

Request:
```json
{
  "hours": 1,
  "to_queued": false
}
```

Response:
```json
{
  "stuck_count": 2,
  "reset_articles": [
    {
      "id": "9af2bbec-8dd0-4c19-925a-0553a6cb395d",
      "keyword": "Explore 300+ AI courses",
      "was_stuck_at": "content_generation",
      "last_updated": "2025-12-10T12:07:50.611378Z"
    }
  ],
  "reset_to": "failed"
}
```

### 3. Improved Error Handling
The generation thread now:
- Catches all exceptions properly
- Updates article status to FAILED if thread crashes
- Logs detailed error information
- Includes full traceback for debugging

## Frontend Integration

Add to your Generation Queue page:

```javascript
// Check for stuck articles every 5 minutes
useEffect(() => {
  const checkStuckInterval = setInterval(async () => {
    try {
      const response = await axios.post('/api/ai-articles/check_stuck/', {
        hours: 1,
        to_queued: false
      });
      
      if (response.data.stuck_count > 0) {
        console.log(`Reset ${response.data.stuck_count} stuck articles`);
        // Refresh the articles list
        fetchArticles();
      }
    } catch (error) {
      console.error('Error checking stuck articles:', error);
    }
  }, 5 * 60 * 1000); // Every 5 minutes
  
  return () => clearInterval(checkStuckInterval);
}, []);
```

## Current Status

✅ **Article `9af2bbec-8dd0-4c19-925a-0553a6cb395d` has been reset to QUEUED**

The article "Explore 300+ AI courses" was stuck at content_generation stage and has been reset to QUEUED status. You can now retry the generation from the Generation Queue page.

## Prevention Tips

1. **Monitor server logs** - Check for pipeline errors regularly
2. **Use the management command** - Run `reset_stuck_articles` periodically via cron
3. **Frontend polling** - Implement the check_stuck endpoint in frontend
4. **Consider Celery** - For production, use Celery for background tasks instead of threads

## Testing

Test the reset functionality:
```bash
# Check current stuck articles
python manage.py shell -c "from news.ai_models import AIArticle; print(AIArticle.objects.filter(status='generating').count())"

# Reset them
python manage.py reset_stuck_articles --to-queued

# Verify reset
python manage.py shell -c "from news.ai_models import AIArticle; print(AIArticle.objects.filter(status='queued').count())"
```
