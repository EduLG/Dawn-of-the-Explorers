import { useState, useEffect, useCallback } from "react";

const API_BASE =
  import.meta?.env?.VITE_API_BASE || "http://localhost:5000/users";

export default function useUser(userId) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchUser = useCallback(
    async (signal) => {
      if (!userId) return;
      setLoading(true);
      setError(null);

      try {
        const res = await fetch(`${API_BASE}/${encodeURIComponent(userId)}`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
          signal,
        });

        if (!res.ok) {
          const text = await res.text();
          throw new Error(text || `Request failed with status ${res.status}`);
        }

        const payload = await res.json();
        setData(payload);
      } catch (err) {
        if (err.name === "AbortError") return;
        setError(err);
      } finally {
        setLoading(false);
      }
    },
    [userId],
  );

  useEffect(() => {
    if (!userId) return;
    const controller = new AbortController();
    fetchUser(controller.signal);
    return () => controller.abort();
  }, [userId, fetchUser]);

  const refetch = useCallback(() => {
    const controller = new AbortController();
    fetchUser(controller.signal);
  }, [fetchUser]);

  return { data, loading, error, refetch };
}
