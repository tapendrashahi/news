#!/usr/bin/env python
"""
Script to create sample job openings for testing
Run with: python create_sample_jobs.py
"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gis.settings')
django.setup()

from news.models import JobOpening

# Clear existing jobs
JobOpening.objects.all().delete()

# Create sample jobs
jobs = [
    {
        'title': 'Senior News Editor',
        'department': 'editorial',
        'location': 'New York, NY (Remote)',
        'employment_type': 'full_time',
        'experience_level': 'senior',
        'description': 'We are seeking an experienced Senior News Editor to lead our editorial team in delivering high-quality, AI-enhanced news content.',
        'responsibilities': '''Lead editorial team and set content strategy
Review and edit news articles for accuracy
Collaborate with AI analysts on story development
Manage publication schedules
Mentor junior writers and editors''',
        'requirements': '''5+ years of experience in news editing
Strong understanding of journalism ethics
Experience with digital publishing platforms
Excellent communication skills
Bachelor's degree in Journalism or related field''',
        'salary_range': '$80,000 - $120,000',
        'is_active': True,
        'application_deadline': datetime.now().date() + timedelta(days=30)
    },
    {
        'title': 'AI Data Analyst',
        'department': 'technology',
        'location': 'San Francisco, CA (Hybrid)',
        'employment_type': 'full_time',
        'experience_level': 'mid',
        'description': 'Join our technology team to build and maintain AI systems that power our news analysis platform.',
        'responsibilities': '''Develop machine learning models for news analysis
Process and analyze large datasets
Collaborate with editorial team on AI features
Monitor system performance and optimization
Create data visualizations and reports''',
        'requirements': '''3+ years of experience in data science or ML
Proficiency in Python and data libraries (pandas, scikit-learn)
Experience with NLP and text analysis
Strong statistical analysis skills
Master's degree in Computer Science or related field''',
        'salary_range': '$90,000 - $130,000',
        'is_active': True,
        'application_deadline': datetime.now().date() + timedelta(days=45)
    },
    {
        'title': 'Business Reporter',
        'department': 'business',
        'location': 'Remote',
        'employment_type': 'full_time',
        'experience_level': 'mid',
        'description': 'Cover business and economic news with the support of our AI-powered research tools.',
        'responsibilities': '''Research and write business news stories
Conduct interviews with industry leaders
Analyze financial data and market trends
Break complex business topics into clear stories
Collaborate with data analysts on investigative pieces''',
        'requirements': '''3+ years of business journalism experience
Strong financial literacy
Excellent writing and communication skills
Ability to meet tight deadlines
Bachelor's degree in Journalism, Business, or Economics''',
        'salary_range': '$60,000 - $85,000',
        'is_active': True,
        'application_deadline': datetime.now().date() + timedelta(days=25)
    },
    {
        'title': 'UX/UI Designer',
        'department': 'design',
        'location': 'Austin, TX (Hybrid)',
        'employment_type': 'full_time',
        'experience_level': 'mid',
        'description': 'Design beautiful and intuitive user experiences for our news platform and mobile apps.',
        'responsibilities': '''Create wireframes, mockups, and prototypes
Design responsive web and mobile interfaces
Conduct user research and usability testing
Maintain and evolve design system
Collaborate with developers on implementation''',
        'requirements': '''3+ years of UX/UI design experience
Proficiency in Figma, Sketch, or Adobe XD
Strong portfolio demonstrating user-centered design
Understanding of web accessibility standards
Bachelor's degree in Design or related field''',
        'salary_range': '$70,000 - $100,000',
        'is_active': True,
        'application_deadline': datetime.now().date() + timedelta(days=20)
    },
    {
        'title': 'Content Marketing Intern',
        'department': 'marketing',
        'location': 'Remote',
        'employment_type': 'internship',
        'experience_level': 'entry',
        'description': 'Gain hands-on experience in content marketing and social media at a cutting-edge news organization.',
        'responsibilities': '''Assist with social media content creation
Help manage editorial content calendar
Support email marketing campaigns
Conduct competitor and market research
Create marketing analytics reports''',
        'requirements': '''Currently enrolled in Marketing, Communications, or related program
Strong writing and communication skills
Familiarity with social media platforms
Basic understanding of SEO principles
Creative mindset and attention to detail''',
        'salary_range': '$20/hour',
        'is_active': True,
        'application_deadline': datetime.now().date() + timedelta(days=15)
    },
    {
        'title': 'Political Correspondent',
        'department': 'editorial',
        'location': 'Washington, DC (On-site)',
        'employment_type': 'full_time',
        'experience_level': 'senior',
        'description': 'Cover political news and policy from the nation\'s capital with AI-assisted research capabilities.',
        'responsibilities': '''Cover Congress, White House, and federal agencies
Develop and maintain political sources
Analyze policy proposals and legislation
Provide live coverage of major political events
Collaborate with data team on election analysis''',
        'requirements': '''5+ years of political journalism experience
Strong network in DC political circles
Deep understanding of US government and politics
Excellent on-camera and writing skills
Bachelor's degree in Journalism, Political Science, or related field''',
        'salary_range': '$75,000 - $110,000',
        'is_active': True,
        'application_deadline': datetime.now().date() + timedelta(days=40)
    }
]

# Create jobs
created_count = 0
for job_data in jobs:
    job = JobOpening.objects.create(**job_data)
    created_count += 1
    print(f"✓ Created: {job.title} ({job.get_department_display()})")

print(f"\n✅ Successfully created {created_count} sample job openings!")
