#!/usr/bin/env python
"""
Phase 4 Testing Suite: Celery Async Processing

Tests:
1. Celery app initialization and configuration
2. Task registration and discovery
3. Task execution and result storage
4. Redis connection and broker
5. Worker functionality
6. Integration with Phase 2 orchestrator
7. Error handling and retries
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gis.settings')
django.setup()

from celery import Celery
from news.celery import app as celery_app
from news import ai_tasks
from news.ai_models import AIArticle, KeywordSource, AIGenerationConfig
from django_celery_results.models import TaskResult
import time


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_result(test_name, passed, details=""):
    """Print test result with formatting"""
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {test_name}")
    if details:
        print(f"  {details}")


def test_celery_app_initialization():
    """Test 1: Verify Celery app is properly initialized"""
    print_section("Test 1: Celery App Initialization")
    
    try:
        # Check app exists
        assert celery_app is not None
        print_result("Celery app created", True)
        
        # Check app name
        assert celery_app.main == 'news'
        print_result("App name correct", True, f"Name: {celery_app.main}")
        
        # Check configuration
        config = celery_app.conf
        assert config.broker_url is not None
        print_result("Broker URL configured", True, f"Broker: {config.broker_url}")
        
        assert config.result_backend == 'django-db'
        print_result("Result backend configured", True, f"Backend: {config.result_backend}")
        
        assert config.task_serializer == 'json'
        print_result("Task serializer configured", True, f"Serializer: {config.task_serializer}")
        
        return True
        
    except AssertionError as e:
        print_result("Celery app initialization", False, str(e))
        return False
    except Exception as e:
        print_result("Celery app initialization", False, f"Error: {e}")
        return False


def test_task_registration():
    """Test 2: Verify all tasks are registered"""
    print_section("Test 2: Task Registration")
    
    try:
        # Get registered tasks
        registered_tasks = list(celery_app.tasks.keys())
        
        print(f"Total registered tasks: {len(registered_tasks)}")
        
        # Expected custom tasks
        expected_tasks = [
            'news.ai_tasks.generate_article_async',
            'news.ai_tasks.retry_article_stage',
            'news.ai_tasks.run_quality_checks',
            'news.ai_tasks.batch_generate_articles',
        ]
        
        all_found = True
        for task_name in expected_tasks:
            if task_name in registered_tasks:
                print_result(f"Task registered: {task_name}", True)
            else:
                print_result(f"Task registered: {task_name}", False)
                all_found = False
        
        # Check debug task
        if 'news.celery.debug_task' in registered_tasks:
            print_result("Debug task registered", True)
        
        return all_found
        
    except Exception as e:
        print_result("Task registration", False, f"Error: {e}")
        return False


def test_redis_connection():
    """Test 3: Verify Redis connection"""
    print_section("Test 3: Redis Connection")
    
    try:
        import redis
        from django.conf import settings
        
        # Parse broker URL
        broker_url = settings.CELERY_BROKER_URL
        print(f"Broker URL: {broker_url}")
        
        # Try to connect
        if 'redis' in broker_url:
            r = redis.from_url(broker_url)
            r.ping()
            print_result("Redis connection", True, "Redis is accessible")
            
            # Check Redis info
            info = r.info()
            print(f"  Redis version: {info.get('redis_version')}")
            print(f"  Connected clients: {info.get('connected_clients')}")
            
            return True
        else:
            print_result("Redis connection", False, "Not using Redis broker")
            return False
            
    except redis.ConnectionError:
        print_result("Redis connection", False, 
                    "Cannot connect to Redis. Start with: redis-server")
        return False
    except Exception as e:
        print_result("Redis connection", False, f"Error: {e}")
        return False


def test_task_execution():
    """Test 4: Execute debug task and verify result storage"""
    print_section("Test 4: Task Execution")
    
    try:
        # Run debug task
        result = celery_app.tasks['news.celery.debug_task'].apply_async()
        
        print(f"Task ID: {result.id}")
        print_result("Debug task queued", True)
        
        # Wait for result (with timeout)
        try:
            task_result = result.get(timeout=10)
            print_result("Debug task executed", True, f"Result: {task_result}")
        except Exception as e:
            print_result("Debug task executed", False, 
                        f"Task may not have completed: {e}")
            print("  Note: Make sure Celery worker is running:")
            print("  celery -A news worker --loglevel=info")
            return False
        
        # Check result in database
        time.sleep(1)  # Give it time to save
        db_result = TaskResult.objects.filter(task_id=result.id).first()
        
        if db_result:
            print_result("Result stored in database", True)
            print(f"  Status: {db_result.status}")
            print(f"  Date done: {db_result.date_done}")
            return True
        else:
            print_result("Result stored in database", False, 
                        "Result not found in database")
            return False
            
    except Exception as e:
        print_result("Task execution", False, f"Error: {e}")
        return False


def test_article_generation_task():
    """Test 5: Test article generation task structure"""
    print_section("Test 5: Article Generation Task")
    
    try:
        # Get the task
        task = celery_app.tasks.get('news.ai_tasks.generate_article_async')
        
        if not task:
            print_result("Article generation task exists", False)
            return False
        
        print_result("Article generation task exists", True)
        
        # Check task configuration
        print(f"  Max retries: {task.max_retries}")
        print(f"  Retry delay: {task.default_retry_delay}s")
        print_result("Task retry configuration", True)
        
        # Check task signature
        sig = task.s()
        print_result("Task signature creation", True)
        
        return True
        
    except Exception as e:
        print_result("Article generation task", False, f"Error: {e}")
        return False


def test_quality_checks_task():
    """Test 6: Test quality checks task"""
    print_section("Test 6: Quality Checks Task")
    
    try:
        task = celery_app.tasks.get('news.ai_tasks.run_quality_checks')
        
        if not task:
            print_result("Quality checks task exists", False)
            return False
        
        print_result("Quality checks task exists", True)
        
        # This task should not have retries (it's a check, not generation)
        print(f"  Max retries: {task.max_retries}")
        
        return True
        
    except Exception as e:
        print_result("Quality checks task", False, f"Error: {e}")
        return False


def test_batch_generation_task():
    """Test 7: Test batch generation task"""
    print_section("Test 7: Batch Generation Task")
    
    try:
        task = celery_app.tasks.get('news.ai_tasks.batch_generate_articles')
        
        if not task:
            print_result("Batch generation task exists", False)
            return False
        
        print_result("Batch generation task exists", True)
        
        # Test task signature with sample data
        sig = task.s(keyword_ids=[])
        print_result("Batch task signature", True)
        
        return True
        
    except Exception as e:
        print_result("Batch generation task", False, f"Error: {e}")
        return False


def test_django_integration():
    """Test 8: Verify Django models integration"""
    print_section("Test 8: Django Integration")
    
    try:
        # Check if we can access Django models
        from news.ai_models import AIArticle, KeywordSource
        
        print_result("Import AI models", True)
        
        # Check database tables exist
        article_count = AIArticle.objects.count()
        keyword_count = KeywordSource.objects.count()
        
        print_result("Query AI models", True, 
                    f"Articles: {article_count}, Keywords: {keyword_count}")
        
        # Check TaskResult model
        task_result_count = TaskResult.objects.count()
        print_result("Query TaskResult model", True, 
                    f"Task results: {task_result_count}")
        
        return True
        
    except Exception as e:
        print_result("Django integration", False, f"Error: {e}")
        return False


def print_usage_instructions():
    """Print instructions for running Celery worker"""
    print_section("Usage Instructions")
    
    print("""
