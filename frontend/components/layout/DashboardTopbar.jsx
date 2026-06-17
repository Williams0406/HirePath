"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { clearSession } from "@/lib/api";

export default function DashboardTopbar() {
  const router = useRouter();

  function logout() {
    clearSession();
    router.replace("/");
  }

  return (
    <header className="topbar">
      <span className="muted">Panel administrativo</span>
      <div className="toolbar">
        <Link className="button secondary" href="/">Inicio</Link>
        <button className="button secondary" type="button" onClick={logout}>Cerrar sesion</button>
      </div>
    </header>
  );
}
