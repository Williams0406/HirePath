import DashboardSidebar from "./DashboardSidebar";
import DashboardTopbar from "./DashboardTopbar";

export default function AppShell({ children, admin = false }) {
  return (
    <div className="app-shell">
      <DashboardSidebar admin={admin} />
      <main className="main">
        <DashboardTopbar />
        {children}
      </main>
    </div>
  );
}
