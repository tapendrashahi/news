# Legal Pages - Quick Reference

## Access the Feature

**Admin Panel**: http://localhost:3000/admin/legal

## Quick Actions

### View All Legal Pages
```
Navigate to: Admin Panel → Legal Pages (⚖️ icon in sidebar)
```

### Create New Page
```
1. Click "Create New Page" button
2. Select page type from dropdown
3. Load a template (optional) or write custom JSON
4. Fill in:
   - Title
   - Slug (URL identifier)
   - Status (Draft/Published/Archived)
   - Version number
   - Effective date
5. Click "Create Page"
```

### Edit Existing Page
```
1. Find the page in the list
2. Click "Edit" button
3. Make changes
4. Click "Update Page"
```

### Publish/Unpublish
```
- Publish: Click "Publish" on draft pages
- Unpublish: Click "Unpublish" on published pages
```

## Available Templates

1. **Privacy Policy** - `privacy_polity.json`
2. **Terms of Service** - `terms_of_service.json`
3. **Cookie Policy** - `cookee.json`
4. **Ethics Policy** - `ethics_policy.json`
5. **Editorial Guidelines** - `guidemines.json`
6. **About Us** - `about.json`

## JSON Editor Tips

- **Load Template**: Select from dropdown → Click "Load Template"
- **Format JSON**: Click "Format JSON" button to auto-indent
- **Validation**: Real-time error checking (red border = error)
- **Preview**: JSON preview shown below editor

## API Endpoints Reference

### Public (No Auth)
```
GET /api/legal/                      # List published pages
GET /api/legal/{id}/                 # Get specific page
GET /api/legal/slug/{slug}/          # Get by slug
GET /api/legal/type/{page_type}/     # Get by type
```

### Admin (Auth Required)
```
GET    /api/admin/legal/             # List all pages
POST   /api/admin/legal/             # Create page
GET    /api/admin/legal/{id}/        # Get page
PUT    /api/admin/legal/{id}/        # Update page
DELETE /api/admin/legal/{id}/        # Delete page
POST   /api/admin/legal/{id}/publish/     # Publish
POST   /api/admin/legal/{id}/unpublish/   # Unpublish
GET    /api/admin/legal/page_types/       # Get types
```

## Status Meanings

- **Draft** 🟡 - Work in progress, not visible to public
- **Published** 🟢 - Live and visible to public
- **Archived** ⚪ - Outdated version, hidden from public

## Current Pages (Auto-populated)

✅ Privacy Policy (v1.0) - Published  
✅ Terms of Service (v1.0) - Published  
✅ Cookie Policy (v1.0) - Published  
✅ Ethics Policy (v2.0) - Published  
✅ Editorial Guidelines (v2.0) - Published  
✅ About Us (v1.0) - Published  

## Common Tasks

### Update Privacy Policy Version
```
1. Edit Privacy Policy page
2. Modify JSON content
3. Update version to "2.0"
4. Set new effective date
5. Save and publish
```

### Add New Legal Page Type
```
Backend:
1. Add to LegalPage.PAGE_TYPES in legal_models.py
2. Create migration
3. Add JSON template to administration/

Frontend:
4. Add to jsonTemplates in LegalPageForm.jsx
5. Restart servers
```

### Repopulate from JSON Files
```bash
python populate_legal_pages.py
```

## Troubleshooting

**"Invalid JSON" Error**
- Click "Format JSON" to check syntax
- Look for unclosed quotes or brackets
- Remove trailing commas

**Page Not Showing**
- Check status (must be Published)
- Verify effective date is not future
- Check permissions (logged in as admin?)

**Template Won't Load**
- Verify file exists in administration/ folder
- Check JSON syntax in template file
- Browser console for errors

## File Locations

```
Backend:
- news/legal_models.py
- news/legal_views.py
- news/legal_serializers.py

Frontend:
- frontend/src/admin/pages/legal/
- frontend/src/admin/services/legalService.js

Templates:
- administration/*.json

Scripts:
- populate_legal_pages.py
```

## Support

For detailed documentation, see:
- `LEGAL_PAGES_GUIDE.md` - Complete guide
- `LEGAL_PAGES_IMPLEMENTATION_SUMMARY.md` - Technical details

---

**Quick Start**: Login → Admin Panel → Legal Pages → Create/Edit
