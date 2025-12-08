# Quick Start: Celery Async Processing

## Prerequisites
- Phase 1-3 completed
- Redis installed
- Python environment activated

## 1. Start Services (3 Commands)

```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Celery Worker
cd /home/tapendra/Downloads/projects/news
celery -A news worker --loglevel=info

# Terminal 3: Django Server
cd /home/tapendra/Downloads/projects/news
python manage.py runserver
```

## 2. Generate an Article

**Option A: Django Shell**
```bash
python manage.py shell
```

```python
from news.ai_tasks import generate_article_async
from news.ai_models import AIArticle, KeywordSource

# Create article from existing keyword
keyword = KeywordSource.objects.filter(approval_status='approved').first()
article = AIArticle.objects.create(
    keyword=keyword,
    template_type='analysis',
    status='queued'
)

# Queue for generation
result = generate_article_async.delay(str(article.id))
print(f"Task ID: {result.id}")
print(f"Article ID: {article.id}")
```

**Option B: API Endpoint** (if you create one)
```bash
curl -X POST http://localhost:8000/api/admin/ai-articles/ \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "keyword-uuid-here",
    "template_type": "analysis",
    "status": "queued"
  }'
```

## 3. Monitor Progress

```python
# Check task status
from django_celery_results.models import TaskResult
task = TaskResult.objects.get(task_id='your-task-id')
print(task.status)  # PENDING, STARTED, SUCCESS, FAILURE

# Check article status
from news.ai_models import AIArticle
article = AIArticle.objects.get(id='your-article-id')
print(article.status)  # queued, generating, completed, failed
print(article.workflow_stage)  # Current pipeline stage
print(article.overall_quality_score)  # Quality score
```

## 4. Run Quality Checks Only

```python
from news.ai_tasks import run_quality_checks
article_id = 'your-article-id'
result = run_quality_checks.delay(article_id)

# Get results
quality_report = result.get(timeout=120)
print(f"Bias: {quality_report['bias_score']}")
print(f"Facts: {quality_report['fact_check_score']}")
print(f"Perspectives: {quality_report['perspective_balance_score']}")
print(f"Passes Standards: {quality_report['passes_standards']}")
```

## 5. Batch Generation

```python
from news.ai_tasks import batch_generate_articles
from news.ai_models import KeywordSource

# Get approved keywords
keywords = KeywordSource.objects.filter(approval_status='approved')[:10]
keyword_ids = [str(k.id) for k in keywords]

# Queue batch
result = batch_generate_articles.delay(keyword_ids)
batch_report = result.get()
print(f"Created: {batch_report['created']}")
print(f"Failed: {batch_report['failed']}")
print(f"Article IDs: {batch_report['article_ids']}")
```

## 6. Retry Failed Articles

```python
from news.ai_tasks import retry_article_stage
from news.ai_models import AIArticle

# Find failed article
article = AIArticle.objects.filter(status='failed').first()
failed_stage = article.workflow_stage

# Retry from failed stage
result = retry_article_stage.delay(str(article.id), failed_stage)
```

## 7. Monitor Workers

```bash
# Active tasks
celery -A news inspect active

# Registered tasks
celery -A news inspect registered

# Worker stats
celery -A news inspect stats

# Purge all pending tasks
celery -A news purge
```

## Troubleshooting

### Worker Not Processing Tasks
```bash
# Check Redis connection
redis-cli ping  # Should return PONG

# Check worker logs
celery -A news worker --loglevel=debug

# Restart worker
# Ctrl+C to stop, then restart
```

### Tasks Failing
```python
# Check error logs
from news.ai_models import AIArticle
article = AIArticle.objects.get(id='article-id')
print(article.error_log)

# Check TaskResult
from django_celery_results.models import TaskResult
task = TaskResult.objects.get(task_id='task-id')
print(task.traceback)
```

### API Keys Missing
```bash
# Set environment variables
export OPENAI_API_KEY='your-key-here'
export ANTHROPIC_API_KEY='your-key-here'

# Or add to .env file
echo "OPENAI_API_KEY=your-key-here" >> .env
echo "ANTHROPIC_API_KEY=your-key-here" >> .env
```

## Performance Tips

1. **Multiple Workers:** Scale horizontally
   ```bash
   celery -A news worker --concurrency=4 --loglevel=info
   ```

2. **Rate Limiting:** Limit API calls
   ```python
   @shared_task(rate_limit='10/m')  # 10 per minute
   ```

3. **Task Routing:** Separate queues
   ```bash
   celery -A news worker -Q generation,quality_checks
   ```

4. **Monitoring:** Install Flower
   ```bash
   pip install flower
   flower -A news --port=5555
   # Visit http://localhost:5555
   ```

## Expected Timings

- **generate_article_async:** 3-15 minutes
- **run_quality_checks:** 30-120 seconds
- **batch_generate_articles:** N × article_time (parallel)
- **retry_article_stage:** 1-10 minutes

## Production Deployment

See `docs/PHASE4_COMPLETE.md` for:
- Supervisor configuration
- Systemd service files
- Scaling strategies
- Monitoring setup
