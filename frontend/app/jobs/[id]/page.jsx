import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";
import { jobs } from "@/lib/mockData";

export default function JobDetailPage({ params }) {
  const job = jobs.find((item) => String(item.id) === String(params.id)) || jobs[0];

  return (
    <AppShell>
      <div className="page">
        <PageHeader
          eyebrow="Detalle"
          title={job.title}
          description={`${job.company} · ${job.location} · ${job.modality}`}
          actions={<><button className="button secondary">Analizar</button><button className="button">Generar CV</button></>}
        />
        <div className="grid cols-2">
          <section className="card pad">
            <div className="toolbar">
              <div className="score">{job.score}%</div>
              <div>
                <h2 className="compact-title">Compatibilidad</h2>
                <p className="muted">Skills coincidentes, experiencia relacionada y señales de riesgo.</p>
              </div>
            </div>
            <h3>Requisitos</h3>
            <p>Analisis, comunicacion con stakeholders, manejo de herramientas digitales y criterio de negocio.</p>
            <h3>Salario sugerido</h3>
            <p>{job.salary}</p>
          </section>
          <section className="card pad">
            <h2 className="compact-title">Empresa y trazabilidad</h2>
            <p className="muted">Fuente: {job.source}</p>
            <div className="empty-image" aria-label="Espacio reservado para imagen de vacante" />
          </section>
        </div>
      </div>
    </AppShell>
  );
}
