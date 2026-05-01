import { useState, useEffect, useCallback } from "react";
import { apiFetch } from "../utils/apiFetch";

export default function useDungeons() {
  const [dungeons, setDungeons] = useState([]);
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState(null);

  const fetchDungeons = useCallback(async (signal) => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch("/api/v1/dungeons", { method: "GET", signal });
      if (!res.ok) throw new Error("Failed to fetch dungeons");
      const data = await res.json();
      setDungeons(data);
    } catch (err) {
      if (err.name === "AbortError") return;
      setError(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    fetchDungeons(controller.signal);
    return () => controller.abort();
  }, [fetchDungeons]);

  return { dungeons, loading, error };
}
