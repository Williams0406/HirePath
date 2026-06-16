export default function KpiCard({ label, value, hint }) {
  return (
    <div className="card pad metric">
      <span className="muted">{label}</span>
      <strong className="metric-value">{value}</strong>
      {hint ? <span className="muted">{hint}</span> : null}
    </div>
  );
}
