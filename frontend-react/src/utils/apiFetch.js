const BASE_URL = import.meta.env.VITE_API_URL ?? "";
const REFRESH_URL = `${BASE_URL}/api/v1/auth/refresh`;

async function refreshAccessToken() {
  const refreshToken = localStorage.getItem("refresh_token");
  if (!refreshToken) return null;

  const res = await fetch(REFRESH_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${refreshToken}`,
    },
  });

  if (!res.ok) return null;

  const data = await res.json();
  localStorage.setItem("token", data.access_token);
  return data.access_token;
}

function clearSessionAndRedirect() {
  localStorage.removeItem("token");
  localStorage.removeItem("refresh_token");
  window.location.href = "/login";
}

export async function apiFetch(url, options = {}) {
  url = `${BASE_URL}${url}`;
  const token = localStorage.getItem("token");

  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  let res = await fetch(url, { ...options, headers });

  if (res.status === 401) {
    const newToken = await refreshAccessToken();

    if (!newToken) {
      clearSessionAndRedirect();
      return res;
    }

    headers.Authorization = `Bearer ${newToken}`;
    res = await fetch(url, { ...options, headers });

    if (res.status === 401) {
      clearSessionAndRedirect();
    }
  }

  return res;
}
