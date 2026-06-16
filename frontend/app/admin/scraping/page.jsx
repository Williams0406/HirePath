import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";

export default function AdminScrapingPage() {
  return (
    <AppShell admin>
      <div className="page">
        <PageHeader eyebrow="Admin" title="Scraping runs" actions={<button className="button">Ejecutar</button>} />
        <div className="card">
          <table className="table">
            <thead><tr><th>Fuente</th><th>Estado</th><th>Encontradas</th><th>Creadas</th></tr></thead>
            <tbody>
              <tr><td>LinkedIn</td><td><span className="status">SUCCESS</span></td><td>120</td><td>34</td></tr>
              <tr><td>Computrabajo</td><td><span className="status amber">PARTIAL</span></td><td>80</td><td>12</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </AppShell>
  );
}
