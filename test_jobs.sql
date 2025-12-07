-- Sample SQL to insert test job openings
-- Run this after migrations using: python manage.py dbshell < test_jobs.sql

INSERT INTO news_jobopening (title, department, location, employment_type, experience_level, description, responsibilities, requirements, salary_range, is_active, posted_date, updated_date, application_deadline)
VALUES
('Senior News Editor', 'editorial', 'New York, NY (Remote)', 'full_time', 'senior', 
'We are seeking an experienced Senior News Editor to lead our editorial team in delivering high-quality, AI-enhanced news content.', 
'Lead editorial team and set content strategy
Review and edit news articles for accuracy
Collaborate with AI analysts on story development
Manage publication schedules
Mentor junior writers and editors',
'5+ years of experience in news editing
Strong understanding of journalism ethics
Experience with digital publishing platforms
Excellent communication skills
Bachelor''s degree in Journalism or related field',
'$80,000 - $120,000', true, datetime('now'), datetime('now'), date('now', '+30 days')),

('AI Data Analyst', 'technology', 'San Francisco, CA (Hybrid)', 'full_time', 'mid',
'Join our technology team to build and maintain AI systems that power our news analysis platform.',
'Develop machine learning models for news analysis
Process and analyze large datasets
Collaborate with editorial team on AI features
Monitor system performance
Create data visualizations',
'3+ years of experience in data science or ML
Proficiency in Python and data libraries
Experience with NLP and text analysis
Strong statistical analysis skills
Master''s degree in Computer Science or related field',
'$90,000 - $130,000', true, datetime('now'), datetime('now'), date('now', '+45 days')),

('Business Reporter', 'business', 'Remote', 'full_time', 'mid',
'Cover business and economic news with the support of our AI-powered research tools.',
'Research and write business news stories
Conduct interviews with industry leaders
Analyze financial data and market trends
Break complex business topics into clear stories
Collaborate with data analysts',
'3+ years of business journalism experience
Strong financial literacy
Excellent writing and communication skills
Ability to meet tight deadlines
Bachelor''s degree in Journalism, Business, or Economics',
'$60,000 - $85,000', true, datetime('now'), datetime('now'), date('now', '+25 days')),

('UX/UI Designer', 'design', 'Austin, TX (Hybrid)', 'full_time', 'mid',
'Design beautiful and intuitive user experiences for our news platform and mobile apps.',
'Create wireframes and prototypes
Design responsive web and mobile interfaces
Conduct user research and testing
Maintain design system
Collaborate with developers',
'3+ years of UX/UI design experience
Proficiency in Figma, Sketch, or Adobe XD
Strong portfolio demonstrating user-centered design
Understanding of web accessibility standards
Bachelor''s degree in Design or related field',
'$70,000 - $100,000', true, datetime('now'), datetime('now'), date('now', '+20 days')),

('Content Marketing Intern', 'marketing', 'Remote', 'internship', 'entry',
'Gain hands-on experience in content marketing and social media at a cutting-edge news organization.',
'Assist with social media content creation
Help manage content calendar
Support email marketing campaigns
Conduct competitor research
Create marketing reports',
'Currently enrolled in Marketing, Communications, or related program
Strong writing and communication skills
Familiarity with social media platforms
Basic understanding of SEO
Creative mindset and attention to detail',
'$20/hour', true, datetime('now'), datetime('now'), date('now', '+15 days'));
