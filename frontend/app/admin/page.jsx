import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";
import KpiCard from "@/components/dashboard/KpiCard";
import { adminMetrics } from "@/lib/mockData";

export default function AdminPage() {
  return (
    <AppShell admin>
      <div className="page">
        <PageHeader eyebrow="Admin" title="Monitoreo global" />
        <div className="grid cols-4">
          {adminMetrics.map((item) => <KpiCard key={item.label} {...item} />)}
        </div>
        <div className="grid cols-2" style={{ marginTop: 18 }}>
          <div className="card pad">
            <h2 className="compact-title">Actividad IA</h2>
            <div className="empty-image" aria-label="Espacio reservado para grafico administrativo" />
          </div>
          <div className="card pad">
            <h2 className="compact-title">Fuentes externas</h2>
            <table className="table">
              <tbody>
                {["LinkedIn", "Computrabajo", "Company Site"].map((source) => (
                  <tr key={source}><td>{source}</td><td><span className="status">Activa</span></td></tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
