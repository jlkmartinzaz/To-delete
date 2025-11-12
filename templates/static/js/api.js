const API_URL = "http://localhost:5000";

async function apiRequest(path, method = "GET", body = null, token = null) {
  const headers = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });

  if (res.status === 401 && path !== "/refresh") {
    throw new Error("Token expirado o inválido");
  }

  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || data.msg || "Error");
  return data;
}
