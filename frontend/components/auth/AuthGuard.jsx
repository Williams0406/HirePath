"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { clearSession, getToken, userApi } from "@/lib/api";

export default function AuthGuard({ children }) {
  const router = useRouter();
  const [ready, setReady] = useState(false);

  useEffect(() => {
    let mounted = true;

    async function verifySession() {
      if (!getToken()) {
        router.replace("/login");
        return;
      }

      try {
        await userApi.me();
        if (mounted) setReady(true);
      } catch {
        clearSession();
        router.replace("/login");
      }
    }

    verifySession();
    return () => {
      mounted = false;
    };
  }, [router]);

  if (!ready) {
    return (
      <main className="page">
        <p className="muted">Validando sesion...</p>
      </main>
    );
  }

  return children;
}
