# YoastSEO Quick Reference Card

## 🚀 Quick Start

```bash
# Start YoastSEO
./manage_yoast.sh start

# Check health
./manage_yoast.sh health

# Test API
./manage_yoast.sh test
```

## 📍 URLs

- **WordPress**: http://localhost:8080
- **Admin**: http://localhost:8080/wp-admin
- **API**: http://localhost:8080/wp-json/yoast/v1/analyze

## 🔑 Credentials

- **Username**: admin
- **Password**: YoastAdmin@123

## 💻 Python Usage

```python
from news.ai_pipeline.yoast_seo import get_yoast_service

yoast = get_yoast_service()

# Analyze
analysis = yoast.analyze_content(
    content="<p>Article content...</p>",
    title="Article Title",
    focus_keyword="keyword"
)

# Get suggestions
suggestions = yoast.optimize_content(
    content="...", title="...", 
    focus_keyword="...", analysis=analysis
)
```

## 📊 Key Metrics

- **SEO Score**: 70+ is good
- **Readability**: 60+ is good  
- **Keyword Density**: 0.5-2.5% is optimal
- **Title Length**: 30-60 characters
- **Meta Description**: 120-160 characters

## 🛠️ Management

```bash
./manage_yoast.sh start    # Start containers
./manage_yoast.sh stop     # Stop containers
./manage_yoast.sh restart  # Restart
./manage_yoast.sh status   # Check status
./manage_yoast.sh logs     # View logs
./manage_yoast.sh health   # Health check
./manage_yoast.sh test     # Test API
```

## 🐳 Docker Commands

```bash
# Check containers
sudo docker ps --filter "name=yoast"

# View logs
sudo docker logs wordpress-yoast

# Restart specific container
sudo docker restart wordpress-yoast
```

## ⚠️ Troubleshooting

**Container not running?**
```bash
./manage_yoast.sh start
```

**API not responding?**
```bash
./manage_yoast.sh restart
curl http://localhost:8080/wp-json/
```

**Need to reset?**
```bash
sudo docker-compose -f docker-compose-yoast.yml down
sudo docker-compose -f docker-compose-yoast.yml up -d
./setup_yoast.sh
```

## 📁 Files

- `docker-compose-yoast.yml` - Container config
- `setup_yoast.sh` - Initial setup
- `manage_yoast.sh` - Management script
- `test_yoast.py` - Integration tests
- `news/ai_pipeline/yoast_seo.py` - Service class

## ✅ Status Check

```bash
# Quick health check
curl http://localhost:8080/wp-json/ && echo "✅ Healthy"

# Detailed test
export YOAST_SEO_URL=http://localhost:8080
python test_yoast.py
```

## 💡 Tips

- YoastSEO runs locally - no external API costs
- Automatic fallback if service unavailable
- Containers persist data across restarts
- No rate limits or request quotas
- 100% free and open source

---

**Status**: ✅ Operational | **Cost**: $0 | **Limits**: None
