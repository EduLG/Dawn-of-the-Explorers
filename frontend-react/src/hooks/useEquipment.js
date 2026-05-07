import { useState, useEffect } from "react";
import { apiFetch } from "../utils/apiFetch";

export function useEquipment(jobId) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!jobId) return;

    const controller = new AbortController();

    const fetchEquipment = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await apiFetch(`/api/v1/equipment?job_id=${jobId}`, {
          method: "GET",
          signal: controller.signal,
        });
        if (!res.ok) throw new Error("Failed to fetch equipment");
        const payload = await res.json();
        setData(payload);
      } catch (err) {
        if (err.name === "AbortError") return;
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchEquipment();
    return () => controller.abort();
  }, [jobId]);

  return { data, loading, error };
}
