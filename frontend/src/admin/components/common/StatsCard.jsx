import './StatsCard.css';

const StatsCard = ({ title, value, icon, color, subtitle }) => {
  return (
    <div className="stats-card" style={{ borderTopColor: color }}>
      <div className="stats-card__icon" style={{ backgroundColor: `${color}15` }}>
        <span style={{ color }}>{icon}</span>
      </div>
      <div className="stats-card__content">
        <h3 className="stats-card__title">{title}</h3>
        <div className="stats-card__value">{value}</div>
        {subtitle && <p className="stats-card__subtitle">{subtitle}</p>}
      </div>
    </div>
  );
};

export default StatsCard;
