import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";

export default function AdminUsersPage() {
  return (
    <AppShell admin>
      <div className="page">
        <PageHeader eyebrow="Admin" title="Usuarios" />
        <div className="card">
          <table className="table">
            <thead><tr><th>Usuario</th><th>Email</th><th>Estado</th></tr></thead>
            <tbody>
              {["ana", "luis", "maria"].map((user) => (
                <tr key={user}><td>{user}</td><td>{user}@hirepath.local</td><td><span className="status">Activo</span></td></tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </AppShell>
  );
}
