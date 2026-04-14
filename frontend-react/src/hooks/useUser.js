import { useState, useEffect, useCallback } from "react";

const API_URL = "/api/v1/users/me";

export default function useUser() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchUser = useCallback(async (signal) => {
    const token = localStorage.getItem("token");
    if (!token) return;

    setLoading(true);
    setError(null);

    try {
      const res = await fetch(API_URL, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
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
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    fetchUser(controller.signal);
    return () => controller.abort();
  }, [fetchUser]);

  const refetch = useCallback(() => {
    const controller = new AbortController();
    fetchUser(controller.signal);
  }, [fetchUser]);

  return { data, loading, error, refetch };
}
