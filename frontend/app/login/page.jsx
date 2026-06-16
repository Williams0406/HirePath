import Link from "next/link";
import AuthForm from "@/components/forms/AuthForm";

export default function LoginPage() {
  return (
    <main className="auth-page">
      <section className="auth-panel">
        <Link href="/" className="brand" style={{ marginBottom: 34 }}>
          <span className="brand-mark">H</span>
          <span>HirePath</span>
        </Link>
        <h1 className="compact-title">Acceso</h1>
        <AuthForm />
        <p className="muted" style={{ marginTop: 18 }}>
          <Link href="/register">Crear cuenta</Link>
        </p>
      </section>
      <section className="auth-visual">
        <div className="visual-placeholder" aria-label="Espacio reservado para imagen de login" />
      </section>
    </main>
  );
}
