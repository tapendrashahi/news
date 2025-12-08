# Admin API Documentation

## Base URL
All admin API endpoints are prefixed with `/api/admin/`

---

## Authentication

### Login
**POST** `/api/admin/auth/login/`

Login to admin panel.

**Request Body:**
```json
{
  "username": "admin",
  "password": "password123"
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User",
    "is_staff": true,
    "is_superuser": true
  }
}
```

**Response (Error - 401):**
```json
{
  "error": "Invalid username or password"
}
```

---

### Logout
**POST** `/api/admin/auth/logout/`

Logout from admin panel.

**Headers:**
- Cookie: sessionid (required)

**Response (200):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

### Get Current User
**GET** `/api/admin/auth/user/`

Get current authenticated admin user information.

**Headers:**
- Cookie: sessionid (required)

**Response (200):**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "first_name": "Admin",
  "last_name": "User",
  "is_staff": true,
  "is_superuser": true,
  "team_member": {
    "id": 1,
    "name": "Admin User",
    "role": "editor",
    "bio": "...",
    ...
  }
}
```

---

## Dashboard

### Get Dashboard Statistics
**GET** `/api/admin/dashboard/stats/`

Get all dashboard statistics including totals, recent activity, and breakdowns.

**Response (200):**
```json
{
  "total_news": 150,
  "total_team": 8,
  "total_comments": 342,
  "pending_comments": 12,
  "total_subscribers": 1250,
  "active_subscribers": 1180,
  "news_last_month": 23,
  "comments_last_month": 87,
  "recent_news": [...],
  "recent_comments": [...],
  "categories": [
    {"code": "tech", "name": "Technology", "count": 45},
    ...
  ],
  "top_shared": [
    {"news": {"id": 1, "title": "...", "slug": "..."}, "shares": 250},
    ...
  ]
}
```

---

## News Management

### List All News
**GET** `/api/admin/news/`

Get all news articles with filtering options.

**Query Parameters:**
- `category` (optional): Filter by category code
- `visibility` (optional): Filter by visibility (public/draft/private)
- `search` (optional): Search in title, content, excerpt
- `page` (optional): Page number for pagination
- `page_size` (optional): Items per page

**Response (200):**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/admin/news/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Breaking News",
      "slug": "breaking-news",
      "content": "...",
      "excerpt": "...",
      "category": "tech",
      "category_display": "Technology",
      "author": {...},
      "image": "/media/news_images/...",
      "created_at": "2025-12-01T10:00:00Z",
      "updated_at": "2025-12-01T10:00:00Z",
      "publish_date": "2025-12-01",
      "meta_description": "...",
      "tags": "ai, technology",
      "tags_list": ["ai", "technology"],
      "visibility": "public",
      "visibility_display": "Public",
      "comment_count": 15,
      "approved_comment_count": 12,
      "total_shares": 45
    },
    ...
  ]
}
```

---

### Get News Detail
**GET** `/api/admin/news/{id}/`

Get detailed information about a specific news article.

**Response (200):**
```json
{
  "id": 1,
  "title": "Breaking News",
  ...
}
```

---

### Create News
**POST** `/api/admin/news/`

Create a new news article.

**Request Body (multipart/form-data or JSON):**
```json
{
  "title": "New Article Title",
  "slug": "new-article-title",
  "content": "Full article content...",
  "excerpt": "Short excerpt...",
  "category": "tech",
  "tags": "ai, technology",
  "author_id": 1,
  "meta_description": "SEO description",
  "visibility": "public",
  "publish_date": "2025-12-08",
  "image": (file upload)
}
```

**Response (201):**
```json
{
  "id": 151,
  "title": "New Article Title",
  ...
}
```

---

### Update News
**PUT/PATCH** `/api/admin/news/{id}/`

Update an existing news article.

**Request Body:** Same as create

**Response (200):**
```json
{
  "id": 1,
  "title": "Updated Title",
  ...
}
```

---

### Delete News
**DELETE** `/api/admin/news/{id}/`

Delete a news article.

