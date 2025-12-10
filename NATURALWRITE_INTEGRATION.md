# Per-Stage AI Configuration & NaturalWrite Integration

## Overview
Implemented comprehensive per-stage AI configuration allowing you to specify different AI providers and models for each pipeline stage, plus integrated NaturalWrite API for humanization and AI detection.

## What Changed

### 1. Database Model Updates (`news/ai_models.py`)
- **Added `NATURALWRITE` provider** to `AIGenerationConfig.Provider` choices
- **Added `stage_configs` JSON field** to store per-stage provider/model configurations
- Created migration: `0019_add_naturalwrite_and_stage_configs.py`

### 2. Pipeline Orchestrator Updates (`news/ai_pipeline/orchestrator.py`)
- **Added `naturalwrite_api_key`** to config loading from environment
- **Added `stage_configs`** support in config
- **New method `_get_llm_for_stage()`** - Returns appropriate LLM for each stage based on stage_configs
- **Updated `_humanize_content()`** to use NaturalWrite API with LLM fallback
- **Updated `_check_ai_detection()`** to use NaturalWrite API detection
- **Updated all stages** to call `_get_llm_for_stage()` instead of using `self.llm_primary`

### 3. Frontend UI Overhaul (`frontend/src/admin/pages/ai-content/settings/`)

#### New AISettings.jsx Features:
- **General Tab**: Default provider/model settings (used when stage has no custom config)
- **Stages Tab**: Configure provider/model for each of 14 pipeline stages:
  - Keyword Analysis
  - Research (non-LLM)
  - Outline
  - Content Generation
  - Humanization
  - AI Detection
  - Plagiarism Check (non-LLM)
  - Bias Detection
  - Fact Verification
  - Perspective Analysis
  - SEO Optimization
  - Meta Generation
  - Image Generation (non-LLM)
  - Finalization

#### UI Features:
- **Visual Cards**: Each stage displayed as a card showing:
  - Stage name and description
  - Provider dropdown (with "Use Default" option)
  - Model dropdown (populated based on selected provider)
  - Clear button (X) to remove custom config
- **Color Coding**: Cards with custom configs highlighted in blue
- **Default Indicators**: Shows which default will be used when no custom config set
- **Non-LLM Stages**: Clearly marked as not using LLM

### 4. NaturalWrite API Integration

#### Humanization (`_humanize_content`):
```python
# API Call
POST https://api.naturalwrite.com/v1/humanize
{
  "text": content,
  "mode": "enhanced",  # Options: standard, enhanced, creative
  "preserve_formatting": True,
  "preserve_links": True
}

# Response
{
  "humanized_text": "...",
  "ai_score_before": 85.5,
  "ai_score_after": 22.3
}
```

#### AI Detection (`_check_ai_detection`):
```python
# API Call
POST https://api.naturalwrite.com/v1/detect
{
  "text": content
}

# Response
{
  "ai_probability": 0.223,  # Converted to percentage
  "details": {...}
}
```

### 5. Model Configuration (`ai-models-config.json`)
Added **NaturalWrite provider** with 3 models:
- `humanize-standard` (Recommended)
- `humanize-enhanced`
- `humanize-creative`

## Environment Variables

Your `.env` file needs:
```env
NATURALWRITE_API_KEY=your_naturalwrite_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

## Usage Examples

### Example 1: Use Groq for fast stages, Gemini for quality stages
```javascript
stage_configs = {
  "outline": {
    "provider": "groq",
    "model": "llama-3.1-8b-instant"
  },
  "content_generation": {
    "provider": "google",
    "model": "gemini-exp-1206"
  },
  "bias_detection": {
    "provider": "groq",
    "model": "llama-3.3-70b-versatile"
  }
}
```

### Example 2: Use NaturalWrite for humanization
```javascript
stage_configs = {
  "humanization": {
    "provider": "naturalwrite",
    "model": "humanize-enhanced"
  }
}
```

## How It Works

### Stage Configuration Priority:
1. **Check `stage_configs[stage_name]`** - If exists, use that provider/model
2. **Fall back to defaults** - Use `ai_provider` and `model_name` from general settings
3. **Create LLM instance** - Initialize appropriate LLM (Groq, Gemini, OpenAI, Anthropic, NaturalWrite)

### NaturalWrite Fallback Logic:
- **Humanization**: If NaturalWrite API fails, falls back to LLM-based humanization
- **AI Detection**: If NaturalWrite API fails, skips detection (returns bypassed=True)

## API Key Security

✅ **Correct**: API keys stored in `.env` file (server-side only)
❌ **Wrong**: Never store API keys in database or frontend code

The frontend only displays status (configured/not-configured), actual keys never leave the backend.

## Testing

### Test Groq + NaturalWrite Pipeline:
1. Go to **AI Settings** → **General Tab**
2. Set default: `Groq` / `llama-3.1-8b-instant`
3. Go to **Stages Tab**
4. Set **Humanization**: `NaturalWrite` / `humanize-enhanced`
5. Save settings
6. Generate an article and check logs for:
   ```
   INFO:news.ai_pipeline.orchestrator:Using NaturalWrite API for humanization
   INFO:news.ai_pipeline.orchestrator:NaturalWrite humanization successful: 5816 chars
   INFO:news.ai_pipeline.orchestrator:Using NaturalWrite API for AI detection
   INFO:news.ai_pipeline.orchestrator:NaturalWrite AI detection: 22.30% AI-generated
   ```

## Benefits

1. **Cost Optimization**: Use cheaper/faster models for simple stages (outline), expensive/smart models for critical stages (content_generation)
2. **Speed Optimization**: Use ultra-fast Groq models for stages that need quick turnaround
3. **Quality Optimization**: Use best models (Gemini 3, Claude) for stages requiring deep reasoning
4. **Specialized Tools**: Use NaturalWrite for humanization (better than LLM-based humanization)
5. **Flexibility**: Change models per-stage without touching code

## Migration Applied

```bash
.venv/bin/python manage.py migrate
# Applying news.0019_add_naturalwrite_and_stage_configs... OK
```

## Files Changed

### Backend:
- `news/ai_models.py` - Added provider, stage_configs field
- `news/migrations/0019_add_naturalwrite_and_stage_configs.py` - Migration
- `news/ai_pipeline/orchestrator.py` - Stage-specific LLM logic, NaturalWrite integration

### Frontend:
- `frontend/src/admin/pages/ai-content/settings/AISettings.jsx` - Complete redesign with stages tab
- `frontend/src/admin/pages/ai-content/settings/AISettings.css` - New styling for stage cards
- `frontend/src/admin/config/ai-models-config.json` - Added NaturalWrite provider

## Next Steps

1. **Restart Django server** to load new orchestrator code
2. **Test generation** with NaturalWrite humanization
3. **Monitor costs** across different provider combinations
4. **Fine-tune stage assignments** based on quality/cost/speed requirements

## Notes

- NaturalWrite API requires valid API key to work
- Non-LLM stages (Research, Plagiarism Check, Image Generation) don't show provider/model dropdowns
- Clearing a stage config (X button) makes it use default settings
- Changes save to database `stage_configs` JSON field
