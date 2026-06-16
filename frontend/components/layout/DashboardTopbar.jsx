export default function DashboardTopbar({ title = "HirePath" }) {
  return (
    <header className="topbar">
      <input className="search" placeholder="Buscar vacantes, empresas o CVs" />
      <div className="toolbar">
        <button className="button icon secondary" title="Notificaciones">N</button>
        <button className="button icon secondary" title="Perfil">P</button>
      </div>
    </header>
  );
}
