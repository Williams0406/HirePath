import Link from "next/link";

export default function PublicNavbar() {
  return (
    <nav className="public-nav">
      <Link href="/" className="brand">
        <span className="brand-mark">H</span>
        <span>HirePath</span>
      </Link>
      <div className="public-links">
        <a href="/#como-funciona">Proceso</a>
        <a href="/#modulos">Modulos</a>
        <a href="/#faq">FAQ</a>
      </div>
      <div className="toolbar">
        <Link className="button secondary" href="/login">Entrar</Link>
        <Link className="button" href="/register">Crear cuenta</Link>
      </div>
    </nav>
  );
}
