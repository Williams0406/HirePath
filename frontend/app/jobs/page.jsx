import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";
import JobCard from "@/components/jobs/JobCard";
import JobFilters from "@/components/jobs/JobFilters";
import { jobs } from "@/lib/mockData";

export default function JobsPage() {
  return (
    <AppShell>
      <div className="page">
        <PageHeader eyebrow="Vacantes" title="Oportunidades encontradas" actions={<button className="button">Importar URL</button>} />
        <JobFilters />
        <div className="grid" style={{ marginTop: 18 }}>
          {jobs.map((job) => <JobCard key={job.id} job={job} />)}
        </div>
      </div>
    </AppShell>
  );
}
