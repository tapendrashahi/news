# Legal Pages Implementation Plan

## Overview
Create 5 legal/policy pages for the Footer's Legal section, fetching content from existing JSON files in the administration folder.

---

## Pages to Create

### 1. **Privacy Policy** (`/privacy-policy`)
- **JSON Source**: `/administration/privacy_polity.json`
- **Route**: `/privacy-policy`
- **Component**: `PrivacyPolicy.jsx`
- **CSS**: `PrivacyPolicy.css`

### 2. **Terms of Service** (`/terms-of-service`)
- **JSON Source**: `/administration/terms_of_service.json`
- **Route**: `/terms-of-service`
- **Component**: `TermsOfService.jsx`
- **CSS**: `TermsOfService.css`

### 3. **Cookie Policy** (`/cookie-policy`)
- **JSON Source**: `/administration/cookee.json`
- **Route**: `/cookie-policy`
- **Component**: `CookiePolicy.jsx`
- **CSS**: `CookiePolicy.css`

### 4. **Editorial Guidelines** (`/editorial-guidelines`)
- **JSON Source**: `/administration/guidemines.json`
- **Route**: `/editorial-guidelines`
- **Component**: `EditorialGuidelines.jsx`
- **CSS**: `EditorialGuidelines.css`

### 5. **Ethics Policy** (`/ethics-policy`)
- **JSON Source**: `/administration/ethics_policy.json`
- **Route**: `/ethics-policy`
- **Component**: `EthicsPolicy.jsx`
- **CSS**: `EthicsPolicy.css`

---

## Shared Layout Structure

All pages will follow the same structure based on Django template:

```
┌─────────────────────────────────────┐
│  Hero Section (Dark Gradient)      │
│  - Page Title                       │
│  - Subtitle                         │
│  - Last Updated Badge               │
└─────────────────────────────────────┘
┌──────────┬──────────────────────────┐
│   TOC    │  Main Content            │
│ (Sticky) │  - Introduction          │
│          │  - Sections with Icons   │
│          │  - Subsections           │
│          │  - Items/Lists           │
│          │                          │
└──────────┴──────────────────────────┘
```

---

## Component Structure

### Reusable Components

#### 1. **LegalPageLayout.jsx**
A shared layout component for all legal pages:
- Hero section with title, subtitle, last updated
- Two-column layout (TOC + Content)
- Sticky table of contents
- Responsive design

#### 2. **LegalPageContent.jsx**
Renders content sections dynamically:
- Section headers with icons
- Subsections
- Bullet lists
- Formatted text

---

## JSON File Structure (Common Pattern)

```json
{
  "metadata": {
    "title": "...",
    "lastUpdated": "...",
    "effectiveDate": "...",
    "companyName": "...",
    "companyEmail": "..."
  },
  "introduction": {
    "title": "...",
    "content": ["paragraph 1", "paragraph 2"]
  },
  "sections": [
    {
      "id": "section-id",
      "title": "Section Title",
      "icon": "icon-name",
      "content": ["paragraph"],
      "items": ["item 1", "item 2"],
      "subsections": [
        {
          "title": "Subsection",
          "content": "...",
          "items": ["..."]
        }
      ]
    }
  ]
}
```

---

## Implementation Steps

### Step 1: Copy JSON Files to Frontend
```bash
cp /home/tapendra/Downloads/projects/news/administration/*.json \\
   /home/tapendra/Downloads/projects/news/frontend/public/administration/
```

### Step 2: Create Shared Layout Component
**File**: `frontend/src/components/legal/LegalPageLayout.jsx`
- Hero section
- TOC sidebar (sticky)
- Main content area
- Responsive grid

### Step 3: Create Shared Layout CSS
**File**: `frontend/src/components/legal/LegalPageLayout.css`
- Based on Django template styles
- Gradient hero
- Sticky TOC
- Section styling with icons
- Mobile responsive

### Step 4: Create Individual Page Components
For each page:
1. Create component file (e.g., `PrivacyPolicy.jsx`)
2. Fetch corresponding JSON
3. Pass data to `LegalPageLayout`
4. Handle loading states

### Step 5: Add Routes
**File**: `frontend/src/App.jsx`
```jsx
import PrivacyPolicy from './pages/PrivacyPolicy';
import TermsOfService from './pages/TermsOfService';
import CookiePolicy from './pages/CookiePolicy';
import EditorialGuidelines from './pages/EditorialGuidelines';
import EthicsPolicy from './pages/EthicsPolicy';

// Add routes:
<Route path="/privacy-policy" element={<PrivacyPolicy />} />
<Route path="/terms-of-service" element={<TermsOfService />} />
<Route path="/cookie-policy" element={<CookiePolicy />} />
<Route path="/editorial-guidelines" element={<EditorialGuidelines />} />
<Route path="/ethics-policy" element={<EthicsPolicy />} />
```

### Step 6: Test All Pages
- Verify JSON loading
- Check TOC navigation
- Test responsive design
- Verify all links work

---

## Design Specifications

### Colors
- **Hero Background**: `linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%)`
- **Background**: `#f8f9fa`
- **Text**: `#2d3748`
- **Headings**: `#1a202c`
- **Accent**: `#7e22ce` (purple from brand)
- **Last Updated Badge**: `rgba(255, 255, 255, 0.2)`

### Typography
- **Hero Title**: 42px, font-weight: 800
- **Section Titles**: 28px, font-weight: 700
- **Subsection Titles**: 20px, font-weight: 600
- **Body Text**: 16px, line-height: 1.7

### Layout
- **Container Max Width**: 1200px
- **TOC Width**: 280px (sticky)
- **Grid Gap**: 40px
- **Content Padding**: 40px
- **Border Radius**: 12px

### Icons
Use Font Awesome icons for sections (already in project):
- Privacy: `fa-shield-alt`
- Terms: `fa-file-contract`
- Cookie: `fa-cookie`
- Editorial: `fa-newspaper`
- Ethics: `fa-balance-scale`

---

## File Structure

```
frontend/src/
├── components/
│   └── legal/
│       ├── LegalPageLayout.jsx
│       └── LegalPageLayout.css
├── pages/
│   ├── PrivacyPolicy.jsx
│   ├── TermsOfService.jsx
│   ├── CookiePolicy.jsx
│   ├── EditorialGuidelines.jsx
│   └── EthicsPolicy.jsx
└── App.jsx (update routes)

frontend/public/
└── administration/
    ├── privacy_polity.json
    ├── terms_of_service.json
    ├── cookee.json
    ├── guidemines.json
    └── ethics_policy.json
```

---

## Benefits

1. **Reusable**: Single layout component for all legal pages
2. **Maintainable**: Content in JSON, easy to update
3. **Consistent**: Same design across all pages
4. **SEO Friendly**: Proper meta tags and structured content
5. **Accessible**: Semantic HTML and ARIA labels
6. **Responsive**: Mobile-first design

---

## Next Steps

1. Review and approve this plan
2. Copy JSON files to frontend/public
3. Create shared LegalPageLayout component
4. Create individual page components
5. Update App.jsx routes
6. Test and deploy
