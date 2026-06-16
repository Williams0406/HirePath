import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";
import { jobs } from "@/lib/mockData";

export default function AdminJobsPage() {
  return (
    <AppShell admin>
      <div className="page">
        <PageHeader eyebrow="Admin" title="Vacantes importadas" />
        <div className="card">
          <table className="table">
            <thead><tr><th>Cargo</th><th>Empresa</th><th>Fuente</th><th>Estado</th></tr></thead>
            <tbody>
              {jobs.map((job) => (
                <tr key={job.id}><td>{job.title}</td><td>{job.company}</td><td>{job.source}</td><td><span className="status">ACTIVE</span></td></tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </AppShell>
  );
}
