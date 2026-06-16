import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";
import InterviewPrepCard from "@/components/interviews/InterviewPrepCard";
import { interviews } from "@/lib/mockData";

export default function InterviewsPage() {
  return (
    <AppShell>
      <div className="page">
        <PageHeader eyebrow="Entrevistas" title="Preparacion personalizada" />
        <div className="grid cols-2">
          {interviews.map((prep) => <InterviewPrepCard key={prep.id} prep={prep} />)}
        </div>
      </div>
    </AppShell>
  );
}
