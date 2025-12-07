# Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │         React Frontend (Port 3000)          │
        ├─────────────────────────────────────────────┤
        │  ┌──────────────────────────────────────┐   │
        │  │         React Router v6              │   │
        │  └──────────────────────────────────────┘   │
        │  ┌──────────────────────────────────────┐   │
        │  │         React Query                  │   │
        │  │      (Server State Management)       │   │
        │  └──────────────────────────────────────┘   │
        │  ┌──────────────────────────────────────┐   │
        │  │           Components                 │   │
        │  │  - Layout (Header, Footer)           │   │
        │  │  - Pages (Home, Detail, Category)    │   │
        │  │  - News Components                   │   │
        │  └──────────────────────────────────────┘   │
        │  ┌──────────────────────────────────────┐   │
        │  │        Services (Axios)              │   │
        │  │  - newsService                       │   │
        │  │  - teamService                       │   │
        │  └──────────────────────────────────────┘   │
        └─────────────────────────────────────────────┘
                              │
                              │ HTTP/REST API
                              ▼
        ┌─────────────────────────────────────────────┐
        │      Django Backend (Port 8000)             │
        ├─────────────────────────────────────────────┤
        │  ┌──────────────────────────────────────┐   │
        │  │      Django REST Framework           │   │
        │  │         API Endpoints                │   │
        │  └──────────────────────────────────────┘   │
        │  ┌──────────────────────────────────────┐   │
        │  │         Serializers                  │   │
        │  │  - NewsSerializer                    │   │
        │  │  - TeamMemberSerializer              │   │
        │  │  - CommentSerializer                 │   │
        │  └──────────────────────────────────────┘   │
        │  ┌──────────────────────────────────────┐   │
        │  │           Models                     │   │
        │  │  - News                              │   │
        │  │  - TeamMember                        │   │
        │  │  - Comment                           │   │
        │  │  - Subscriber                        │   │
        │  └──────────────────────────────────────┘   │
        │  ┌──────────────────────────────────────┐   │
        │  │         Django Admin                 │   │
        │  └──────────────────────────────────────┘   │
        └─────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │            SQLite Database                  │
        │  - news_news                                │
        │  - news_teammember                          │
        │  - news_comment                             │
        │  - news_subscriber                          │
        └─────────────────────────────────────────────┘
```

## Data Flow

### 1. User Requests News List

```
User Browser
    │
    │ 1. Navigate to "/"
    ▼
React Router
    │
    │ 2. Load Home component
    ▼
Home.jsx (Page)
    │
    │ 3. useQuery hook
    ▼
newsService.getNews()
    │
    │ 4. HTTP GET /api/news/
    ▼
Django REST API
    │
    │ 5. Serialize data
    ▼
NewsSerializer
    │
    │ 6. Query database
    ▼
News Model → SQLite
    │
    │ 7. Return JSON
    ▼
React Query (Cache)
    │
    │ 8. Update UI
    ▼
Home.jsx (Render)
    │
    ▼
User Browser (Display)
```

### 2. User Views News Detail

```
User Browser
    │
    │ 1. Click news article
    ▼
React Router
    │
    │ 2. Navigate to /news/:slug
    ▼
NewsDetail.jsx
    │
    │ 3. useQuery with slug
    ▼
newsService.getNewsDetail(slug)
    │
    │ 4. HTTP GET /api/news/:slug/
    ▼
Django REST API
    │
    │ 5. Fetch related data (author, comments)
    ▼
Database
    │
    │ 6. Return detailed JSON
    ▼
NewsDetail.jsx (Render)
```

### 3. User Adds Comment

```
User Browser
    │
    │ 1. Submit comment form
    ▼
CommentForm.jsx
    │
    │ 2. Handle submit
    ▼
commentService.addComment(data)
    │
    │ 3. HTTP POST /api/news/:id/comment/
    ▼
Django REST API
    │
    │ 4. Validate data
    ▼
CommentSerializer
    │
    │ 5. Save to database
    ▼
Comment Model → SQLite
    │
    │ 6. Return new comment
    ▼
React Query (Invalidate cache)
    │
    │ 7. Refetch comments
    ▼
