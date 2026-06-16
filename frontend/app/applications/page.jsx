import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";
import ApplicationKanban from "@/components/applications/ApplicationKanban";
import { applications } from "@/lib/mockData";

export default function ApplicationsPage() {
  return (
    <AppShell>
      <div className="page">
        <PageHeader eyebrow="CRM laboral" title="Postulaciones" actions={<button className="button">Nueva</button>} />
        <ApplicationKanban applications={applications} />
      </div>
    </AppShell>
  );
}
