#!/bin/bash
# YoastSEO Management Script

case "$1" in
    start)
        echo "Starting YoastSEO containers..."
        sudo docker-compose -f docker-compose-yoast.yml up -d
        echo "Waiting for services to be ready..."
        sleep 10
        sudo docker ps --filter "name=yoast"
        echo ""
        echo "YoastSEO is running at: http://localhost:8080"
        ;;
    
    stop)
        echo "Stopping YoastSEO containers..."
        sudo docker-compose -f docker-compose-yoast.yml down
        ;;
    
    restart)
        echo "Restarting YoastSEO containers..."
        sudo docker-compose -f docker-compose-yoast.yml restart
        ;;
    
    status)
        echo "YoastSEO container status:"
        sudo docker ps --filter "name=yoast"
        ;;
    
    logs)
        echo "YoastSEO logs (press Ctrl+C to exit):"
        sudo docker-compose -f docker-compose-yoast.yml logs -f wordpress-yoast
        ;;
    
    test)
        echo "Testing YoastSEO API..."
        curl -X POST http://localhost:8080/wp-json/yoast/v1/analyze \
          -H "Content-Type: application/json" \
          -d '{
            "text": "Test article content for SEO analysis. This is a longer text with multiple sentences.",
            "title": "Test Article Title",
            "keyword": "test",
            "description": "Test meta description for SEO analysis"
          }' | python3 -m json.tool
        ;;
    
    health)
        echo "Checking YoastSEO health..."
        curl -s http://localhost:8080/wp-json/ > /dev/null && echo "✅ YoastSEO API is healthy" || echo "❌ YoastSEO API is not responding"
        ;;
    
    *)
        echo "YoastSEO Management Script"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|logs|test|health}"
        echo ""
        echo "Commands:"
        echo "  start    - Start YoastSEO containers"
        echo "  stop     - Stop YoastSEO containers"
        echo "  restart  - Restart YoastSEO containers"
        echo "  status   - Show container status"
        echo "  logs     - View container logs"
        echo "  test     - Test API endpoint"
        echo "  health   - Check API health"
        exit 1
        ;;
esac