CommentList.jsx (Update)
```

## Component Hierarchy

```
App
│
├─ Router
│   │
│   └─ Routes
│       │
│       └─ Layout
│           │
│           ├─ Header
│           │   └─ Navbar
│           │
│           ├─ Main Content (Outlet)
│           │   │
│           │   ├─ Home
│           │   │   ├─ NewsList
│           │   │   │   └─ NewsCard (multiple)
│           │   │   │       ├─ Image
│           │   │   │       ├─ CategoryBadge
│           │   │   │       └─ ShareButtons
│           │   │   └─ Pagination
│           │   │
│           │   ├─ NewsDetail
│           │   │   ├─ NewsHeader
│           │   │   ├─ NewsContent
│           │   │   ├─ ShareButtons
│           │   │   ├─ CommentList
│           │   │   │   └─ Comment (multiple)
│           │   │   ├─ CommentForm
│           │   │   └─ RelatedNews
│           │   │
│           │   ├─ Category
│           │   │   └─ NewsList
│           │   │       └─ NewsCard (filtered)
│           │   │
│           │   ├─ Search
│           │   │   ├─ SearchBar
│           │   │   └─ SearchResults
│           │   │
│           │   ├─ About
│           │   │   ├─ TeamGrid
│           │   │   │   └─ TeamMemberCard (multiple)
│           │   │   └─ NewsletterForm
│           │   │
│           │   └─ NotFound
│           │
│           └─ Footer
│               ├─ SocialLinks
│               └─ Newsletter
│
└─ QueryClientProvider
    └─ (All queries cached here)
```

## File Dependencies

```
src/index.jsx
    └─ imports App.jsx
        ├─ imports routes.jsx
        │   ├─ imports Layout.jsx
        │   │   ├─ imports Header.jsx
        │   │   └─ imports Footer.jsx
        │   ├─ imports Home.jsx
        │   │   └─ uses newsService.js
        │   ├─ imports NewsDetail.jsx
        │   │   └─ uses newsService.js
        │   ├─ imports Category.jsx
        │   ├─ imports Search.jsx
        │   ├─ imports About.jsx
        │   └─ imports NotFound.jsx
        └─ imports styles/index.css

services/
    ├─ api.js (Axios instance)
    ├─ newsService.js
    ├─ teamService.js
    └─ commentService.js
        └─ all import api.js
```

## API Endpoint Structure

```
/api/
├─ news/
│   ├─ GET    /                  # List all news
│   ├─ GET    /:slug/            # Get news detail
│   ├─ GET    /category/:cat/    # Filter by category
│   ├─ GET    /search/?q=query   # Search news
│   ├─ POST   /:id/view/         # Increment views
│   └─ POST   /:id/comment/      # Add comment
│
├─ team/
│   ├─ GET    /                  # List team members
│   └─ GET    /:id/              # Get team member detail
│
├─ categories/
│   └─ GET    /                  # Get all categories
│
└─ subscribe/
    ├─ POST   /                  # Subscribe to newsletter
    └─ POST   /unsubscribe/      # Unsubscribe
```

## Development vs Production

### Development Mode
```
┌─────────────┐         ┌─────────────┐
│   React     │◄────────│  Webpack    │
│   (3000)    │  Proxy  │  Dev Server │
└─────────────┘         └─────────────┘
      │
      │ API Calls
      ▼
┌─────────────┐
│   Django    │
│   (8000)    │
└─────────────┘
```

### Production Mode
```
┌─────────────────────────────┐
│         Django (8000)       │
│                             │
│  ┌───────────────────────┐  │
│  │  Static Files         │  │
│  │  - React Build        │  │
│  │  - CSS/JS Bundles     │  │
│  └───────────────────────┘  │
│                             │
│  ┌───────────────────────┐  │
│  │  API Endpoints        │  │
│  └───────────────────────┘  │
└─────────────────────────────┘
```

## State Management

```
┌──────────────────────────────────────┐
│         React Query Cache            │
├──────────────────────────────────────┤
│  Query Keys:                         │
│  - ['news'] → News list              │
│  - ['news', slug] → News detail      │
│  - ['categories'] → Category list    │
│  - ['team'] → Team members           │
│  - ['search', query] → Search results│
└──────────────────────────────────────┘
         ▲                    │
         │                    │
    Fetch data          Cached data
         │                    │
         │                    ▼
┌──────────────────────────────────────┐
│         React Components             │
└──────────────────────────────────────┘
```

## Security Flow

```
User Input
    │
    │ 1. Client-side validation
    ▼
React Form
    │
    │ 2. Submit to API
    ▼
Django REST Framework
    │
    │ 3. Serializer validation
    ▼
Django Model
    │
    │ 4. Database constraints
    ▼
SQLite
```

---

**Legend:**
- `→` Data flow
- `├─` Tree structure
- `│` Vertical connection
- `▼` Process flow
- `◄` Bidirectional
