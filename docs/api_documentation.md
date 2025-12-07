# Django REST API Documentation

## Overview
This document provides detailed information about the REST API endpoints for the Django News application.

## Base URL
```
Development: http://localhost:8000/api
Production: https://yourdomain.com/api
```

## API Endpoints

### News Endpoints

#### 1. List All News
**GET** `/api/news/`

Retrieve a paginated list of all news articles.

**Query Parameters:**
- `page` (integer, optional): Page number (default: 1)
- `page_size` (integer, optional): Items per page (default: 10, max: 100)
- `category` (string, optional): Filter by category
- `search` (string, optional): Search in title and content

**Response:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/news/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Breaking News: Technology Advances",
      "slug": "breaking-news-technology-advances",
      "excerpt": "Brief summary of the news article...",
      "content": "Full content of the article...",
      "category": "tech",
      "author": {
        "id": 1,
        "name": "John Doe",
        "role": "tech_editor"
      },
      "image": "http://localhost:8000/media/news_images/article1.jpg",
      "views": 1250,
      "created_at": "2025-12-01T10:30:00Z",
      "updated_at": "2025-12-01T10:30:00Z",
      "published": true,
      "comment_count": 15,
      "share_count": 45
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `400 Bad Request`: Invalid parameters

---

#### 2. Get News Detail
**GET** `/api/news/{slug}/`

Retrieve a single news article by slug.

**Path Parameters:**
- `slug` (string, required): News article slug

