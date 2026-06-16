import Link from "next/link";

export default function InterviewPrepCard({ prep }) {
  return (
    <article className="card pad">
      <span className="status amber">Preparacion</span>
      <h3>{prep.title}</h3>
      <p className="muted">{prep.company}</p>
      <p>{prep.advice}</p>
      <Link className="button secondary" href={`/interviews/${prep.id}`}>Abrir</Link>
    </article>
  );
}
