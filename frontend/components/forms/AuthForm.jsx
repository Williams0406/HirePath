"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { authApi, setSession } from "@/lib/api";

export default function AuthForm({ mode = "login" }) {
  const router = useRouter();
  const [form, setForm] = useState({ username: "", email: "", first_name: "", last_name: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const update = (event) => setForm((current) => ({ ...current, [event.target.name]: event.target.value }));

  async function submit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (mode === "register") {
        await authApi.register(form);
      }
      const tokens = await authApi.login(form.username, form.password);
      setSession(tokens);
      router.push("/admin");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="grid" onSubmit={submit}>
      {mode === "register" ? (
        <div className="form-grid">
          <div className="field">
            <label>Nombres</label>
            <input className="input" name="first_name" value={form.first_name} onChange={update} />
          </div>
          <div className="field">
            <label>Apellidos</label>
            <input className="input" name="last_name" value={form.last_name} onChange={update} />
          </div>
          <div className="field">
            <label>Email</label>
            <input className="input" name="email" type="email" value={form.email} onChange={update} />
          </div>
          <div className="field">
            <label>Usuario</label>
            <input className="input" name="username" required value={form.username} onChange={update} />
          </div>
        </div>
      ) : (
        <div className="field">
          <label>Usuario</label>
          <input className="input" name="username" required value={form.username} onChange={update} />
        </div>
      )}
      <div className="field">
        <label>Clave</label>
        <input className="input" name="password" type="password" required value={form.password} onChange={update} />
      </div>
      {error ? <p style={{ color: "var(--red)" }}>{error}</p> : null}
      <button className="button" disabled={loading}>{loading ? "Procesando" : mode === "register" ? "Crear cuenta" : "Entrar"}</button>
    </form>
  );
}
