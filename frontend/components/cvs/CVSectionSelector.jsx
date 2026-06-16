const sections = ["Resumen", "Experiencia", "Proyectos", "Skills", "Educacion", "Certificaciones"];

export default function CVSectionSelector() {
  return (
    <div className="card pad">
      <h2 className="compact-title">Secciones</h2>
      <div className="grid">
        {sections.map((section) => (
          <label key={section} className="toolbar">
            <input type="checkbox" defaultChecked />
            <span>{section}</span>
          </label>
        ))}
      </div>
    </div>
  );
}
