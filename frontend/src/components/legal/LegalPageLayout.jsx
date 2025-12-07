import { useState, useEffect } from 'react';
import './LegalPageLayout.css';

function LegalPageLayout({ jsonFile, pageType }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeSection, setActiveSection] = useState('');

  useEffect(() => {
    fetch(`/administration/${jsonFile}`)
      .then(response => response.json())
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error loading content:', error);
        setLoading(false);
      });
  }, [jsonFile]);

  useEffect(() => {
    const handleScroll = () => {
      const sections = document.querySelectorAll('.legal-section');
      let current = '';

      sections.forEach(section => {
        const sectionTop = section.offsetTop;
        if (window.pageYOffset >= sectionTop - 100) {
          current = section.getAttribute('id');
        }
      });

      setActiveSection(current);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [data]);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      const offset = 80;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }
  };

  if (loading) {
    return <div className="legal-loading">Loading...</div>;
  }

  if (!data) {
    return <div className="legal-error">Failed to load content</div>;
  }

  return (
    <div className="legal-page">
      {/* Hero Section */}
      <section className="legal-hero">
        <div className="legal-hero__container">
          <h1 className="legal-hero__title">{data.metadata.title}</h1>
          <p className="legal-hero__subtitle">
            {pageType === 'privacy' && 'Your privacy is important to us'}
            {pageType === 'terms' && 'Please read these terms carefully'}
            {pageType === 'cookie' && 'How we use cookies on our website'}
            {pageType === 'editorial' && 'Our commitment to quality journalism'}
            {pageType === 'ethics' && 'Our ethical standards and principles'}
          </p>
          <div className="legal-hero__badge">
            <i className="far fa-calendar-alt"></i>
            Last Updated: {new Date(data.metadata.lastUpdated).toLocaleDateString('en-US', { 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            })}
          </div>
        </div>
      </section>

      {/* Main Content */}
      <div className="legal-container">
        {/* Table of Contents */}
        <aside className="legal-toc">
          <div className="legal-toc__card">
            <h2 className="legal-toc__title">
              <i className="fas fa-list"></i>
              Table of Contents
            </h2>
            <nav className="legal-toc__nav">
              <ul className="legal-toc__list">
                <li className="legal-toc__item">
                  <a
                    href="#introduction"
                    className={`legal-toc__link ${activeSection === 'introduction' ? 'active' : ''}`}
                    onClick={(e) => {
                      e.preventDefault();
                      scrollToSection('introduction');
                    }}
                  >
                    {data.introduction.title}
                  </a>
                </li>
                {data.sections.map((section) => (
                  <li key={section.id} className="legal-toc__item">
                    <a
                      href={`#${section.id}`}
                      className={`legal-toc__link ${activeSection === section.id ? 'active' : ''}`}
                      onClick={(e) => {
                        e.preventDefault();
                        scrollToSection(section.id);
                      }}
                    >
                      {section.title}
                    </a>
                  </li>
                ))}
              </ul>
            </nav>
          </div>
        </aside>

        {/* Content */}
        <main className="legal-content">
          {/* Introduction */}
          <section id="introduction" className="legal-section">
            <div className="legal-section__header">
              <h2 className="legal-section__title">{data.introduction.title}</h2>
            </div>
            <div className="legal-section__body">
              {data.introduction.content.map((paragraph, index) => (
                <p key={index} className="legal-text">{paragraph}</p>
              ))}
            </div>
          </section>

          {/* Sections */}
          {data.sections.map((section) => (
            <section key={section.id} id={section.id} className="legal-section">
              <div className="legal-section__header">
                {section.icon && (
                  <div className="legal-section__icon">
                    <i className={`fas fa-${section.icon}`}></i>
                  </div>
                )}
                <h2 className="legal-section__title">{section.title}</h2>
              </div>
              
              <div className="legal-section__body">
                {section.content && section.content.map((paragraph, index) => (
                  <p key={index} className="legal-text">{paragraph}</p>
                ))}

                {section.items && (
                  <ul className="legal-list">
                    {section.items.map((item, index) => (
                      <li key={index} className="legal-list__item">{item}</li>
                    ))}
                  </ul>
                )}

                {section.subsections && section.subsections.map((subsection, subIndex) => (
                  <div key={subIndex} className="legal-subsection">
                    <h3 className="legal-subsection__title">{subsection.title}</h3>
                    {subsection.content && (
                      <p className="legal-text">{subsection.content}</p>
                    )}
                    {subsection.items && (
                      <ul className="legal-list">
                        {subsection.items.map((item, itemIndex) => (
                          <li key={itemIndex} className="legal-list__item">{item}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                ))}
              </div>
            </section>
          ))}

          {/* Contact Section */}
          <section className="legal-contact">
            <div className="legal-contact__card">
              <h3 className="legal-contact__title">Questions or Concerns?</h3>
              <p className="legal-contact__text">
                If you have any questions about this {data.metadata.title.toLowerCase()}, 
                please contact us at{' '}
                <a href={`mailto:${data.metadata.companyEmail}`} className="legal-contact__link">
                  {data.metadata.companyEmail}
                </a>
              </p>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}

export default LegalPageLayout;
