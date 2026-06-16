import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";

export default function AdminAILogsPage() {
  return (
    <AppShell admin>
      <div className="page">
        <PageHeader eyebrow="Admin" title="Logs de IA" />
        <div className="card">
          <table className="table">
            <thead><tr><th>Tarea</th><th>Proveedor</th><th>Tokens</th><th>Estado</th></tr></thead>
            <tbody>
              {["JOB_MATCH", "CV_GENERATION", "INTERVIEW_PREP"].map((task, index) => (
                <tr key={task}><td>{task}</td><td>groq</td><td>{1200 + index * 430}</td><td><span className="status">OK</span></td></tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </AppShell>
  );
}
