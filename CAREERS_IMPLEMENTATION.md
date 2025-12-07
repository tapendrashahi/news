# Careers Page Implementation

## Overview
Complete careers page with job listings and resume upload functionality.

## Features Implemented

### Backend (Django)

#### 1. Database Models (`news/models.py`)
- **JobOpening Model**:
  - Title, department, location, employment type, experience level
  - Description, responsibilities, requirements
  - Salary range, active status
  - Posted date, application deadline
  
- **JobApplication Model**:
  - Links to job opening
  - Applicant information (name, email, phone)
  - Resume upload (PDF, DOC, DOCX - max 5MB)
  - Cover letter, LinkedIn, portfolio URLs
  - Years of experience
  - Application status tracking

#### 2. Admin Interface (`news/admin.py`)
- **JobOpeningAdmin**:
  - List view with department, type, level filters
  - Application count display
  - Fieldsets for organized editing
  
- **JobApplicationAdmin**:
  - Application tracking with status updates
  - Resume download functionality
  - Bulk actions (approve, reject, schedule interview)
  - Status filtering and search

#### 3. API Endpoints (`news/api.py`, `news/serializers.py`)
- **GET /api/jobs/** - List all active job openings
  - Filter by department, type, experience level
  - Search by title, description, requirements
  - Returns formatted responsibilities and requirements lists
  
- **POST /api/applications/** - Submit job application
  - Multipart form data for file upload
  - Resume validation (file type and size)
  - Automatic status tracking

### Frontend (React)

#### 1. Careers Page Component (`frontend/src/pages/Careers.jsx`)
- **Hero Section**:
  - Job statistics (open positions, departments)
  - Compelling call-to-action
  
- **Job Filters**:
  - Filter by department
  - Filter by employment type
  
- **Job Listings**:
  - Card-based layout
  - Displays all job details
  - Badges for department, type, level, location
  - Expandable responsibilities and requirements
  
- **Application Modal**:
  - Full application form
  - Resume file upload with drag-drop support
  - Form validation
  - Success/error messaging
  - Auto-close after successful submission

#### 2. Styling (`frontend/src/pages/Careers.css`)
- Dark gradient hero matching site design
- Purple accent colors (#7e22ce)
- Responsive grid layout
- Hover effects and animations
- Mobile-optimized design

## File Structure

```
Backend:
├── news/
│   ├── models.py (JobOpening, JobApplication)
│   ├── admin.py (Admin interfaces)
│   ├── serializers.py (API serializers)
│   ├── api.py (ViewSets)
│   └── api_urls.py (Routes)

Frontend:
├── src/
│   ├── pages/
│   │   ├── Careers.jsx
│   │   └── Careers.css
│   └── routes.jsx (Route: /careers)

Utilities:
└── create_sample_jobs.py (Test data generator)
```

## Setup Instructions

### 1. Run Migrations
```bash
python manage.py migrate
```

### 2. Create Sample Jobs (Optional)
```bash
python create_sample_jobs.py
```

### 3. Access Admin Panel
Navigate to `http://localhost:8000/admin/` and manage:
- Job Openings under "News" section
- Job Applications to review submissions

### 4. Frontend Route
The careers page is accessible at: `http://localhost:3000/careers`

## API Usage

### List Jobs
```bash
GET /api/jobs/
GET /api/jobs/?department=editorial
GET /api/jobs/?employment_type=full_time
GET /api/jobs/?search=editor
```

### Submit Application
```bash
POST /api/applications/
Content-Type: multipart/form-data

{
  "job_opening": 1,
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "years_of_experience": 5,
  "resume": <file>,
  "cover_letter": "...",
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "portfolio_url": "https://johndoe.com"
}
```

## Resume Upload Configuration

### Allowed File Types
- PDF (.pdf)
- Microsoft Word (.doc, .docx)

### File Size Limit
- Maximum: 5MB

### Storage Location
- Resumes stored in: `media/resumes/YYYY/MM/`
- Example: `media/resumes/2025/12/johndoe_resume.pdf`

## Admin Features

### Job Opening Management
- Create/edit job postings
- Set application deadlines
- Activate/deactivate positions
- View application count per job

### Application Tracking
- Review submitted applications
- Download resumes
- Update application status:
  - Submitted (default)
  - Under Review
  - Interview Scheduled
  - Rejected
  - Accepted
- Add internal notes
- Bulk status updates

## Customization

### Adding New Departments
Edit `DEPARTMENT_CHOICES` in `news/models.py`:
```python
DEPARTMENT_CHOICES = [
    ('editorial', 'Editorial'),
    ('technology', 'Technology'),
    ('your_new_dept', 'Your New Department'),
]
```

### Adding New Employment Types
Edit `EMPLOYMENT_TYPE_CHOICES` in `news/models.py`:
```python
EMPLOYMENT_TYPE_CHOICES = [
    ('full_time', 'Full Time'),
    ('your_new_type', 'Your New Type'),
]
```

## Testing

### Test Job Creation
```bash
python create_sample_jobs.py
```

### Test API
```bash
curl http://localhost:8000/api/jobs/
```

### Test Application Submission
1. Navigate to http://localhost:3000/careers
2. Click "Apply Now" on any job
3. Fill out the form
4. Upload a resume
5. Submit

### Verify in Admin
1. Go to http://localhost:8000/admin/
2. Check "Job Applications"
3. View submitted application
4. Download resume

## Security Considerations

- File type validation (only PDF, DOC, DOCX)
- File size validation (max 5MB)
- Resume files stored securely in media folder
- CSRF protection enabled
- Form input sanitization

## Future Enhancements

- Email notifications on application submission
- Application status tracking for candidates
- Advanced filtering (salary range, location)
- Saved job applications for logged-in users
- Application analytics and reporting
- Interview scheduling integration
- Video resume support
- Application deadline notifications
