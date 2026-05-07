import { useState, useEffect } from "react";
import { apiFetch } from "../utils/apiFetch";

const useJobs = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiFetch("/api/v1/jobs")
      .then((r) => r.json())
      .then(setJobs)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return { jobs, loading };
};

export default useJobs;
