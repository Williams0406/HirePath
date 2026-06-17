"use client";

import { useEffect, useMemo, useState } from "react";
import AppShell from "@/components/layout/AppShell";
import PageHeader from "@/components/layout/PageHeader";
import { unwrapList, userApi } from "@/lib/api";

const emptyProfile = {
  headline: "",
  professional_summary: "",
  current_salary: "",
  desired_salary_min: "",
  desired_salary_max: "",
  availability: "",
  country: "",
  city: "",
  linkedin_url: "",
  github_url: "",
  portfolio_url: "",
};

const emptyLlm = {
  groq_model: "llama-3.1-8b-instant",
  is_enabled: false,
  has_groq_api_key: false,
};

const groqModels = [
  "llama-3.1-8b-instant",
  "llama-3.3-70b-versatile",
  "mixtral-8x7b-32768",
  "gemma2-9b-it",
];

const profileFields = [
  ["headline", "Titular profesional", "text"],
  ["availability", "Disponibilidad", "text"],
  ["country", "Pais", "text"],
  ["city", "Ciudad", "text"],
  ["current_salary", "Salario actual", "number"],
  ["desired_salary_min", "Salario deseado min.", "number"],
  ["desired_salary_max", "Salario deseado max.", "number"],
  ["linkedin_url", "LinkedIn", "url"],
  ["github_url", "GitHub", "url"],
  ["portfolio_url", "Portafolio", "url"],
  ["professional_summary", "Resumen profesional", "textarea"],
];

const sections = [
  {
    key: "educations",
    label: "Educacion",
    singular: "educacion",
    empty: "Agrega estudios, grados y formacion relevante.",
    primary: (item) => item.degree || "Titulo sin nombre",
    secondary: (item) => [item.institution, item.field_of_study].filter(Boolean).join(" - "),
    meta: (item) => dateRange(item.start_date, item.end_date),
    body: (item) => item.description,
    fields: [
      ["degree", "Titulo", "text", true],
      ["institution", "Institucion", "text", true],
      ["field_of_study", "Area"],
      ["start_date", "Inicio", "date"],
      ["end_date", "Fin", "date"],
      ["description", "Descripcion", "textarea"],
    ],
    initial: { degree: "", institution: "", field_of_study: "", start_date: "", end_date: "", description: "" },
  },
  {
    key: "work-experiences",
    label: "Experiencia profesional",
    singular: "experiencia",
    empty: "Registra roles, responsabilidades y logros medibles.",
    primary: (item) => item.position || "Cargo sin nombre",
    secondary: (item) => item.company || "",
    meta: (item) => dateRange(item.start_date, item.is_current ? "Actual" : item.end_date),
    body: (item) => [item.description, item.achievements, item.tools_used ? `Herramientas: ${item.tools_used}` : ""].filter(Boolean).join("\n"),
    fields: [
      ["position", "Cargo", "text", true],
      ["company", "Empresa", "text", true],
      ["start_date", "Inicio", "date"],
      ["end_date", "Fin", "date"],
      ["is_current", "Trabajo actual", "checkbox"],
      ["description", "Responsabilidades", "textarea"],
      ["achievements", "Logros", "textarea"],
      ["tools_used", "Herramientas usadas", "textarea"],
    ],
    initial: { position: "", company: "", start_date: "", end_date: "", is_current: false, description: "", achievements: "", tools_used: "" },
  },
  {
    key: "projects",
    label: "Proyectos",
    singular: "proyecto",
    empty: "Incluye proyectos que prueben criterio, alcance e impacto.",
    primary: (item) => item.name || "Proyecto sin nombre",
    secondary: (item) => item.technologies || item.url || "",
    meta: () => "",
    body: (item) => [item.description, item.impact].filter(Boolean).join("\n"),
    fields: [
      ["name", "Nombre", "text", true],
      ["url", "URL", "url"],
      ["description", "Descripcion", "textarea", true],
      ["technologies", "Tecnologias", "textarea"],
      ["impact", "Impacto", "textarea"],
    ],
    initial: { name: "", url: "", description: "", technologies: "", impact: "" },
  },
  {
    key: "certifications",
    label: "Certificaciones",
    singular: "certificacion",
    empty: "Agrega certificados y credenciales verificables.",
    primary: (item) => item.name || "Certificacion sin nombre",
    secondary: (item) => item.institution || item.credential_url || "",
    meta: (item) => item.issue_date || "",
    body: (item) => item.description,
    fields: [
      ["name", "Nombre", "text", true],
      ["institution", "Institucion"],
      ["issue_date", "Fecha", "date"],
      ["credential_url", "URL credencial", "url"],
      ["description", "Descripcion", "textarea"],
    ],
    initial: { name: "", institution: "", issue_date: "", credential_url: "", description: "" },
  },
  {
    key: "skills",
    label: "Catalogo de skills",
    singular: "skill",
    empty: "Crea skills reutilizables para asignarlas al usuario.",
    primary: (item) => item.name || "Skill sin nombre",
    secondary: (item) => categoryLabel(item.category),
    meta: () => "",
    body: () => "",
    fields: [
      ["name", "Nombre", "text", true],
      ["category", "Categoria", "select", true, [
        ["TECHNICAL", "Tecnica"],
        ["SOFT", "Blanda"],
        ["LANGUAGE", "Idioma"],
        ["TOOL", "Herramienta"],
        ["OTHER", "Otra"],
      ]],
    ],
    initial: { name: "", category: "TECHNICAL" },
  },
];

