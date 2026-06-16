"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const items = [
  ["D", "Dashboard", "/dashboard"],
  ["P", "Perfil", "/profile"],
  ["V", "Vacantes", "/jobs"],
  ["C", "CVs", "/cvs"],
  ["A", "Postulaciones", "/applications"],
  ["E", "Entrevistas", "/interviews"],
  ["S", "Configuracion", "/settings"],
];

export default function DashboardSidebar({ admin = false }) {
  const pathname = usePathname();
  const navItems = admin
    ? [
        ["M", "Metricas", "/admin"],
        ["U", "Usuarios", "/admin/users"],
        ["F", "Fuentes", "/admin/sources"],
        ["R", "Scraping", "/admin/scraping"],
        ["V", "Vacantes", "/admin/jobs"],
        ["I", "Logs IA", "/admin/ai-logs"],
      ]
    : items;

  return (
    <aside className="sidebar">
      <Link href={admin ? "/admin" : "/dashboard"} className="brand">
        <span className="brand-mark">H</span>
        <span>HirePath</span>
      </Link>
      <div className="nav-list">
        {navItems.map(([icon, label, href]) => (
          <Link key={href} href={href} className={`nav-item ${pathname === href ? "active" : ""}`}>
            <span className="nav-ico">{icon}</span>
            <span>{label}</span>
          </Link>
        ))}
      </div>
    </aside>
  );
}
