export default function JobFilters() {
  return (
    <div className="card pad">
      <div className="toolbar">
        <input className="input" style={{ maxWidth: 280 }} placeholder="Buscar cargo o empresa" />
        <select className="select" style={{ maxWidth: 180 }} defaultValue="">
          <option value="">Modalidad</option>
          <option>REMOTE</option>
          <option>HYBRID</option>
          <option>ONSITE</option>
        </select>
        <select className="select" style={{ maxWidth: 180 }} defaultValue="">
          <option value="">Fuente</option>
          <option>LinkedIn</option>
          <option>Computrabajo</option>
          <option>Company Site</option>
        </select>
        <button className="button icon secondary" title="Filtrar">F</button>
      </div>
    </div>
  );
}