const levelOptions = [
  ["BASIC", "Basico"],
  ["INTERMEDIATE", "Intermedio"],
  ["ADVANCED", "Avanzado"],
  ["EXPERT", "Experto"],
];

function categoryLabel(value) {
  return {
    TECHNICAL: "Tecnica",
    SOFT: "Blanda",
    LANGUAGE: "Idioma",
    TOOL: "Herramienta",
    OTHER: "Otra",
  }[value] || "Otra";
}

function dateRange(start, end) {
  if (!start && !end) return "";
  return [start, end].filter(Boolean).join(" - ");
}

function cleanPayload(payload) {
  return Object.fromEntries(
    Object.entries(payload).map(([key, value]) => {
      if (key.endsWith("_date") && value === "") return [key, null];
      if (["current_salary", "desired_salary_min", "desired_salary_max"].includes(key) && value === "") return [key, null];
      return [key, value];
    }),
  );
}

function toFormValue(value) {
  if (value === null || value === undefined) return "";
  return value;
}

function jumpToSection(id) {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
}

function IconButton({ label, children, variant = "secondary", ...props }) {
  return (
    <button className={`button icon ${variant}`} type="button" title={label} aria-label={label} {...props}>
      {children}
    </button>
  );
}

function FieldControl({ field, value, onChange }) {
  const [name, label, type = "text", required = false, options = []] = field;
  const inputId = `field-${name}`;

  if (type === "textarea") {
    return (
      <div className="field span-2">
        <label htmlFor={inputId}>{label}</label>
        <textarea id={inputId} className="textarea" required={required} value={toFormValue(value)} onChange={(event) => onChange(name, event.target.value)} />
      </div>
    );
  }

  if (type === "select") {
    return (
      <div className="field">
        <label htmlFor={inputId}>{label}</label>
        <select id={inputId} className="select" required={required} value={toFormValue(value)} onChange={(event) => onChange(name, event.target.value)}>
          {options.map(([optionValue, optionLabel]) => <option key={optionValue} value={optionValue}>{optionLabel}</option>)}
        </select>
      </div>
    );
  }

  if (type === "checkbox") {
    return (
      <label className="check-field">
        <input type="checkbox" checked={Boolean(value)} onChange={(event) => onChange(name, event.target.checked)} />
        <span>{label}</span>
      </label>
    );
  }

  return (
    <div className="field">
      <label htmlFor={inputId}>{label}</label>
      <input id={inputId} className="input" required={required} type={type} step={type === "number" ? "0.01" : undefined} value={toFormValue(value)} onChange={(event) => onChange(name, event.target.value)} />
    </div>
  );
}

