import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";

export default function SettingsPage() {
  return (
    <AppShell>
      <div className="page">
        <PageHeader eyebrow="Cuenta" title="Configuracion" actions={<button className="button">Guardar</button>} />
        <div className="grid cols-2">
          <section className="card pad">
            <h2 className="compact-title">Preferencias</h2>
            <label className="toolbar"><input type="checkbox" defaultChecked /> Vacantes remotas</label>
            <label className="toolbar"><input type="checkbox" defaultChecked /> Alertas de entrevista</label>
            <label className="toolbar"><input type="checkbox" /> Reporte semanal</label>
          </section>
          <section className="card pad">
            <h2 className="compact-title">API</h2>
            <input className="input" defaultValue="http://127.0.0.1:8010/api" />
          </section>
        </div>
      </div>
    </AppShell>
  );
}
