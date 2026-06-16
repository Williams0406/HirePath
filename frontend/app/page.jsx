import Link from "next/link";
import Footer from "@/components/layout/Footer";
import PublicNavbar from "@/components/layout/PublicNavbar";

export default function LandingPage() {
  return (
    <>
      <PublicNavbar />
      <main>
        <section className="hero">
          <div>
            <p className="eyebrow">HirePath</p>
            <h1>Postulaciones laborales con estrategia, orden y control.</h1>
            <p className="lead">
              Una plataforma para alinear tu perfil real con vacantes, CVs, respuestas, salarios y entrevistas.
            </p>
            <div className="toolbar" style={{ marginTop: 24 }}>
              <Link className="button" href="/register">Crear cuenta</Link>
              <Link className="button secondary" href="/login">Entrar</Link>
            </div>
          </div>
          <div className="visual-placeholder" aria-label="Espacio reservado para imagen principal" />
        </section>

        <section id="como-funciona" className="section">
          <div className="grid cols-4">
            {["Perfil", "Vacantes", "CV", "Entrevista"].map((item, index) => (
              <article className="card pad" key={item}>
                <span className="status blue">0{index + 1}</span>
                <h3>{item}</h3>
                <p className="muted">Cada paso mantiene trazabilidad y revision humana.</p>
              </article>
            ))}
          </div>
        </section>

        <section id="modulos" className="section">
          <div className="page-header">
            <div>
              <p className="eyebrow">Modulos</p>
              <h2>Centro de empleabilidad asistida</h2>
            </div>
          </div>
          <div className="grid cols-3">
            {["Matching inteligente", "Salario sugerido", "Pipeline laboral", "CV dinamico", "Respuestas asistidas", "Preparacion STAR"].map((item) => (
              <article className="card pad" key={item}>
                <h3>{item}</h3>
                <div className="empty-image" aria-label="Espacio reservado para imagen de modulo" />
              </article>
            ))}
          </div>
        </section>

        <section id="faq" className="section">
          <div className="grid cols-2">
            <article className="card pad">
              <h3>Datos reales</h3>
              <p className="muted">El contenido generado se basa en informacion registrada por el usuario.</p>
            </article>
            <article className="card pad">
              <h3>Revision final</h3>
              <p className="muted">El usuario aprueba CVs, respuestas y postulaciones antes de avanzar.</p>
            </article>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
