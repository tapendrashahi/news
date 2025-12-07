import { useState, useEffect } from 'react';
import './About.css';

function About() {
  const [aboutData, setAboutData] = useState(null);
  const [teamMembers, setTeamMembers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch about content from JSON
    fetch('/administration/about.json')
      .then(response => response.json())
      .then(data => {
        setAboutData(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error loading about content:', error);
        setLoading(false);
      });

    // Fetch team members from API
    fetch('http://localhost:8000/api/team/')
      .then(response => response.json())
      .then(data => setTeamMembers(data.results || data))
      .catch(error => console.error('Error loading team members:', error));
  }, []);

  if (loading || !aboutData) {
    return <div className="about-loading">Loading...</div>;
  }

  return (
    <div className="about-page">
      {/* Hero Section */}
      <section className="about-hero">
        <div className="about-hero__container">
          <h1 className="about-hero__title">{aboutData.hero.title}</h1>
          <p className="about-hero__subtitle">{aboutData.hero.subtitle}</p>
        </div>
      </section>

      {/* Main Content */}
      <div className="about-container">
        {/* Mission Section */}
        <section className="about-section">
          <div className="about-section__header">
            <div className="about-section__icon">
              <i className="fas fa-bullseye"></i>
            </div>
            <h2 className="about-section__title">{aboutData.mission.title}</h2>
          </div>
          {aboutData.mission.content.map((paragraph, index) => (
            <p key={index} className="about-section__text">{paragraph}</p>
          ))}
        </section>

        {/* Values Section */}
        <section className="about-section">
          <div className="about-section__header">
            <div className="about-section__icon">
              <i className="fas fa-gem"></i>
            </div>
            <h2 className="about-section__title">{aboutData.values.title}</h2>
          </div>
          <div className="values-grid">
            {aboutData.values.items.map((value, index) => (
              <div key={index} className="value-card">
                <div className="value-card__icon">
                  <i className={`fas fa-${value.icon}`}></i>
                </div>
                <h3 className="value-card__title">{value.title}</h3>
                <p className="value-card__text">{value.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Story Section */}
        <section className="about-section">
          <div className="about-section__header">
            <div className="about-section__icon">
              <i className="fas fa-book-open"></i>
            </div>
            <h2 className="about-section__title">{aboutData.story.title}</h2>
          </div>
          {aboutData.story.content.map((paragraph, index) => (
            <p key={index} className="about-section__text">{paragraph}</p>
          ))}
        </section>
      </div>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="stats-container">
          <div className="stats-grid">
            {aboutData.stats.map((stat, index) => (
              <div key={index} className="stat-item">
                <div className="stat-item__number">{stat.value}</div>
                <div className="stat-item__label">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <div className="about-container">
        <section className="about-section">
          <div className="about-section__header">
            <div className="about-section__icon">
              <i className="fas fa-users"></i>
            </div>
            <h2 className="about-section__title">{aboutData.team.title}</h2>
          </div>
          <p className="about-section__text" style={{ marginBottom: '40px' }}>
            {aboutData.team.description}
          </p>
          <div className="team-grid">
            {(teamMembers.length > 0 ? teamMembers : aboutData.team.fallbackMembers).map((member, index) => (
              <div key={index} className="team-card">
                <div className="team-card__photo">
                  {member.photo ? (
                    <img src={member.photo} alt={member.name} />
                  ) : (
                    <i className={`fas fa-${member.icon || 'user'}`}></i>
                  )}
                </div>
                <div className="team-card__info">
                  <h3 className="team-card__name">{member.name}</h3>
                  <p className="team-card__role">{member.role || member.position || 'Team Member'}</p>
                  {(member.twitter_url || member.linkedin_url || member.email) && (
                    <div className="team-card__social">
                      {member.twitter_url && (
                        <a href={member.twitter_url} target="_blank" rel="noopener noreferrer">
                          <i className="fab fa-twitter"></i>
                        </a>
                      )}
                      {member.linkedin_url && (
                        <a href={member.linkedin_url} target="_blank" rel="noopener noreferrer">
                          <i className="fab fa-linkedin-in"></i>
                        </a>
                      )}
                      {member.email && (
                        <a href={`mailto:${member.email}`}>
                          <i className="fas fa-envelope"></i>
                        </a>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

export default About;
