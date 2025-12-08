# Quick Start: Using Gemini for Article Generation

## ✅ Everything is Ready!

Your news system now uses **Google Gemini 2.0 Flash** for AI content generation.

## 🚀 How to Use

### 1. Via React Admin (Recommended)

**Keywords Page → Approve Content:**
1. Go to AI Content > Keywords in admin
2. Click on pending scraped articles
3. Click "Approve" button
4. System automatically:
   - Creates AIArticle with Gemini
   - Queues for generation
   - Generates title, outline, content

### 2. Via Django Admin

**Create Article Manually:**
1. Go to `/admin/news/keywordsource/`
2. Add keyword
3. System auto-generates article using Gemini

### 3. Test the Pipeline

```bash
# Quick API test
python test_gemini.py

# Full article generation
python test_pipeline_gemini.py
```

## 📊 Current Status

- ✅ Gemini API Key: Configured in `.env`
- ✅ Default Model: `gemini-2.0-flash-exp`
- ✅ Pipeline: Fully functional
- ✅ Tests: All passing (3/3)
- ✅ Bug Fixes: Duplicate slug issue fixed

## 🎯 Models Updated

| Component | Old Default | New Default |
|-----------|-------------|-------------|
| Orchestrator | GPT-4 Turbo | Gemini 2.0 Flash |
| AIArticle | gpt-4-turbo-preview | gemini-2.0-flash-exp |
| AIGenerationConfig | OpenAI | Google (Gemini) |
| Max Tokens | 4000 | 8000 |

## 🔧 Configuration

All configuration is automatic. But you can customize:

**Change Model:**
```python
# In .env or config
DEFAULT_MODEL=gemini-1.5-pro  # or gemini-2.0-flash-exp
```

**Switch Provider:**
```python
DEFAULT_AI_PROVIDER=google  # or openai, anthropic
```

## 📈 What Gemini Does

1. **Keyword Analysis**: Analyzes topics
2. **Research**: Gathers information
3. **Outline**: Creates article structure
4. **Content**: Generates full article (800-1500 words)
5. **SEO**: Optimizes meta tags
6. **Quality**: Checks content quality

## 🎨 Gemini Advantages

- 💰 **Cost**: 80% cheaper than GPT-4
- ⚡ **Speed**: Very fast generation
- 📚 **Context**: 1M token context window
- 🎯 **Quality**: Excellent for news content

## 🛠️ Troubleshooting

**If generation fails:**
1. Check API key in `.env`
2. Verify quota not exceeded
3. Check logs: `tail -f logs/generation.log`
4. Run test: `python test_gemini.py`

**Empty title/slug error:**
Fixed! System now always sets title before creating articles.

## 📝 Next Actions

1. **Approve more content** - Go to Keywords page
2. **Monitor generation** - Check Generation Queue
3. **Review articles** - Articles go to "Under Review" status
4. **Publish** - Approve and publish to site

## 🔗 Documentation

- Full details: `GEMINI_INTEGRATION.md`
- API docs: `/docs/API_INTEGRATION_GUIDE.md`
- Pipeline: `/docs/AI_PIPELINE_GUIDE.md`

---

**Ready to generate news with Gemini! 🚀**