**Response (204):** No content

---

### Upload News Image
**POST** `/api/admin/news/{id}/upload_image/`

Upload or update image for a news article.

**Request Body (multipart/form-data):**
- `image`: Image file

**Response (200):**
```json
{
  "id": 1,
  "title": "...",
  "image": "/media/news_images/new_image.jpg",
  ...
}
```

---

## Team Management

### List Team Members
**GET** `/api/admin/team/`

Get all team members.

**Response (200):**
```json
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "name": "John Doe",
      "role": "editor",
      "role_display": "Editor",
      "bio": "...",
      "photo": "/media/team_photos/...",
      "email": "john@example.com",
      "twitter_url": "https://twitter.com/...",
      "linkedin_url": "https://linkedin.com/in/...",
      "is_active": true,
      "order": 1,
      "joined_date": "2024-01-15",
      "article_count": 23,
      "recent_articles": [...]
    },
    ...
  ]
}
```

---

### Create Team Member
**POST** `/api/admin/team/`

Create a new team member.

**Request Body (multipart/form-data or JSON):**
```json
{
  "name": "Jane Smith",
  "role": "writer",
  "bio": "Experienced tech writer...",
  "email": "jane@example.com",
  "twitter_url": "https://twitter.com/janesmith",
  "linkedin_url": "https://linkedin.com/in/janesmith",
  "order": 5,
  "photo": (file upload)
}
```

**Response (201):**
```json
{
  "id": 9,
  "name": "Jane Smith",
  ...
}
```

---

### Update Team Member
**PUT/PATCH** `/api/admin/team/{id}/`

Update team member details.

---

### Delete Team Member
**DELETE** `/api/admin/team/{id}/`

Delete a team member.

---

### Get Team Member Articles
**GET** `/api/admin/team/{id}/articles/`

Get all articles written by a specific team member.

**Query Parameters:**
- `page` (optional): Page number
- `page_size` (optional): Items per page (default: 10)

**Response (200):**
```json
{
  "count": 23,
  "results": [...]
}
```

---

## Comments Moderation

### List Comments
**GET** `/api/admin/comments/`

Get all comments with filtering.

**Query Parameters:**
- `filter` (optional): all/pending/approved (default: all)
- `page` (optional): Page number
- `page_size` (optional): Items per page

**Response (200):**
```json
{
  "count": 342,
  "results": [
    {
      "id": 1,
      "news": 5,
      "news_id": 5,
      "news_title": "Article Title",
      "name": "Commenter Name",
      "email": "commenter@example.com",
      "text": "Great article!",
      "created_at": "2025-12-07T15:30:00Z",
      "is_approved": false
    },
    ...
  ]
}
```

---

### Approve Comment
**POST** `/api/admin/comments/{id}/approve/`

Approve a pending comment.

**Response (200):**
```json
{
  "success": true,
  "message": "Comment approved successfully",
  "comment": {...}
}
```

---

### Unapprove Comment
**POST** `/api/admin/comments/{id}/unapprove/`

Unapprove an approved comment.

**Response (200):**
```json
{
  "success": true,
  "message": "Comment unapproved successfully",
  "comment": {...}
}
```

---

### Delete Comment
**DELETE** `/api/admin/comments/{id}/`

Delete a comment.

**Response (204):** No content

---

## Subscribers Management

### List Subscribers
**GET** `/api/admin/subscribers/`

Get all newsletter subscribers.

**Query Parameters:**
- `status` (optional): active/unsubscribed
- `search` (optional): Search in email or name
- `page` (optional): Page number
- `page_size` (optional): Items per page

**Response (200):**
```json
{
  "count": 1250,
  "results": [
    {
      "id": 1,
      "email": "subscriber@example.com",
      "name": "Subscriber Name",
      "is_active": true,
      "subscribed_at": "2025-11-15T10:00:00Z",
      "unsubscribed_at": null
    },
    ...
  ]
}
```

---

### Get Subscriber Statistics
**GET** `/api/admin/subscribers/stats/`

