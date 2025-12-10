# Plagiarism Check - Quick Reference

## 🚀 Quick Start

### 1. Configure Plagiarism Check
```bash
# Already configured in .env
CODEQUIRY_API_KEY=84c86cedaf8e7cd6d9a20615b1689859c821c2da9e0f4f67a1aae3445a2a3554
```

### 2. Enable in AI Settings
1. Go to: **Admin → AI Content → Settings**
2. Click **PLAGIARISM** tab
3. Toggle **ON**
4. Set threshold: **5%**
5. Click **Save Configuration**

### 3. Generate Article
Articles automatically checked and rewritten if needed!

---

## ⚙️ Default Configuration

```json
{
  "enabled": true,
  "threshold": 5.0,
  "maxRetries": 3,
  "autoRewrite": true,
  "strategy": "rewrite_sections"
}
```

---

## 📊 Threshold Guide

| Score | Status | Action |
|-------|--------|--------|
| 0-5% | ✅ Pass | Publish |
| 5-10% | ⚠️ Warning | Auto-rewrite (1 attempt) |
| 10-15% | 🚨 High | Auto-rewrite (2-3 attempts) |
| >15% | ❌ Critical | Rewrite entire article |

---

## 🔄 Workflow

```
Content Generated
    ↓
Humanized
    ↓
Plagiarism Check ──→ < 5%? ──→ ✅ PASS
    ↓                    ↓
  > 5%               NO
    ↓                    ↓
Rewrite Content     Rewrite
    ↓                    ↓
Re-check            Re-check
    ↓                    ↓
< 5%? ──→ YES ──→ ✅ PASS
    ↓
   NO
    ↓
Retry (max 3x)
    ↓
Still > 5%? ──→ ❌ FAIL
```

---

## 🛠️ Key Files

### Backend
- `news/ai_pipeline/plagiarism_checker.py` - Codequiry integration
- `news/ai_pipeline/orchestrator.py` - Auto-rewrite logic
- `news/ai_pipeline/prompts/plagiarism_prompts.py` - Rewrite prompts
- `news/api_admin.py` - Configuration API endpoint

### Frontend
- `frontend/src/admin/pages/ai-content/settings/PlagiarismSettings.jsx` - UI
- `frontend/src/admin/pages/ai-content/settings/PlagiarismSettings.css` - Styles

### Config
- `plagiarism_config.json` - Settings (auto-generated)
- `.env` - CODEQUIRY_API_KEY

---

## 🧪 Testing

### Test Plagiarism Check
```python
from news.ai_pipeline.plagiarism_checker import get_plagiarism_checker

checker = get_plagiarism_checker()
result = checker.check_plagiarism(
    content="Your article content here",
    title="Article Title",
    threshold=5.0
)

print(f"Score: {result.overall_score}%")
print(f"Passed: {result.is_plagiarized is False}")
```

---

## 🔧 Troubleshooting

### Issue: High Plagiarism Score Won't Reduce
**Solution**: 
1. Increase `maxRetries` to 5
2. Enable "Rewrite Entire Article"
3. Lower threshold temporarily

### Issue: API Error
**Solution**: 
1. Check CODEQUIRY_API_KEY is valid
2. Verify internet connection
3. Check Codequiry API status

### Issue: SEO Lost After Rewrite
**Solution**: 
1. Enable "Maintain SEO" in settings
2. Verify keyword density in rewritten content
3. Check prompts preserve keyword placement

---

## 📈 Success Metrics

- **Target**: < 5% plagiarism
- **Rewrite Success**: 95%+ on attempt 1-2
- **SEO Retention**: 100% (keywords, density, structure)
- **Nepal Context**: 100% preserved
- **Student Tone**: 100% maintained

---

## 💡 Tips

### For Best Results
1. ✅ Keep threshold at **5%** for educational content
2. ✅ Enable **both** web and database checks
3. ✅ Use **"Rewrite Sections"** strategy (faster)
4. ✅ Enable **SEO** and **Nepal context** maintenance
5. ✅ Set **max retries to 3** (optimal)

### For Original Content
1. Use unique Nepal examples from the start
2. Avoid copying phrases from research
3. Express ideas in your own words
4. Add student perspective and "you" language

---

## 🎯 Quick Commands

### Check Health
```python
from news.ai_pipeline.plagiarism_checker import get_plagiarism_checker
checker = get_plagiarism_checker()
is_healthy, message = checker.health_check()
print(f"Status: {message}")
```

### Load Config
```python
import json
with open('plagiarism_config.json') as f:
    config = json.load(f)
print(f"Threshold: {config['plagiarism_check']['threshold']}%")
```

### Manual Rewrite
```python
from news.ai_pipeline.orchestrator import ContentOrchestrator
orchestrator = ContentOrchestrator()

# Rewrite plagiarized content
rewritten = await orchestrator._rewrite_plagiarized_sections(
    article, context, plagiarism_result, config
)
```

---

**Ready to use!** 🚀

All plagiarism checking is now automated in the content generation pipeline.
