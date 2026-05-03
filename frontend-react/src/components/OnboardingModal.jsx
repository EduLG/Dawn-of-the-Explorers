import { useState } from "react";
import { apiFetch } from "../utils/apiFetch";
import useJobs from "../hooks/useJobs";

const EMPTY_CHAR = { name: "", job_id: "" };

const OnboardingModal = ({ username, onComplete }) => {
  const { jobs, loading: jobsLoading } = useJobs();

  const [partyName, setPartyName] = useState("");
  const [characters, setCharacters] = useState([
    { ...EMPTY_CHAR },
    { ...EMPTY_CHAR },
    { ...EMPTY_CHAR },
    { ...EMPTY_CHAR },
  ]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const updateChar = (index, field, value) => {
    setCharacters((prev) =>
      prev.map((c, i) => (i === index ? { ...c, [field]: value } : c))
    );
  };

  const isValid =
    partyName.trim().length > 0 &&
    characters.every((c) => c.name.trim().length > 0 && c.job_id !== "");

  const handleSubmit = async () => {
    if (!isValid) return;
    setSubmitting(true);
    setError(null);
    try {
      const res = await apiFetch("/api/v1/party/setup", {
        method: "POST",
        body: JSON.stringify({
          party_name: partyName.trim(),
          characters: characters.map((c) => ({
            name: c.name.trim(),
            job_id: parseInt(c.job_id),
          })),
        }),
      });
      if (!res.ok) {
        const body = await res.json();
        throw new Error(body.error || "Setup failed");
      }
      onComplete();
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-sm px-4 py-8 overflow-y-auto">
      <div className="w-full max-w-2xl bg-[#0d0703] border border-white/10 rounded-3xl shadow-2xl p-6 sm:p-8 space-y-7 my-auto">

        {/* Header */}
        <div className="text-center space-y-1">
          <p className="text-[10px] uppercase tracking-widest text-[#a89070]">
            Welcome, {username}
          </p>
          <h2 className="text-2xl font-bold text-[#f3e5c8]">Set up your party</h2>
          <p className="text-xs text-[#6b5a45]">
            Name your party and choose a class for each of your four heroes.
          </p>
        </div>

        {/* Party name */}
        <div className="space-y-1.5">
          <label className="text-[10px] uppercase tracking-widest text-[#a89070]">
            Party name
          </label>
          <input
            type="text"
            value={partyName}
            onChange={(e) => setPartyName(e.target.value)}
            placeholder="e.g. Heroes of Light"
            maxLength={40}
            className="w-full px-4 py-2.5 rounded-xl text-sm text-[#f3e5c8] bg-white/5 border border-white/10 outline-none focus:border-[#c9973b]/60 transition-colors placeholder:text-[#4a3a2a]"
          />
        </div>

        {/* Character cards */}
        <div className="space-y-2">
          <p className="text-[10px] uppercase tracking-widest text-[#a89070]">Your heroes</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {characters.map((char, i) => {
              const selectedJob = jobs.find((j) => j.id === parseInt(char.job_id));
              return (
                <div
                  key={i}
                  className="rounded-2xl border border-white/10 bg-white/5 p-4 space-y-3"
                >
                  <p className="text-[10px] uppercase tracking-widest text-[#6b5a45]">
                    Hero {i + 1}
                  </p>

                  <input
                    type="text"
                    value={char.name}
                    onChange={(e) => updateChar(i, "name", e.target.value)}
                    placeholder="Character name"
                    maxLength={30}
                    className="w-full px-3 py-2 rounded-xl text-sm text-[#f3e5c8] bg-white/5 border border-white/10 outline-none focus:border-[#c9973b]/60 transition-colors placeholder:text-[#4a3a2a]"
                  />

                  {jobsLoading ? (
                    <p className="text-xs text-[#6b5a45]">Loading classes...</p>
                  ) : (
                    <div className="relative">
                      <select
                        value={char.job_id}
                        onChange={(e) => updateChar(i, "job_id", e.target.value)}
                        className="w-full px-3 py-2 rounded-xl text-sm text-[#f3e5c8] bg-white/5 border border-white/10 outline-none focus:border-[#c9973b]/60 transition-colors appearance-none"
                        style={{ background: "rgba(255,255,255,0.04)" }}
                      >
                        <option value="">Select class...</option>
                        {jobs.map((job) => (
                          <option key={job.id} value={job.id}>
                            {job.icon}  {job.name}
                          </option>
                        ))}
                      </select>
                    </div>
                  )}

                  {selectedJob && (
                    <p className="text-[11px] text-[#c9973b]">
                      {selectedJob.icon} {selectedJob.name}
                    </p>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {error && (
          <p className="text-xs text-red-400 text-center">{error}</p>
        )}

        {/* Submit */}
        <button
          onClick={handleSubmit}
          disabled={!isValid || submitting}
          className="w-full py-3 rounded-xl text-sm font-bold uppercase tracking-wider transition-all duration-200 bg-[#c9973b]/20 border border-[#c9973b]/40 text-[#f3e5c8] hover:bg-[#c9973b]/30 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {submitting ? "Setting up..." : "Begin Adventure"}
        </button>
      </div>
    </div>
  );
};

export default OnboardingModal;
