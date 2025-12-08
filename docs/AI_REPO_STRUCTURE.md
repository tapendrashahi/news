# AI Content Generation System - Repository Structure

## 📁 Project Structure Overview

```
news/
├── docs/
│   ├── AI_CONTENT_TASKS.md           # ✅ Main task checklist
│   ├── agent_workflow_plan.md        # ✅ Comprehensive implementation plan
│   ├── AI_PIPELINE_GUIDE.md          # 📝 Developer documentation (template)
│   ├── API_INTEGRATION_GUIDE.md      # 📝 API integration guide (template)
│   ├── AI_CONTENT_USER_GUIDE.md      # 📝 User guide (template)
│   └── AI_DEPLOYMENT_GUIDE.md        # 📝 Deployment guide (template)
│
├── news/                              # Django backend
│   ├── ai_models.py                  # 🔲 Database models
│   ├── ai_serializers.py             # 🔲 DRF serializers
│   ├── ai_views.py                   # 🔲 API viewsets
│   ├── ai_tasks.py                   # 🔲 Celery tasks
│   ├── celery.py                     # 🔲 Celery configuration
│   │
│   └── ai_pipeline/                  # LangChain pipeline
│       ├── __init__.py               # 🔲 Package init
│       ├── orchestrator.py           # 🔲 Main pipeline orchestrator
│       │
│       ├── chains/                   # LangChain chains
│       │   ├── __init__.py          # 🔲
│       │   ├── content_generator.py # 🔲 Content generation chain
│       │   ├── humanizer.py         # 🔲 Humanization chain
│       │   ├── seo_optimizer.py     # 🔲 SEO optimization
│       │   └── meta_generator.py    # 🔲 Meta tags generation
│       │
│       ├── agents/                   # LangChain agents
│       │   ├── __init__.py          # 🔲
│       │   └── research_agent.py    # 🔲 Web research agent
│       │
│       ├── tools/                    # Pipeline tools
│       │   ├── __init__.py          # 🔲
│       │   ├── keyword_scraper.py   # 🔲 Keyword discovery
│       │   ├── ai_detector.py       # 🔲 AI content detection
│       │   ├── plagiarism_checker.py # 🔲 Plagiarism checking
│       │   ├── bias_detector.py     # 🔲 Bias detection (AI Analitica)
│       │   ├── fact_verifier.py     # 🔲 Fact verification
│       │   ├── perspective_analyzer.py # 🔲 Multi-perspective analysis
│       │   └── image_generator.py   # 🔲 DALL-E image generation
│       │
│       └── prompts/                  # Prompt templates
│           ├── __init__.py          # 🔲
│           ├── article_templates.py # 🔲 Article generation prompts
│           ├── seo_prompts.py       # 🔲 SEO prompts
│           └── meta_prompts.py      # 🔲 Meta generation prompts
│
├── frontend/                         # React admin interface
│   └── src/
│       └── admin/
│           ├── services/
│           │   └── aiContentService.js # 🔲 API service layer
│           │
│           └── pages/
│               └── ai-content/
│                   ├── keywords/         # Keyword management
│                   │   ├── KeywordsList.jsx # 🔲
│                   │   ├── KeywordForm.jsx # 🔲
│                   │   ├── KeywordScraper.jsx # 🔲
│                   │   ├── KeywordApproval.jsx # 🔲
│                   │   └── Keywords.css # 🔲
│                   │
│                   ├── generation-queue/  # Real-time generation tracking
│                   │   ├── GenerationQueue.jsx # 🔲
│                   │   ├── ArticleProgress.jsx # 🔲
│                   │   ├── StageIndicator.jsx # 🔲
│                   │   └── GenerationQueue.css # 🔲
│                   │
│                   ├── review-queue/      # Article review interface
│                   │   ├── ReviewQueue.jsx # 🔲
│                   │   ├── ArticleReview.jsx # 🔲
│                   │   ├── QualityMetrics.jsx # 🔲
│                   │   ├── ComparisonView.jsx # 🔲
│                   │   └── ReviewQueue.css # 🔲
│                   │
│                   ├── settings/          # AI configuration
│                   │   ├── AISettings.jsx # 🔲
│                   │   ├── APICredentials.jsx # 🔲
│                   │   ├── GenerationSettings.jsx # 🔲
│                   │   ├── QualityThresholds.jsx # 🔲
│                   │   ├── PromptTemplates.jsx # 🔲
│                   │   └── Settings.css # 🔲
│                   │
│                   └── analytics/         # Analytics dashboard
│                       ├── AIAnalytics.jsx # 🔲
│                       ├── BiasMetrics.jsx # 🔲
│                       ├── CostAnalysis.jsx # 🔲
│                       ├── QualityTrends.jsx # 🔲
│                       └── Analytics.css # 🔲
│
└── .env.example                      # ✅ Environment variables template

```

