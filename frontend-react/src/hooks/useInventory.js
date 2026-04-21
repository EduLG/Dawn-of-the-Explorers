import { useState, useEffect, useCallback } from "react";
import { apiFetch } from "../utils/apiFetch";

export function useInventory() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchInventory = useCallback(async (signal) => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch("/api/v1/inventory", { signal });
      if (!res.ok) throw new Error("Failed to fetch inventory");
      const json = await res.json();
      setData(json);
    } catch (err) {
      if (err.name === "AbortError") return;
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    fetchInventory(controller.signal);
    return () => controller.abort();
  }, [fetchInventory]);

  const refetch = useCallback(() => fetchInventory(), [fetchInventory]);

  return { data, loading, error, refetch };
}
