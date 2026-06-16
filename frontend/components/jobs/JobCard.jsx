import Link from "next/link";

export default function JobCard({ job }) {
  return (
    <article className="card job-card">
      <div>
        <div className="toolbar" style={{ marginBottom: 10 }}>
          <span className="status blue">{job.modality}</span>
          <span className="status">{job.source}</span>
        </div>
        <h3>{job.title}</h3>
        <p className="muted">{job.company || job.external_company_detail?.name || "Empresa externa"} · {job.location}</p>
        <p className="muted">{job.seniority} · {job.salary || job.salary_text || "Salario no publicado"}</p>
        <div className="toolbar">
          <Link className="button secondary" href={`/jobs/${job.id}`}>Ver detalle</Link>
          <Link className="button" href={`/cvs?job=${job.id}`}>Generar CV</Link>
        </div>
      </div>
      <div className="score">{job.score || 72}%</div>
    </article>
  );
}