## 📊 File Status Legend

- ✅ **Complete** - File created and ready
- 🔲 **Empty Template** - File created, needs implementation
- 📝 **Documentation Template** - Documentation structure ready

## 🎯 Implementation Workflow

### Step 1: Environment Setup
1. Copy `.env.example` to `.env`
2. Fill in API keys and configuration
3. Install dependencies from `requirements.txt`

### Step 2: Backend Development (Weeks 1-5)
1. Start with `news/ai_models.py` (database models)
2. Create migrations and apply
3. Implement serializers and views
4. Build LangChain pipeline components
5. Set up Celery tasks

### Step 3: Frontend Development (Weeks 7-8)
1. Implement service layer (`aiContentService.js`)
2. Build keyword management UI
3. Create generation queue dashboard
4. Implement review interface
5. Build settings and analytics

### Step 4: Integration & Testing (Weeks 9-10)
1. End-to-end testing
2. Quality assurance
3. Performance optimization

### Step 5: Documentation & Deployment (Weeks 11-12)
1. Complete documentation templates
2. Production deployment
3. Monitoring setup

## 📋 Key Implementation Files

### Backend Priority Files
1. `news/ai_models.py` - Define database schema
2. `news/ai_pipeline/orchestrator.py` - Main pipeline logic
3. `news/ai_pipeline/tools/bias_detector.py` - Critical for AI Analitica mission
4. `news/ai_pipeline/tools/fact_verifier.py` - Ensure 100% citation
5. `news/ai_tasks.py` - Async processing

### Frontend Priority Files
1. `frontend/src/admin/services/aiContentService.js` - API integration
2. `frontend/src/admin/pages/ai-content/generation-queue/GenerationQueue.jsx` - Real-time tracking
3. `frontend/src/admin/pages/ai-content/review-queue/ArticleReview.jsx` - Quality control
4. `frontend/src/admin/pages/ai-content/settings/QualityThresholds.jsx` - Configure standards

## 🚀 Getting Started

### For Code Generation with Claude
1. Open each empty file in sequence
2. Copy the task description from file header
3. Use Claude to generate implementation
4. Review with GitHub Copilot
5. Test and iterate

### Recommended Order
1. Start with database models (Phase 1)
2. Build core tools (bias detector, fact verifier)
3. Create LangChain chains
4. Implement Celery tasks
5. Build frontend components
6. Integration testing

## 📖 Reference Documentation
- **Main Plan**: `docs/agent_workflow_plan.md` (1252 lines)
- **Task List**: `docs/AI_CONTENT_TASKS.md` (comprehensive checklist)
- **API Keys**: `.env.example` (all required credentials)

## 🎓 AI Analitica Mission Alignment

Critical files that must follow AI Analitica standards:
- `news/ai_pipeline/prompts/article_templates.py` - System prompts emphasizing objectivity
- `news/ai_pipeline/tools/bias_detector.py` - < 20% bias threshold
- `news/ai_pipeline/tools/fact_verifier.py` - 100% citation requirement
- `news/ai_pipeline/tools/perspective_analyzer.py` - ≥ 2 perspectives per article

## 📞 Support
For implementation questions, refer to:
- Task descriptions in each file header
- Phase documentation in `docs/agent_workflow_plan.md`
- Task checklist in `docs/AI_CONTENT_TASKS.md`

---

**Created:** December 8, 2025  
**Total Files:** 56 empty templates ready for implementation  
**Estimated Timeline:** 12 weeks  
**Status:** Ready for code generation
