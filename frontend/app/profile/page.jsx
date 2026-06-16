import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";

export default function ProfilePage() {
  return (
    <AppShell>
      <div className="page">
        <PageHeader eyebrow="Perfil" title="Perfil profesional" actions={<button className="button">Guardar</button>} />
        <div className="grid cols-2">
          <section className="card pad">
            <h2 className="compact-title">Datos base</h2>
            <div className="form-grid">
              <div className="field"><label>Titular</label><input className="input" /></div>
              <div className="field"><label>Años de experiencia</label><input className="input" type="number" /></div>
              <div className="field"><label>Pais</label><input className="input" /></div>
              <div className="field"><label>Ciudad</label><input className="input" /></div>
              <div className="field" style={{ gridColumn: "1 / -1" }}><label>Resumen</label><textarea className="textarea" /></div>
            </div>
          </section>
          <section className="card pad">
            <h2 className="compact-title">Skills y enlaces</h2>
            <div className="grid">
              <input className="input" placeholder="LinkedIn" />
              <input className="input" placeholder="GitHub" />
              <input className="input" placeholder="Portafolio" />
              <div className="toolbar">
                {["Python", "Django", "Next.js", "SQL", "Comunicacion"].map((item) => <span className="status blue" key={item}>{item}</span>)}
              </div>
            </div>
          </section>
        </div>
      </div>
    </AppShell>
  );
}
