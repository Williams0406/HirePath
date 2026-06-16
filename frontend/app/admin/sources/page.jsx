import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";

export default function AdminSourcesPage() {
  return (
    <AppShell admin>
      <div className="page">
        <PageHeader eyebrow="Admin" title="Fuentes de empleo" actions={<button className="button">Nueva fuente</button>} />
        <div className="grid cols-3">
          {["LinkedIn", "Computrabajo", "Indeed"].map((source) => (
            <article className="card pad" key={source}>
              <h3>{source}</h3>
              <span className="status">Activa</span>
            </article>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