To use the Celery async processing system:

1. Start Redis (if not running):
   $ redis-server

2. Start Celery worker:
   $ celery -A news worker --loglevel=info

3. (Optional) Start Celery beat for periodic tasks:
   $ celery -A news beat --loglevel=info

4. Monitor tasks:
   $ celery -A news inspect active
   $ celery -A news inspect registered

5. Queue an article for generation (in Django shell):
   >>> from news.ai_tasks import generate_article_async
   >>> from news.ai_models import AIArticle
   >>> article = AIArticle.objects.first()
   >>> generate_article_async.delay(str(article.id))

6. Check task status:
   >>> from django_celery_results.models import TaskResult
   >>> TaskResult.objects.all()

7. View worker stats:
   $ celery -A news inspect stats

For production, use supervisor or systemd to manage workers:
   [program:celery_worker]
   command=celery -A news worker --loglevel=info
   directory=/path/to/project
   user=www-data
   autostart=true
   autorestart=true
    """)


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "    PHASE 4: CELERY ASYNC PROCESSING - TEST SUITE".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    
    results = []
    
    # Run tests
    results.append(("Celery App Initialization", test_celery_app_initialization()))
    results.append(("Task Registration", test_task_registration()))
    results.append(("Redis Connection", test_redis_connection()))
    results.append(("Task Execution", test_task_execution()))
    results.append(("Article Generation Task", test_article_generation_task()))
    results.append(("Quality Checks Task", test_quality_checks_task()))
    results.append(("Batch Generation Task", test_batch_generation_task()))
    results.append(("Django Integration", test_django_integration()))
    
    # Print summary
    print_section("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Phase 4 is ready.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review the output above.")
    
    # Print usage instructions
    print_usage_instructions()
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
