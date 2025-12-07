import { useState, useEffect } from 'react';
import './Careers.css';

function Careers() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedJob, setSelectedJob] = useState(null);
  const [showApplicationModal, setShowApplicationModal] = useState(false);
  const [filterDepartment, setFilterDepartment] = useState('all');
  const [filterType, setFilterType] = useState('all');
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: '',
    linkedin_url: '',
    portfolio_url: '',
    years_of_experience: '',
    cover_letter: '',
    resume: null
  });
  const [submitStatus, setSubmitStatus] = useState({ type: '', message: '' });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = () => {
    fetch('http://localhost:8000/api/jobs/')
      .then(response => response.json())
      .then(data => {
        setJobs(data.results || data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error loading jobs:', error);
        setLoading(false);
      });
  };

  const handleApplyClick = (job) => {
    setSelectedJob(job);
    setShowApplicationModal(true);
    setSubmitStatus({ type: '', message: '' });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    setFormData(prev => ({
      ...prev,
      resume: e.target.files[0]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setSubmitStatus({ type: '', message: '' });

    const formDataToSend = new FormData();
    formDataToSend.append('job_opening', selectedJob.id);
    formDataToSend.append('full_name', formData.full_name);
    formDataToSend.append('email', formData.email);
    formDataToSend.append('phone', formData.phone);
    formDataToSend.append('linkedin_url', formData.linkedin_url);
    formDataToSend.append('portfolio_url', formData.portfolio_url);
    formDataToSend.append('years_of_experience', formData.years_of_experience || 0);
    formDataToSend.append('cover_letter', formData.cover_letter);
    if (formData.resume) {
      formDataToSend.append('resume', formData.resume);
    }

    try {
      const response = await fetch('http://localhost:8000/api/applications/', {
        method: 'POST',
        body: formDataToSend
      });

      if (response.ok) {
        setSubmitStatus({
          type: 'success',
          message: 'Application submitted successfully! We will review your application and get back to you soon.'
        });
        setFormData({
          full_name: '',
          email: '',
          phone: '',
          linkedin_url: '',
          portfolio_url: '',
          years_of_experience: '',
          cover_letter: '',
          resume: null
        });
        setTimeout(() => {
          setShowApplicationModal(false);
        }, 3000);
      } else {
        const error = await response.json();
        setSubmitStatus({
          type: 'error',
          message: error.message || 'Failed to submit application. Please try again.'
        });
      }
    } catch (error) {
      setSubmitStatus({
        type: 'error',
        message: 'Network error. Please check your connection and try again.'
      });
    } finally {
      setSubmitting(false);
    }
  };

  const filteredJobs = jobs.filter(job => {
    const departmentMatch = filterDepartment === 'all' || job.department === filterDepartment;
    const typeMatch = filterType === 'all' || job.employment_type === filterType;
    return departmentMatch && typeMatch;
  });

  const departments = [...new Set(jobs.map(job => job.department))];
  const types = [...new Set(jobs.map(job => job.employment_type))];

  if (loading) {
    return <div className="careers-loading">Loading job openings...</div>;
  }

  return (
    <div className="careers-page">
      {/* Hero Section */}
      <section className="careers-hero">
        <div className="careers-hero__container">
          <h1 className="careers-hero__title">Join Our Team</h1>
          <p className="careers-hero__subtitle">
            Help us shape the future of AI-powered journalism. We're looking for talented individuals
            who are passionate about news, technology, and making a difference.
          </p>
          <div className="careers-hero__stats">
            <div className="hero-stat">
              <div className="hero-stat__number">{jobs.length}</div>
              <div className="hero-stat__label">Open Positions</div>
            </div>
            <div className="hero-stat">
              <div className="hero-stat__number">{departments.length}</div>
              <div className="hero-stat__label">Departments</div>
            </div>
            <div className="hero-stat">
              <div className="hero-stat__number">Remote</div>
              <div className="hero-stat__label">Work Options</div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <div className="careers-container">
        {/* Filters */}
        <div className="careers-filters">
          <div className="filter-group">
            <label>Department:</label>
            <select value={filterDepartment} onChange={(e) => setFilterDepartment(e.target.value)}>
              <option value="all">All Departments</option>
              {departments.map(dept => (
                <option key={dept} value={dept}>
                  {jobs.find(j => j.department === dept)?.department_display}
                </option>
              ))}
            </select>
          </div>
          <div className="filter-group">
            <label>Type:</label>
            <select value={filterType} onChange={(e) => setFilterType(e.target.value)}>
              <option value="all">All Types</option>
              {types.map(type => (
                <option key={type} value={type}>
                  {jobs.find(j => j.employment_type === type)?.employment_type_display}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Job Listings */}
        <div className="careers-jobs">
          {filteredJobs.length === 0 ? (
            <div className="careers-empty">
              <i className="fas fa-briefcase"></i>
              <p>No job openings match your criteria.</p>
            </div>
          ) : (
            filteredJobs.map((job) => (
              <div key={job.id} className="job-card">
                <div className="job-card__header">
                  <div className="job-card__title-section">
                    <h3 className="job-card__title">{job.title}</h3>
                    <div className="job-card__meta">
                      <span className="job-badge job-badge--department">
                        <i className="fas fa-building"></i>
                        {job.department_display}
                      </span>
                      <span className="job-badge job-badge--type">
                        <i className="fas fa-clock"></i>
                        {job.employment_type_display}
                      </span>
                      <span className="job-badge job-badge--level">
                        <i className="fas fa-layer-group"></i>
                        {job.experience_level_display}
                      </span>
                      <span className="job-badge job-badge--location">
                        <i className="fas fa-map-marker-alt"></i>
                        {job.location}
                      </span>
                    </div>
                  </div>
                </div>

                <p className="job-card__description">{job.description}</p>

                <div className="job-card__details">
                  <div className="job-details__section">
                    <h4><i className="fas fa-tasks"></i> Responsibilities</h4>
                    <ul>
                      {job.responsibilities_list.slice(0, 3).map((resp, idx) => (
                        <li key={idx}>{resp}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="job-details__section">
                    <h4><i className="fas fa-check-circle"></i> Requirements</h4>
                    <ul>
                      {job.requirements_list.slice(0, 3).map((req, idx) => (
                        <li key={idx}>{req}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                {job.salary_range && (
                  <div className="job-card__salary">
                    <i className="fas fa-dollar-sign"></i>
                    <strong>Salary Range:</strong> {job.salary_range}
                  </div>
                )}

                <div className="job-card__footer">
                  <span className="job-card__date">
                    <i className="fas fa-calendar-alt"></i>
                    Posted {new Date(job.posted_date).toLocaleDateString()}
                  </span>
                  <button 
                    className="job-card__apply-btn"
                    onClick={() => handleApplyClick(job)}
                  >
                    Apply Now
                    <i className="fas fa-arrow-right"></i>
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Application Modal */}
      {showApplicationModal && (
        <div className="application-modal" onClick={() => setShowApplicationModal(false)}>
          <div className="application-modal__content" onClick={(e) => e.stopPropagation()}>
            <button 
              className="application-modal__close"
              onClick={() => setShowApplicationModal(false)}
            >
              <i className="fas fa-times"></i>
            </button>

            <h2 className="application-modal__title">
              Apply for {selectedJob?.title}
            </h2>

            {submitStatus.message && (
              <div className={`application-alert application-alert--${submitStatus.type}`}>
                <i className={`fas fa-${submitStatus.type === 'success' ? 'check-circle' : 'exclamation-circle'}`}></i>
                {submitStatus.message}
              </div>
            )}

            <form onSubmit={handleSubmit} className="application-form">
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="full_name">Full Name *</label>
                  <input
                    type="text"
                    id="full_name"
                    name="full_name"
                    value={formData.full_name}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="email">Email *</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="phone">Phone *</label>
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="years_of_experience">Years of Experience</label>
                  <input
                    type="number"
                    id="years_of_experience"
                    name="years_of_experience"
                    value={formData.years_of_experience}
                    onChange={handleInputChange}
                    min="0"
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="linkedin_url">LinkedIn Profile</label>
                <input
                  type="url"
                  id="linkedin_url"
                  name="linkedin_url"
                  value={formData.linkedin_url}
                  onChange={handleInputChange}
                  placeholder="https://linkedin.com/in/yourprofile"
                />
              </div>

              <div className="form-group">
                <label htmlFor="portfolio_url">Portfolio URL</label>
                <input
                  type="url"
                  id="portfolio_url"
                  name="portfolio_url"
                  value={formData.portfolio_url}
                  onChange={handleInputChange}
                  placeholder="https://yourportfolio.com"
                />
              </div>

              <div className="form-group">
                <label htmlFor="resume">Resume * (PDF, DOC, DOCX - Max 5MB)</label>
                <div className="file-input-wrapper">
                  <input
                    type="file"
                    id="resume"
                    name="resume"
                    onChange={handleFileChange}
                    accept=".pdf,.doc,.docx"
                    required
                  />
                  <div className="file-input-label">
                    <i className="fas fa-upload"></i>
                    {formData.resume ? formData.resume.name : 'Choose file...'}
                  </div>
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="cover_letter">Cover Letter</label>
                <textarea
                  id="cover_letter"
                  name="cover_letter"
                  value={formData.cover_letter}
                  onChange={handleInputChange}
                  rows="6"
                  placeholder="Tell us why you're interested in this position..."
                ></textarea>
              </div>

              <div className="form-actions">
                <button 
                  type="button" 
                  className="btn-cancel"
                  onClick={() => setShowApplicationModal(false)}
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="btn-submit"
                  disabled={submitting}
                >
                  {submitting ? (
                    <>
                      <i className="fas fa-spinner fa-spin"></i>
                      Submitting...
                    </>
                  ) : (
                    <>
                      Submit Application
                      <i className="fas fa-paper-plane"></i>
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Careers;