Get subscriber statistics.

**Response (200):**
```json
{
  "total_subscribers": 1250,
  "active_subscribers": 1180,
  "unsubscribed_count": 70,
  "new_this_month": 45
}
```

---

### Create Subscriber
**POST** `/api/admin/subscribers/`

Add a new subscriber.

**Request Body:**
```json
{
  "email": "new@example.com",
  "name": "New Subscriber"
}
```

**Response (201):**
```json
{
  "id": 1251,
  "email": "new@example.com",
  "name": "New Subscriber",
  "is_active": true,
  "subscribed_at": "2025-12-08T12:00:00Z",
  "unsubscribed_at": null
}
```

---

### Toggle Subscriber Status
**POST** `/api/admin/subscribers/{id}/toggle/`

Toggle subscriber active/inactive status.

**Response (200):**
```json
{
  "success": true,
  "message": "Subscriber email@example.com has been activated",
  "subscriber": {...}
}
```

---

### Delete Subscriber
**DELETE** `/api/admin/subscribers/{id}/`

Delete a subscriber.

**Response (204):** No content

---

### Bulk Delete Subscribers
**POST** `/api/admin/subscribers/bulk_delete/`

Delete multiple subscribers at once.

**Request Body:**
```json
{
  "ids": [1, 2, 3, 4, 5]
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "5 subscriber(s) deleted successfully",
  "deleted_count": 5
}
```

---

### Export Subscribers to CSV
**GET** `/api/admin/subscribers/export/`

Export all subscribers to CSV file.

**Query Parameters:** Same as list endpoint for filtering

**Response (200):** CSV file download
```csv
Email,Name,Status,Subscribed At,Unsubscribed At
subscriber@example.com,Name,Active,2025-11-15 10:00,
...
```

---

## Reports & Analytics

### Get Analytics Data
**GET** `/api/admin/reports/analytics/`

Get comprehensive analytics and reports data.

**Query Parameters:**
- `days` (optional): Number of days for period stats (default: 30)

**Response (200):**
```json
{
  "days": 30,
  "total_news": 150,
  "news_period": 23,
  "category_stats": [
    {
      "code": "tech",
      "name": "Technology",
      "count": 45,
      "percentage": 30.0
    },
    ...
  ],
  "total_comments": 342,
  "approved_comments": 330,
  "pending_comments": 12,
  "comments_period": 87,
  "approval_rate": 96,
  "share_stats": [
    {"platform": "Facebook", "count": 450},
    {"platform": "Twitter", "count": 380},
    {"platform": "Linkedin", "count": 220},
    {"platform": "Email", "count": 150}
  ],
  "top_authors": [
    {"id": 1, "name": "John Doe", "count": 35},
    {"id": 2, "name": "Jane Smith", "count": 28},
    ...
  ],
  "most_commented": [
    {
      "news": {"id": 5, "title": "...", "slug": "..."},
      "count": 45
    },
    ...
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Error message describing what went wrong"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "error": "You do not have permission to access the admin area"
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Testing the API

### Using cURL

**Login:**
```bash
curl -X POST http://localhost:8000/api/admin/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}' \
  -c cookies.txt
```

**Get Dashboard Stats:**
```bash
curl http://localhost:8000/api/admin/dashboard/stats/ \
  -b cookies.txt
```

**Create News Article:**
```bash
curl -X POST http://localhost:8000/api/admin/news/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "New Article",
    "slug": "new-article",
    "content": "Article content here...",
    "category": "tech",
    "visibility": "public"
  }'
```

### Using Postman/Thunder Client

1. Create a POST request to `/api/admin/auth/login/`
2. Set Content-Type to `application/json`
3. Send login credentials in body
4. Save the session cookie
5. Use the cookie for subsequent requests

---

## Notes

- All admin endpoints require authentication (except login)
- Session-based authentication is used
- CSRF protection is enabled for POST/PUT/PATCH/DELETE requests
- File uploads use multipart/form-data
- Pagination is available on list endpoints
- Filtering and search are supported where applicable