function InlineForm({ children, onSubmit, submitLabel, busy, onCancel }) {
  return (
    <form className="cv-form-panel" onSubmit={onSubmit}>
      <div className="cv-form-grid">{children}</div>
      <div className="form-actions span-2">
        <button className="button" type="submit" disabled={busy}>{submitLabel}</button>
        <button className="button secondary" type="button" onClick={onCancel}>Cancelar</button>
      </div>
    </form>
  );
}

function ResourceSection({ config, items, onSave, onDelete, busy }) {
  const [form, setForm] = useState(config.initial);
  const [editingId, setEditingId] = useState(null);
  const [formOpen, setFormOpen] = useState(false);

  function update(name, value) {
    setForm((current) => ({ ...current, [name]: value }));
  }

  function startAdd() {
    setEditingId(null);
    setForm(config.initial);
    setFormOpen(true);
  }

  function startEdit(item) {
    setEditingId(item.id);
    setForm({ ...config.initial, ...item });
    setFormOpen(true);
  }

  function closeForm() {
    setEditingId(null);
    setForm(config.initial);
    setFormOpen(false);
  }

  async function submit(event) {
    event.preventDefault();
    await onSave(config.key, editingId, cleanPayload(form));
    closeForm();
  }

  return (
    <section className="cv-section" id={`section-${config.key}`}>
      <div className="cv-section-title">
        <h2>{config.label}</h2>
        <IconButton label={`Agregar ${config.singular}`} onClick={startAdd}>+</IconButton>
      </div>

      {formOpen ? (
        <InlineForm onSubmit={submit} submitLabel={editingId ? "Guardar cambios" : "Agregar registro"} busy={busy} onCancel={closeForm}>
          {config.fields.map((field) => <FieldControl key={field[0]} field={field} value={form[field[0]]} onChange={update} />)}
        </InlineForm>
      ) : null}

      <div className="cv-entry-list">
        {items.length ? items.map((item) => (
          <article className="cv-entry" key={item.id}>
            <div className="cv-entry-main">
              <div className="cv-entry-heading">
                <div>
                  <h3>{config.primary(item)}</h3>
                  {config.secondary(item) ? <p>{config.secondary(item)}</p> : null}
                </div>
                {config.meta(item) ? <span>{config.meta(item)}</span> : null}
              </div>
              {config.body(item) ? (
                <ul>
                  {config.body(item).split("\n").filter(Boolean).map((line) => <li key={line}>{line}</li>)}
                </ul>
              ) : null}
            </div>
            <div className="cv-actions">
              <IconButton label={`Editar ${config.singular}`} onClick={() => startEdit(item)}>✎</IconButton>
              <IconButton label={`Eliminar ${config.singular}`} variant="danger" onClick={() => onDelete(config.key, item.id)}>X</IconButton>
            </div>
          </article>
        )) : <div className="cv-empty"><p>{config.empty}</p></div>}
      </div>
    </section>
  );
}

