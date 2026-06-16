import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";

export default function OnboardingPage() {
  return (
    <AppShell>
      <div className="page">
        <PageHeader eyebrow="Inicio" title="Configura tu perfil" description="Completa los datos que alimentan el matching y los CVs." />
        <div className="card pad">
          <div className="form-grid">
            <div className="field">
              <label>Titular profesional</label>
              <input className="input" placeholder="Analista de datos" />
            </div>
            <div className="field">
              <label>Ubicacion</label>
              <input className="input" placeholder="Lima, Peru" />
            </div>
            <div className="field" style={{ gridColumn: "1 / -1" }}>
              <label>Resumen</label>
              <textarea className="textarea" />
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
