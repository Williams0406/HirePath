const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

export function getToken() {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem("hirepath_access");
}

export function setSession(tokens) {
  if (typeof window === "undefined") return;
  if (tokens?.access) window.localStorage.setItem("hirepath_access", tokens.access);
  if (tokens?.refresh) window.localStorage.setItem("hirepath_refresh", tokens.refresh);
}

export function clearSession() {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem("hirepath_access");
  window.localStorage.removeItem("hirepath_refresh");
}

export async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let details = null;
    try {
      details = await response.json();
    } catch {
      details = { detail: response.statusText };
    }
    throw new Error(details.detail || JSON.stringify(details));
  }

  if (response.status === 204) return null;
  return response.json();
}

export function unwrapList(payload) {
  if (Array.isArray(payload)) return payload;
  return payload?.results || [];
}

export const authApi = {
  login: (username, password) =>
    apiFetch("/auth/login/", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }),
  register: (payload) =>
    apiFetch("/auth/register/", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};

export const userApi = {
  me: () => apiFetch("/me/"),
  profile: () => apiFetch("/profile/"),
  llmSettings: () => apiFetch("/llm-settings/"),
  updateProfile: (payload) =>
    apiFetch("/profile/", {
      method: "PATCH",
      body: JSON.stringify(payload),
    }),
  updateLlmSettings: (payload) =>
    apiFetch("/llm-settings/", {
      method: "PATCH",
      body: JSON.stringify(payload),
    }),
  chatWithGroq: (payload) =>
    apiFetch("/llm/chat/", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  list: (resource) => apiFetch(`/${resource}/`),
  create: (resource, payload) =>
    apiFetch(`/${resource}/`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  update: (resource, id, payload) =>
    apiFetch(`/${resource}/${id}/`, {
      method: "PATCH",
      body: JSON.stringify(payload),
    }),
  remove: (resource, id) =>
    apiFetch(`/${resource}/${id}/`, {
      method: "DELETE",
    }),
};

export { API_URL };
