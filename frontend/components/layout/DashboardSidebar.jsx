"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const items = [["U", "Mi panel", "/admin"]];

export default function DashboardSidebar({ admin = false }) {
  const pathname = usePathname();
  const navItems = items;

  return (
    <aside className="sidebar">
      <Link href="/admin" className="brand">
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
