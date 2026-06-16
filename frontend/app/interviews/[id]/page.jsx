import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";
import { interviews } from "@/lib/mockData";

export default function InterviewDetailPage({ params }) {
  const prep = interviews.find((item) => String(item.id) === String(params.id)) || interviews[0];

  return (
    <AppShell>
      <div className="page">
        <PageHeader eyebrow="Guion" title={prep.title} description={`${prep.company} · Metodo STAR`} />
        <div className="grid cols-2">
          <section className="card pad">
            <h2 className="compact-title">Consejo general</h2>
            <p>{prep.advice}</p>
            <div className="empty-image" aria-label="Espacio reservado para imagen de entrevista" />
          </section>
          <section className="card pad">
            <h2 className="compact-title">Preguntas probables</h2>
            <div className="timeline">
              {prep.questions.map((question) => (
                <div className="timeline-item" key={question}>
                  <strong>{question}</strong>
                  <textarea className="textarea" style={{ marginTop: 10 }} />
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </AppShell>
  );
}
