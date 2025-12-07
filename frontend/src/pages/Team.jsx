import { useState, useEffect } from 'react';
import './Team.css';

function Team() {
  const [teamMembers, setTeamMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetch('http://localhost:8000/api/team/')
      .then(response => response.json())
      .then(data => {
        setTeamMembers(data.results || data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error loading team members:', error);
        setLoading(false);
      });
  }, []);

  const getRoleIcon = (role) => {
    const icons = {
      'editor': 'user-edit',
      'reporter': 'newspaper',
      'analyst': 'chart-line',
      'contributor': 'pen-fancy',
      'photographer': 'camera',
    };
    return icons[role] || 'user';
  };

  const filteredMembers = filter === 'all' 
    ? teamMembers 
    : teamMembers.filter(member => member.role === filter);

  const roles = [...new Set(teamMembers.map(member => member.role))];

  if (loading) {
    return <div className="team-loading">Loading team members...</div>;
  }

  return (
    <div className="team-page">
      {/* Hero Section */}
      <section className="team-hero">
        <div className="team-hero__container">
          <h1 className="team-hero__title">Meet Our Team</h1>
          <p className="team-hero__subtitle">
            Our diverse team of journalists, editors, and analysts brings decades of combined 
            experience in news reporting and AI-powered analysis.
          </p>
        </div>
      </section>

      {/* Filter Section */}
      <div className="team-container">
        <div className="team-filters">
          <button 
            className={`team-filter ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            <i className="fas fa-users"></i>
            All Team ({teamMembers.length})
          </button>
          {roles.map(role => {
            const count = teamMembers.filter(m => m.role === role).length;
            return (
              <button 
                key={role}
                className={`team-filter ${filter === role ? 'active' : ''}`}
                onClick={() => setFilter(role)}
              >
                <i className={`fas fa-${getRoleIcon(role)}`}></i>
                {role.charAt(0).toUpperCase() + role.slice(1)}s ({count})
              </button>
            );
          })}
        </div>

        {/* Team Grid */}
        <div className="team-members">
          {filteredMembers.length === 0 ? (
            <div className="team-empty">
              <i className="fas fa-users"></i>
              <p>No team members found.</p>
            </div>
          ) : (
            <div className="team-grid">
              {filteredMembers.map((member) => (
                <div key={member.id} className="member-card">
                  <div className="member-card__photo">
                    {member.photo ? (
                      <img src={member.photo} alt={member.name} />
                    ) : (
                      <div className="member-card__placeholder">
                        <i className={`fas fa-${getRoleIcon(member.role)}`}></i>
                      </div>
                    )}
                    <div className="member-card__badge">
                      {member.role_display || member.role}
                    </div>
                  </div>
                  
                  <div className="member-card__content">
                    <h3 className="member-card__name">{member.name}</h3>
                    
                    {member.bio && (
                      <p className="member-card__bio">{member.bio}</p>
                    )}
                    
                    {member.article_count > 0 && (
                      <div className="member-card__stats">
                        <div className="member-stat">
                          <i className="fas fa-newspaper"></i>
                          <span>{member.article_count} Article{member.article_count !== 1 ? 's' : ''}</span>
                        </div>
                        {member.joined_date && (
                          <div className="member-stat">
                            <i className="fas fa-calendar-alt"></i>
                            <span>Since {new Date(member.joined_date).getFullYear()}</span>
                          </div>
                        )}
                      </div>
                    )}
                    
                    {(member.twitter_url || member.linkedin_url || member.email) && (
                      <div className="member-card__social">
                        {member.twitter_url && (
                          <a href={member.twitter_url} target="_blank" rel="noopener noreferrer" title="Twitter">
                            <i className="fab fa-twitter"></i>
                          </a>
                        )}
                        {member.linkedin_url && (
                          <a href={member.linkedin_url} target="_blank" rel="noopener noreferrer" title="LinkedIn">
                            <i className="fab fa-linkedin-in"></i>
                          </a>
                        )}
                        {member.email && (
                          <a href={`mailto:${member.email}`} title="Email">
                            <i className="fas fa-envelope"></i>
                          </a>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* CTA Section */}
      <section className="team-cta">
        <div className="team-cta__container">
          <h2 className="team-cta__title">Join Our Team</h2>
          <p className="team-cta__text">
            We're always looking for talented journalists, analysts, and contributors 
            to join our mission of delivering unbiased, AI-powered news analysis.
          </p>
          <a href="/careers" className="team-cta__button">
            View Open Positions
            <i className="fas fa-arrow-right"></i>
          </a>
        </div>
      </section>
    </div>
  );
}

export default Team;
