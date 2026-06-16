export const metrics = [
  { label: "Vacantes recomendadas", value: "18", hint: "6 nuevas esta semana" },
  { label: "CVs generados", value: "7", hint: "3 pendientes de revision" },
  { label: "Postulaciones activas", value: "12", hint: "4 con seguimiento" },
  { label: "Entrevistas", value: "3", hint: "2 por preparar" },
];

export const jobs = [
  {
    id: 1,
    title: "Analista de Datos BI",
    company: "Andes Analytics",
    location: "Lima, Peru",
    modality: "HYBRID",
    seniority: "Semi Senior",
    salary: "S/ 3,500 - S/ 4,800",
    score: 86,
    source: "LinkedIn",
  },
  {
    id: 2,
    title: "Frontend Developer Next.js",
    company: "Nova Talent",
    location: "Remoto",
    modality: "REMOTE",
    seniority: "Junior avanzado",
    salary: "S/ 4,000 - S/ 5,500",
    score: 79,
    source: "Company Site",
  },
  {
    id: 3,
    title: "Especialista CRM Laboral",
    company: "PeopleOps Lab",
    location: "Lima, Peru",
    modality: "ONSITE",
    seniority: "Senior",
    salary: "No publicado",
    score: 68,
    source: "Computrabajo",
  },
];

export const applications = [
  { id: 1, title: "Analista de Datos BI", company: "Andes Analytics", status: "MATCHED", date: "2026-06-10" },
  { id: 2, title: "Frontend Developer Next.js", company: "Nova Talent", status: "CV_GENERATED", date: "2026-06-12" },
  { id: 3, title: "Product Analyst", company: "Metric Studio", status: "INTERVIEW", date: "2026-06-15" },
  { id: 4, title: "Data Assistant", company: "Retail Pro", status: "APPLIED", date: "2026-06-08" },
];

export const interviews = [
  {
    id: 1,
    title: "Product Analyst",
    company: "Metric Studio",
    advice: "Conecta tus proyectos con indicadores de negocio y decisiones tomadas con datos.",
    questions: [
      "Cuentame sobre un proyecto donde usaste datos para mejorar un proceso.",
      "Como priorizas hallazgos cuando hay muchas metricas disponibles?",
      "Cual seria tu expectativa salarial para esta posicion?",
    ],
  },
  {
    id: 2,
    title: "Analista de Datos BI",
    company: "Andes Analytics",
    advice: "Prepara ejemplos de dashboards, calidad de datos y comunicacion con usuarios internos.",
    questions: [
      "Como validarias la confiabilidad de una fuente de datos?",
      "Que indicadores mostrarias para un equipo comercial?",
    ],
  },
];

export const cvItems = [
  { id: 1, title: "CV Analista BI", job: "Analista de Datos BI", updated: "2026-06-15", status: "Listo" },
  { id: 2, title: "CV Frontend Next.js", job: "Frontend Developer Next.js", updated: "2026-06-14", status: "Revision" },
];

export const adminMetrics = [
  { label: "Usuarios", value: "124" },
  { label: "Vacantes importadas", value: "1,842" },
  { label: "Fuentes activas", value: "8" },
  { label: "Solicitudes IA", value: "5,230" },
];
