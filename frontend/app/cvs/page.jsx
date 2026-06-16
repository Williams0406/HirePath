import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";
import { cvItems } from "@/lib/mockData";

export default function CVsPage() {
  return (
    <AppShell>
      <div className="page">
        <PageHeader eyebrow="CV" title="CVs generados" actions={<button className="button">Nuevo CV</button>} />
        <div className="grid cols-2">
          {cvItems.map((item) => (
            <article className="card pad" key={item.id}>
              <span className="status blue">{item.status}</span>
              <h3>{item.title}</h3>
              <p className="muted">{item.job} · {item.updated}</p>
              <a className="button secondary" href={`/cvs/${item.id}`}>Ver preview</a>
            </article>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
