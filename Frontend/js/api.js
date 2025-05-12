const API_BASE = "https://localhost:8000"; // apunta a tu gateway

const endpoints = {
  login: `${API_BASE}/auth/login`,
  me: `${API_BASE}/auth/me`,
  libros: `${API_BASE}/libros`,
  logout: `${API_BASE}/auth/logout`,
};

async function apiFetch(url, options = {}) {
  const token = localStorage.getItem("token");
  if (token) {
    options.headers = {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`,
    };
  }
  const res = await fetch(url, options);
  if (res.status === 401) {
    window.location.href = "login.html";
  }
  return res.json();
}
