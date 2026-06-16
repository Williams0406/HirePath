import "./globals.css";

export const metadata = {
  title: "HirePath",
  description: "Plataforma inteligente de empleabilidad asistida",
};

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
