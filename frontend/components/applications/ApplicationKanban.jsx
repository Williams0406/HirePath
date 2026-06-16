const columns = [
  ["DETECTED", "Detectada"],
  ["MATCHED", "Compatible"],
  ["CV_GENERATED", "CV generado"],
  ["APPLIED", "Postulada"],
  ["INTERVIEW", "Entrevista"],
];

export default function ApplicationKanban({ applications }) {
  return (
    <div className="kanban">
      {columns.map(([key, label]) => (
        <section key={key} className="kanban-column">
          <h3>{label}</h3>
          <div className="grid">
            {applications
              .filter((item) => item.status === key)
              .map((item) => (
                <article key={item.id} className="card pad">
                  <strong>{item.title}</strong>
                  <p className="muted">{item.company}</p>
                  <span className="status blue">{item.date}</span>
                </article>
              ))}
          </div>
        </section>
      ))}
    </div>
  );
}
