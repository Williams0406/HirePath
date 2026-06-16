import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";
import CVPreview from "@/components/cvs/CVPreview";
import CVSectionSelector from "@/components/cvs/CVSectionSelector";

export default function CVDetailPage() {
  return (
    <AppShell>
      <div className="page">
        <PageHeader eyebrow="Preview" title="CV dinamico" actions={<><button className="button secondary">Guardar</button><button className="button">Descargar PDF</button></>} />
        <div className="split">
          <div className="grid">
            <CVSectionSelector />
            <div className="card pad">
              <h2 className="compact-title">Contenido usado</h2>
              <p className="muted">Resumen, experiencias, proyectos y skills seleccionados desde el perfil.</p>
            </div>
          </div>
          <CVPreview title="CV Analista BI" />
        </div>
      </div>
    </AppShell>
  );
}
