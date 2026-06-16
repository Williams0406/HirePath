export default function CVPreview({ title = "CV adaptado" }) {
  return (
    <div className="card cv-preview">
      <h2>{title}</h2>
      <p className="muted">Resumen profesional orientado al puesto seleccionado.</p>
      <hr style={{ border: 0, borderTop: "1px solid var(--line)", margin: "20px 0" }} />
      <section>
        <h3>Experiencia relevante</h3>
        <p>Proyecto o rol seleccionado desde el perfil profesional real.</p>
        <p>Logros medibles y herramientas usadas.</p>
      </section>
      <section>
        <h3>Skills</h3>
        <div className="toolbar">
          <span className="status blue">Django</span>
          <span className="status blue">Next.js</span>
          <span className="status blue">SQL</span>
          <span className="status blue">Analisis</span>
        </div>
      </section>
      <section style={{ marginTop: 24 }}>
        <h3>Educacion y certificaciones</h3>
        <p>Elementos seleccionados para esta vacante.</p>
      </section>
    </div>
  );
}
