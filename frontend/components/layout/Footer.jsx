export default function Footer() {
  return (
    <footer className="section" style={{ background: "var(--navy)", color: "#cbd5e1" }}>
      <div className="grid cols-3">
        <div>
          <div className="brand">
            <span className="brand-mark">H</span>
            <span>HirePath</span>
          </div>
        </div>
        <div className="muted">Veracidad, privacidad y control humano en cada postulacion.</div>
        <div className="toolbar">
          <a href="#">Terminos</a>
          <a href="#">Privacidad</a>
          <a href="#">Contacto</a>
        </div>
      </div>
    </footer>
  );
}
