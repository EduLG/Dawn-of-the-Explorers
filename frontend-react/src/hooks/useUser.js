import { useState, useEffect, useCallback } from "react";

const API_BASE = "http://localhost:5000/users";

export function useUser(userId) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchUser = useCallback(async (id) => {
    if (!id) return null;
    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem("token");
      const res = await fetch(`${API_BASE}/${id}`, {
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
      });

      const contentType = res.headers.get("content-type") || "";
      const data = contentType.includes("application/json")
        ? await res.json()
        : null;

      if (!res.ok) {
        const msg = (data && data.error) || "Failed to fetch user";
        throw new Error(msg);
      }

      setUser(data);
      return data;
    } catch (err) {
      setError(err.message || String(err));
      setUser(null);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (userId) {
      fetchUser(userId).catch(() => {});
    }
  }, [userId, fetchUser]);

  return {
    user,
    loading,
    error,
    refetch: () => fetchUser(userId),
  };
}

export default useUser;
