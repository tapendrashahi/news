# Image Upload and Dynamic News Guide

## Overview
Your NewsPortal project now fully supports image uploads for news articles and displays them dynamically across all pages.

## Features Implemented

### 1. **Dynamic Image Display**
- All news articles can now have associated images
- Images are displayed on:
  - Home page (hero section, secondary cards, article grid)
  - Category pages
  - News detail pages
- Fallback to placeholder images when no image is uploaded

### 2. **Admin Interface**
- Upload images directly in the Django admin
- Preview images while editing
- Thumbnail view in the news list
- Image field supports: JPG, PNG, GIF, WebP

### 3. **Media Configuration**
- Images are stored in: `media/news_images/`
- Media URL: `/media/`
- All media files are served during development

## How to Use

### Adding News with Images via Admin

1. **Access Admin Panel**
   - Go to: http://127.0.0.1:8000/admin/
   - Login with your superuser credentials

2. **Create/Edit News Article**
   - Navigate to: News → Add News (or edit existing)
   - Fill in the fields:
     - **Title**: Your news headline
     - **Content**: Full article text
     - **Category**: Choose from Business, Political, Tech, or Education
     - **Image**: Click "Choose File" and select an image

3. **Image Guidelines**
   - **Recommended size**: 1200x600px for featured articles
   - **Minimum size**: 400x300px
   - **Format**: JPG, PNG, GIF, or WebP
   - **Max file size**: Depends on your server settings (default ~2.5MB)

4. **Save**
   - Click "Save" or "Save and continue editing"
   - The image will be uploaded to `media/news_images/`

### Viewing News

1. **Home Page**: http://127.0.0.1:8000/
   - Hero section shows the latest news with uploaded images
   - Secondary cards display the 2nd and 3rd latest news
   - Article grid shows more news items

2. **Category Pages**: http://127.0.0.1:8000/category/business/
   - Shows all news filtered by category
   - Each article displays its uploaded image

3. **News Detail**: http://127.0.0.1:8000/news/1/
   - Full article view with large featured image
   - Complete content display

## Template Changes

### Image Display Logic
The templates now use conditional logic to show images:

```django
{% if news.image %}
    <img src="{{ news.image.url }}" alt="{{ news.title }}">
{% else %}
    <img src="[fallback_placeholder_url]" alt="{{ news.title }}">
{% endif %}
```

### Category Display
Category labels now use the proper display name:
```django
{{ news.get_category_display|upper }}
```

## Database Schema

The `News` model includes:
```python
class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## Testing the Features

### Test Image Upload
1. Go to admin: http://127.0.0.1:8000/admin/
2. Create a new news article with an image
3. View the home page to see it displayed
4. Check the category page for that category
5. Click through to the detail page

### Test Without Images
1. Create a news article without uploading an image
2. Verify placeholder images are shown
3. No errors should occur

## Image Storage

- **Location**: `c:\projects\gis\media\news_images\`
- Images are automatically organized in this folder
- Filenames are preserved (with conflict resolution)

## Tips for Best Results

1. **Use High-Quality Images**
   - Clear, professional photos work best
   - Proper aspect ratios prevent distortion

2. **Optimize Images Before Upload**
   - Compress large images to reduce load time
   - Use tools like TinyPNG or ImageOptim

3. **Image Aspect Ratios**
   - Hero/Featured: 2:1 (e.g., 1200x600)
   - Article cards: 4:3 (e.g., 400x300)
   - Detail page: 2.4:1 (e.g., 1200x500)

4. **Consistent Style**
   - Use similar image styles across articles
   - Consider color schemes that match your brand

## Troubleshooting

### Images Not Displaying
- Check that the server is running
- Verify `MEDIA_URL` and `MEDIA_ROOT` in settings.py
- Ensure images are in `media/news_images/`
- Check browser console for 404 errors

### Upload Errors
- Ensure Pillow is installed: `pip install Pillow`
- Check file permissions on the media folder
- Verify file size isn't too large

### Image Quality Issues
- Upload higher resolution images
- Check image compression settings
- Use appropriate file formats (JPG for photos, PNG for graphics)

## Next Steps

Consider adding:
- Image thumbnails generation for better performance
- Image cropping/resizing on upload
- Multiple images per article (gallery)
- Image alt text field for better SEO
- Image caption field

## Support

For more information, see:
- Django ImageField docs: https://docs.djangoproject.com/en/5.2/ref/models/fields/#imagefield
- Pillow documentation: https://pillow.readthedocs.io/
- Media files guide: https://docs.djangoproject.com/en/5.2/topics/files/