function UserSkillSection({ userSkills, skills, onSave, onDelete, busy }) {
  const initial = { skill: "", level: "INTERMEDIATE", years_experience: "0" };
  const [form, setForm] = useState(initial);
  const [editingId, setEditingId] = useState(null);
  const [formOpen, setFormOpen] = useState(false);

  function update(name, value) {
    setForm((current) => ({ ...current, [name]: value }));
  }

  function startAdd() {
    setEditingId(null);
    setForm(initial);
    setFormOpen(true);
  }

  function startEdit(item) {
    setEditingId(item.id);
    setForm({
      skill: item.skill || "",
      level: item.level || "INTERMEDIATE",
      years_experience: item.years_experience || "0",
    });
    setFormOpen(true);
  }

  function closeForm() {
    setEditingId(null);
    setForm(initial);
    setFormOpen(false);
  }

  async function submit(event) {
    event.preventDefault();
    await onSave("user-skills", editingId, cleanPayload(form));
    closeForm();
  }

  return (
    <section className="cv-section" id="section-user-skills">
      <div className="cv-section-title">
        <h2>Habilidades del usuario</h2>
        <IconButton label="Agregar habilidad del usuario" onClick={startAdd}>+</IconButton>
      </div>

      {formOpen ? (
        <InlineForm onSubmit={submit} submitLabel={editingId ? "Guardar cambios" : "Agregar habilidad"} busy={busy || !skills.length} onCancel={closeForm}>
          <div className="field">
            <label>Skill</label>
            <select className="select" required value={form.skill} onChange={(event) => update("skill", event.target.value)}>
              <option value="">Seleccionar skill</option>
              {skills.map((skill) => <option key={skill.id} value={skill.id}>{skill.name}</option>)}
            </select>
          </div>
          <div className="field">
            <label>Nivel</label>
            <select className="select" value={form.level} onChange={(event) => update("level", event.target.value)}>
              {levelOptions.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
            </select>
          </div>
          <div className="field">
            <label>Anios de experiencia</label>
            <input className="input" type="number" step="0.5" value={form.years_experience} onChange={(event) => update("years_experience", event.target.value)} />
          </div>
        </InlineForm>
      ) : null}

      <div className="cv-skill-grid">
        {userSkills.length ? userSkills.map((item) => (
          <article className="cv-skill" key={item.id}>
            <div>
              <strong>{item.skill_detail?.name || "Skill"}</strong>
              <span>{levelOptions.find(([value]) => value === item.level)?.[1] || item.level} · {item.years_experience} anios</span>
            </div>
            <div className="cv-actions">
              <IconButton label="Editar habilidad" onClick={() => startEdit(item)}>✎</IconButton>
              <IconButton label="Eliminar habilidad" variant="danger" onClick={() => onDelete("user-skills", item.id)}>X</IconButton>
            </div>
          </article>
        )) : <div className="cv-empty"><p>Asigna habilidades al usuario para destacarlas en el CV.</p></div>}
      </div>
    </section>
  );
}

function ProfileSection({ profile, onChange, onSave, onClear, busy }) {
  const [formOpen, setFormOpen] = useState(false);
  const location = [profile.city, profile.country].filter(Boolean).join(", ");
  const links = [
    ["LinkedIn", profile.linkedin_url],
    ["GitHub", profile.github_url],
    ["Portafolio", profile.portfolio_url],
  ].filter(([, value]) => value);

  return (
    <section className="cv-section" id="section-profile">
      <div className="cv-section-title">
        <h2>Perfil profesional</h2>
        <div className="toolbar">
          <IconButton label="Agregar informacion de perfil" onClick={() => setFormOpen(true)}>+</IconButton>
          <IconButton label="Editar perfil" onClick={() => setFormOpen(true)}>✎</IconButton>
          <IconButton label="Limpiar perfil" variant="danger" onClick={onClear}>X</IconButton>
        </div>
      </div>

      <div className="cv-profile-summary">
        <p>{profile.professional_summary || "Agrega un resumen profesional claro y especifico para que el CV tenga una introduccion fuerte."}</p>
        <div>
          {profile.headline ? <span>{profile.headline}</span> : null}
          {location ? <span>{location}</span> : null}
          {profile.availability ? <span>{profile.availability}</span> : null}
          {links.map(([label, value]) => <span key={label}>{label}: {value}</span>)}
        </div>
      </div>

      {formOpen ? (
        <InlineForm onSubmit={(event) => onSave(event, () => setFormOpen(false))} submitLabel="Guardar perfil" busy={busy} onCancel={() => setFormOpen(false)}>
          {profileFields.map((field) => <FieldControl key={field[0]} field={field} value={profile[field[0]]} onChange={onChange} />)}
        </InlineForm>
      ) : null}
    </section>
  );
}

function LlmSection({ llm, onSave, onClear, busy }) {
  const [formOpen, setFormOpen] = useState(false);
  const [draft, setDraft] = useState({ groq_api_key: "", groq_model: emptyLlm.groq_model, is_enabled: false });

  useEffect(() => {
    setDraft({ groq_api_key: "", groq_model: llm.groq_model || emptyLlm.groq_model, is_enabled: Boolean(llm.is_enabled) });
  }, [llm]);

  function update(name, value) {
    setDraft((current) => ({ ...current, [name]: value }));
  }

  async function submit(event) {
    event.preventDefault();
    const payload = {
      groq_model: draft.groq_model,
      is_enabled: draft.is_enabled,
      ...(draft.groq_api_key ? { groq_api_key: draft.groq_api_key } : {}),
    };
    await onSave(payload);
    setDraft((current) => ({ ...current, groq_api_key: "" }));
    setFormOpen(false);
  }

  return (
    <section className="cv-section" id="section-llm">
      <div className="cv-section-title">
        <h2>Groq LLM</h2>
        <div className="toolbar">
          <IconButton label="Agregar API key de Groq" onClick={() => setFormOpen(true)}>+</IconButton>
          <IconButton label="Editar configuracion Groq" onClick={() => setFormOpen(true)}>✎</IconButton>
          <IconButton label="Eliminar API key de Groq" variant="danger" onClick={onClear}>X</IconButton>
        </div>
      </div>

      <div className="llm-status">
        <span className={llm.has_groq_api_key ? "status" : "status amber"}>{llm.has_groq_api_key ? "API key configurada" : "API key pendiente"}</span>
        <p className="muted">Modelo: {llm.groq_model || emptyLlm.groq_model}</p>
      </div>

      {formOpen ? (
        <form className="cv-form-panel" onSubmit={submit}>
          <div className="cv-form-grid">
            <div className="field span-2">
              <label>Groq API key</label>
              <input className="input" type="password" value={draft.groq_api_key} placeholder={llm.has_groq_api_key ? "Deja en blanco para conservar la key actual" : "gsk_..."} onChange={(event) => update("groq_api_key", event.target.value)} />
            </div>
            <div className="field">
              <label>Modelo</label>
              <select className="select" value={draft.groq_model} onChange={(event) => update("groq_model", event.target.value)}>
                {groqModels.map((model) => <option key={model} value={model}>{model}</option>)}
              </select>
            </div>
            <label className="check-field">
              <input type="checkbox" checked={draft.is_enabled} onChange={(event) => update("is_enabled", event.target.checked)} />
              <span>Habilitar LLM para este usuario</span>
            </label>
          </div>
          <div className="form-actions span-2">
            <button className="button" type="submit" disabled={busy}>Guardar Groq</button>
            <button className="button secondary" type="button" onClick={() => setFormOpen(false)}>Cancelar</button>
          </div>
        </form>
      ) : null}
    </section>
  );
}

export default function AdminPage() {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(emptyProfile);
  const [llm, setLlm] = useState(emptyLlm);
  const [collections, setCollections] = useState({});
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  const resources = useMemo(() => [...sections.map((section) => section.key), "user-skills"], []);

  useEffect(() => {
    async function loadUserPanel() {
      try {
        const [me, candidateProfile, llmSettings, ...resourcePayloads] = await Promise.all([
          userApi.me(),
          userApi.profile(),
          userApi.llmSettings(),
          ...resources.map((resource) => userApi.list(resource)),
        ]);
        setUser(me);
        setProfile({ ...emptyProfile, ...candidateProfile });
        setLlm({ ...emptyLlm, ...llmSettings });
        setCollections(Object.fromEntries(resources.map((resource, index) => [resource, unwrapList(resourcePayloads[index])])));
      } catch (err) {
        setError(err.message);
      }
    }

    loadUserPanel();
  }, [resources]);

  const fullName = [user?.first_name, user?.last_name].filter(Boolean).join(" ") || user?.username || "Usuario";
  const location = [profile.city, profile.country].filter(Boolean).join(", ");
  const navItems = [
    ["section-profile", "Perfil"],
    ...sections.map((section) => [`section-${section.key}`, section.label]),
    ["section-user-skills", "Habilidades"],
    ["section-llm", "Groq LLM"],
  ];

  function updateProfile(name, value) {
    setProfile((current) => ({ ...current, [name]: value }));
  }

  async function saveProfile(event, afterSave) {
    event.preventDefault();
    await runAction(async () => {
      const saved = await userApi.updateProfile(cleanPayload(profile));
      setProfile({ ...emptyProfile, ...saved });
      setMessage("Perfil actualizado.");
      afterSave?.();
    });
  }

  async function clearProfile() {
    await runAction(async () => {
      const saved = await userApi.updateProfile(cleanPayload(emptyProfile));
      setProfile({ ...emptyProfile, ...saved });
      setMessage("Datos de CandidateProfile eliminados.");
    });
  }

  async function saveLlmSettings(payload) {
    await runAction(async () => {
      const saved = await userApi.updateLlmSettings(payload);
      setLlm({ ...emptyLlm, ...saved });
      setMessage("Configuracion de Groq actualizada.");
    });
  }

  async function clearLlmSettings() {
    await saveLlmSettings({ groq_api_key: "", is_enabled: false });
  }

  async function saveResource(resource, id, payload) {
    await runAction(async () => {
      const saved = id ? await userApi.update(resource, id, payload) : await userApi.create(resource, payload);
      setCollections((current) => ({
        ...current,
        [resource]: id
          ? (current[resource] || []).map((item) => item.id === id ? saved : item)
          : [...(current[resource] || []), saved],
      }));
      setMessage(id ? "Registro actualizado." : "Registro creado.");
    });
  }

  async function deleteResource(resource, id) {
    await runAction(async () => {
      await userApi.remove(resource, id);
      setCollections((current) => ({
        ...current,
        [resource]: (current[resource] || []).filter((item) => item.id !== id),
      }));
      setMessage("Registro eliminado.");
    });
  }

  async function runAction(action) {
    setBusy(true);
    setError("");
    setMessage("");
    try {
      await action();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <AppShell admin>
      <div className="page admin-page">
        <PageHeader
          eyebrow="Panel privado"
          title="CV administrativo"
          description="Gestiona la informacion del usuario y su LLM personal desde una vista tipo CV."
        />

        {error ? <p className="alert error">{error}</p> : null}
        {message ? <p className="alert success">{message}</p> : null}

        <div className="cv-workspace">
          <nav className="cv-side-nav" aria-label="Ir a seccion del CV">
            <p className="eyebrow">Secciones</p>
            {navItems.map(([id, label]) => (
              <button key={id} type="button" onClick={() => jumpToSection(id)}>{label}</button>
            ))}
          </nav>

          <article className="harvard-cv">
            <header className="cv-header">
              <h1>{fullName}</h1>
              <p>{profile.headline || "Titular profesional pendiente"}</p>
              <div>
                {user?.email ? <span>{user.email}</span> : null}
                {location ? <span>{location}</span> : null}
                {profile.linkedin_url ? <span>{profile.linkedin_url}</span> : null}
              </div>
            </header>

            <ProfileSection profile={profile} onChange={updateProfile} onSave={saveProfile} onClear={clearProfile} busy={busy} />

            {sections.map((section) => (
              <ResourceSection
                key={section.key}
                config={section}
                items={collections[section.key] || []}
                onSave={saveResource}
                onDelete={deleteResource}
                busy={busy}
              />
            ))}

            <UserSkillSection
              userSkills={collections["user-skills"] || []}
              skills={collections.skills || []}
              onSave={saveResource}
              onDelete={deleteResource}
              busy={busy}
            />

            <LlmSection llm={llm} onSave={saveLlmSettings} onClear={clearLlmSettings} busy={busy} />
          </article>
        </div>
      </div>
    </AppShell>
  );
}