**Response:**
```json
{
  "id": 1,
  "title": "Breaking News: Technology Advances",
  "slug": "breaking-news-technology-advances",
  "excerpt": "Brief summary...",
  "content": "Full content...",
  "category": "tech",
  "author": {
    "id": 1,
    "name": "John Doe",
    "role": "tech_editor",
    "photo": "http://localhost:8000/media/team_photos/john.jpg",
    "bio": "Tech editor with 10 years experience"
  },
  "image": "http://localhost:8000/media/news_images/article1.jpg",
  "views": 1251,
  "created_at": "2025-12-01T10:30:00Z",
  "updated_at": "2025-12-01T10:30:00Z",
  "published": true,
  "comments": [
    {
      "id": 1,
      "author": "Jane Smith",
      "email": "jane@example.com",
      "content": "Great article!",
      "created_at": "2025-12-01T11:00:00Z",
      "approved": true
    }
  ],
  "related_news": [
    {
      "id": 2,
      "title": "Related Article",
      "slug": "related-article",
      "excerpt": "Brief summary...",
      "image": "http://localhost:8000/media/news_images/article2.jpg"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: News article not found

---

#### 3. Get News by Category
**GET** `/api/news/category/{category}/`

Retrieve news articles filtered by category.

**Path Parameters:**
- `category` (string, required): Category name (business, political, tech, education, sports)

**Query Parameters:**
- `page` (integer, optional): Page number
- `page_size` (integer, optional): Items per page

**Response:**
```json
{
  "category": "tech",
  "count": 45,
  "results": [
    // ... news articles
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `400 Bad Request`: Invalid category

---

#### 4. Search News
**GET** `/api/news/search/`

Search news articles by keywords.

**Query Parameters:**
- `q` (string, required): Search query
- `page` (integer, optional): Page number
- `page_size` (integer, optional): Items per page

**Response:**
```json
{
  "query": "technology",
  "count": 23,
  "results": [
    // ... matching news articles
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `400 Bad Request`: Missing or invalid query parameter

---

#### 5. Increment News Views
**POST** `/api/news/{id}/view/`

Increment the view count for a news article.

**Path Parameters:**
- `id` (integer, required): News article ID

**Response:**
```json
{
  "views": 1252
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: News article not found

---

### Comment Endpoints

#### 6. Add Comment
**POST** `/api/news/{id}/comment/`

Add a comment to a news article.

**Path Parameters:**
- `id` (integer, required): News article ID

**Request Body:**
```json
{
  "author": "John Smith",
  "email": "john@example.com",
  "content": "This is an insightful article. Thanks for sharing!"
}
```

**Response:**
```json
{
  "id": 10,
  "author": "John Smith",
  "email": "john@example.com",
  "content": "This is an insightful article. Thanks for sharing!",
  "created_at": "2025-12-04T15:30:00Z",
  "approved": false
}
```

**Status Codes:**
- `201 Created`: Comment created successfully
- `400 Bad Request`: Validation error
- `404 Not Found`: News article not found

---

#### 7. Get Comments
**GET** `/api/news/{id}/comments/`

Get all approved comments for a news article.

**Path Parameters:**
- `id` (integer, required): News article ID

**Response:**
```json
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "author": "Jane Doe",
      "content": "Great article!",
      "created_at": "2025-12-01T12:00:00Z"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: News article not found

---

### Share Endpoints

#### 8. Increment Share Count
**POST** `/api/news/{id}/share/`

Increment the share count for a news article.

**Path Parameters:**
- `id` (integer, required): News article ID

**Request Body:**
```json
{
  "platform": "facebook"
}
```

**Response:**
```json
{
  "share_count": 46,
  "platform_shares": {
    "facebook": 20,
    "twitter": 15,
    "linkedin": 11
  }
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: News article not found

---

### Team Endpoints

#### 9. List Team Members
**GET** `/api/team/`

Retrieve all active team members.

**Response:**
```json
{
  "count": 12,
  "results": [
    {
      "id": 1,
      "name": "John Doe",
      "role": "tech_editor",
      "role_display": "Tech Editor",
      "bio": "Tech editor with 10 years of experience...",
      "photo": "http://localhost:8000/media/team_photos/john.jpg",
      "email": "john@newssite.com",
      "twitter_url": "https://twitter.com/johndoe",
      "linkedin_url": "https://linkedin.com/in/johndoe",
      "is_active": true,
      "article_count": 145
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success

---

#### 10. Get Team Member Detail
**GET** `/api/team/{id}/`

Retrieve a single team member's details.

**Path Parameters:**
- `id` (integer, required): Team member ID

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "role": "tech_editor",
  "role_display": "Tech Editor",
  "bio": "Tech editor with 10 years of experience...",
  "photo": "http://localhost:8000/media/team_photos/john.jpg",
  "email": "john@newssite.com",
  "twitter_url": "https://twitter.com/johndoe",
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "is_active": true,
  "articles": [
    {
      "id": 1,
      "title": "Latest Tech News",
      "slug": "latest-tech-news",
      "created_at": "2025-12-01T10:30:00Z"
    }
  ],
  "article_count": 145
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Team member not found

---

### Category Endpoints

#### 11. Get All Categories
**GET** `/api/categories/`

Retrieve all news categories with article counts.

**Response:**
```json
{
  "categories": [
    {
      "name": "business",
      "display_name": "Business",
      "count": 45,
      "description": "Business and finance news"
    },
    {
      "name": "political",
      "display_name": "Political",
      "count": 67,
      "description": "Political news and analysis"
    },
    {
      "name": "tech",
      "display_name": "Technology",
      "count": 89,
      "description": "Technology and innovation news"
    },
    {
      "name": "education",
      "display_name": "Education",
      "count": 34,
      "description": "Education sector news"
    },
    {
      "name": "sports",
      "display_name": "Sports",
      "count": 56,
      "description": "Sports news and updates"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success

---

### Subscriber Endpoints

#### 12. Subscribe to Newsletter
**POST** `/api/subscribe/`

Subscribe an email to the newsletter.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "Successfully subscribed to newsletter",
  "email": "user@example.com"
}
```

**Status Codes:**
- `201 Created`: Successfully subscribed
- `400 Bad Request`: Invalid email or already subscribed

---

#### 13. Unsubscribe from Newsletter
**POST** `/api/unsubscribe/`

Unsubscribe an email from the newsletter.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "Successfully unsubscribed from newsletter"
}
```

**Status Codes:**
- `200 OK`: Successfully unsubscribed
- `404 Not Found`: Email not found in subscribers

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message here",
  "detail": "Detailed error description",
  "status_code": 400
}
```

### Common Error Codes
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

---

## Rate Limiting

API endpoints are rate-limited to prevent abuse:
- **Unauthenticated users**: 100 requests per hour
- **Authenticated users**: 1000 requests per hour

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1701784800
```

---

## Pagination

All list endpoints support pagination:

**Request:**
```
GET /api/news/?page=2&page_size=20
```

**Response:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/news/?page=3",
  "previous": "http://localhost:8000/api/news/?page=1",
  "results": [...]
}
```

---

## Filtering & Sorting

### Filtering
```
GET /api/news/?category=tech&published=true
```

### Sorting
```
GET /api/news/?ordering=-created_at
GET /api/news/?ordering=title
```

Multiple fields:
```
GET /api/news/?ordering=-views,-created_at
```

---

## CORS Configuration

CORS is enabled for:
- Development: `http://localhost:3000`
- Production: Configure in Django settings

Allowed methods: GET, POST, PUT, PATCH, DELETE, OPTIONS

---

## Authentication (Future)

### JWT Authentication
Will be implemented in future updates:

```
POST /api/auth/login/
POST /api/auth/logout/
POST /api/auth/refresh/
```

---

## Webhook Events (Future)

Future webhook support for:
- New article published
- Comment added
- Trending article alert

---

## API Versioning

Current version: `v1`

Future versions will be accessible via:
```
/api/v2/news/
```

---

## Example Usage

### JavaScript (Axios)
```javascript
import axios from 'axios';

// Get news list
const getNews = async () => {
  const response = await axios.get('http://localhost:8000/api/news/');
  return response.data;
};

// Get news detail
const getNewsDetail = async (slug) => {
  const response = await axios.get(`http://localhost:8000/api/news/${slug}/`);
  return response.data;
};

// Add comment
const addComment = async (newsId, commentData) => {
  const response = await axios.post(
    `http://localhost:8000/api/news/${newsId}/comment/`,
    commentData
  );
  return response.data;
};

// Subscribe to newsletter
const subscribe = async (email) => {
  const response = await axios.post(
    'http://localhost:8000/api/subscribe/',
    { email }
  );
  return response.data;
};
```

### Python (Requests)
```python
import requests

# Get news list
response = requests.get('http://localhost:8000/api/news/')
news_list = response.json()

# Get news detail
response = requests.get('http://localhost:8000/api/news/breaking-news/')
news_detail = response.json()

# Add comment
comment_data = {
    'author': 'John Doe',
    'email': 'john@example.com',
    'content': 'Great article!'
}
response = requests.post(
    'http://localhost:8000/api/news/1/comment/',
    json=comment_data
)
```

---

## Testing

### Using cURL
```bash
# Get news list
curl http://localhost:8000/api/news/

# Get news detail
curl http://localhost:8000/api/news/breaking-news/

# Add comment
curl -X POST http://localhost:8000/api/news/1/comment/ \
  -H "Content-Type: application/json" \
  -d '{"author":"John","email":"john@example.com","content":"Great!"}'

# Subscribe
curl -X POST http://localhost:8000/api/subscribe/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'
```

---

**Last Updated**: December 4, 2025  
**API Version**: 1.0  
**Status**: In Development
