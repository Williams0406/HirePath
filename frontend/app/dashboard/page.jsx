import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";
import KpiCard from "@/components/dashboard/KpiCard";
import JobCard from "@/components/jobs/JobCard";
import { applications, jobs, metrics } from "@/lib/mockData";

export default function DashboardPage() {
  return (
    <AppShell>
      <div className="page">
        <PageHeader eyebrow="Panel" title="Centro de control" description="Resumen operativo de busqueda, CVs y entrevistas." />
        <div className="grid cols-4">
          {metrics.map((item) => <KpiCard key={item.label} {...item} />)}
        </div>
        <div className="grid cols-2" style={{ marginTop: 18 }}>
          <section className="grid">
            <h2 className="compact-title">Vacantes destacadas</h2>
            {jobs.slice(0, 2).map((job) => <JobCard key={job.id} job={job} />)}
          </section>
          <section className="card pad">
            <h2 className="compact-title">Ultimas postulaciones</h2>
            <table className="table">
              <tbody>
                {applications.map((item) => (
                  <tr key={item.id}>
                    <td>{item.title}<br /><span className="muted">{item.company}</span></td>
                    <td><span className="status blue">{item.status}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        </div>
      </div>
    </AppShell>
  );
}
