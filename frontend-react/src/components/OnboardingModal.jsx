// src/components/OnboardingModal.jsx
import { useState } from "react";
import { Dropdown } from "primereact/dropdown";
import { apiFetch } from "../utils/apiFetch";
import useJobs from "../hooks/useJobs";

const dropdownPT = {
  root: {
    className: "relative w-full flex items-center rounded-xl cursor-pointer transition-colors duration-200 border",
    style: { background: "var(--bg-input)", borderColor: "var(--border-input)" },
  },
  input: {
    className: "flex-1 px-4 py-2.5 text-sm bg-transparent outline-none cursor-pointer truncate capitalize",
    style: { color: "var(--text-primary)" },
  },
  trigger: {
    className: "flex items-center justify-center w-10 shrink-0",
    style: { color: "var(--text-muted)" },
  },
  panel: {
    className: "border rounded-xl shadow-2xl overflow-hidden z-50",
    style: { background: "var(--bg-modal)", borderColor: "var(--border-soft)", backdropFilter: "blur(12px)" },
  },
  wrapper: { className: "overflow-auto max-h-56" },
  list: { className: "p-1 m-0 list-none" },
  item: ({ context }) => ({
    className: "px-4 py-2.5 rounded-lg text-sm cursor-pointer transition-colors duration-150 mx-1",
    style: context.selected
      ? { background: "var(--accent-dim)", color: "var(--text-primary)", fontWeight: 600 }
      : { color: "var(--text-secondary)" },
  }),
  emptyMessage: {
    className: "px-4 py-3 text-sm text-center",
    style: { color: "var(--text-muted)" },
  },
};

const jobItemTemplate = (option) => (
  <div className="flex items-center gap-3">
    <img src={option.icon} alt={option.name} className="w-6 h-6 object-contain" />
    <span className="capitalize">{option.name}</span>
  </div>
);

const EMPTY_CHAR = { name: "", job: null };

const OnboardingModal = ({ username, onComplete }) => {
  const { jobs, loading: jobsLoading } = useJobs();

  const [partyName, setPartyName] = useState("");
  const [characters, setCharacters] = useState([
    { ...EMPTY_CHAR }, { ...EMPTY_CHAR }, { ...EMPTY_CHAR }, { ...EMPTY_CHAR },
  ]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const updateChar = (index, field, value) =>
    setCharacters((prev) => prev.map((c, i) => (i === index ? { ...c, [field]: value } : c)));

  const isValid =
    partyName.trim().length > 0 &&
    characters.every((c) => c.name.trim().length > 0 && c.job !== null);

  const handleSubmit = async () => {
    if (!isValid) return;
    setSubmitting(true);
    setError(null);
    try {
      const res = await apiFetch("/api/v1/party/setup", {
        method: "POST",
        body: JSON.stringify({
          party_name: partyName.trim(),
          characters: characters.map((c) => ({ name: c.name.trim(), job_id: c.job.id })),
        }),
      });
      if (!res.ok) { const body = await res.json(); throw new Error(body.error || "Setup failed"); }
      onComplete();
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const inputStyle = {
    width: "100%",
    padding: "10px 16px",
    borderRadius: "12px",
    fontSize: "14px",
    border: "1px solid var(--border-input)",
    background: "var(--bg-input)",
    color: "var(--text-primary)",
    outline: "none",
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm px-4 py-8 overflow-y-auto"
      style={{ background: "oklch(0 0 0 / 0.65)" }}
    >
      <div
        className="w-full max-w-4xl rounded-3xl shadow-[var(--shadow-modal)] p-6 sm:p-10 space-y-7 my-auto border"
        style={{ background: "var(--bg-modal)", borderColor: "var(--border-soft)" }}
      >
        {/* Header */}
        <div className="text-center space-y-1">
          <p className="text-sm uppercase tracking-widest" style={{ color: "var(--text-muted)" }}>
            Welcome, {username}
          </p>
          <h2 className="text-2xl font-bold" style={{ color: "var(--text-primary)" }}>
            Set up your party
          </h2>
          <p className="text-sm" style={{ color: "var(--text-secondary)" }}>
            Name your party and choose a class for each of your four heroes.
          </p>
        </div>

        {/* Party name */}
        <div className="space-y-1.5">
          <label className="text-sm uppercase tracking-widest" style={{ color: "var(--text-muted)" }}>
            Party name
          </label>
          <input
            type="text"
            value={partyName}
            onChange={(e) => setPartyName(e.target.value)}
            placeholder="e.g. Heroes of Light"
            maxLength={40}
            style={{ ...inputStyle, "::placeholder": { color: "var(--text-placeholder)" } }}
          />
        </div>

        {/* Character cards */}
        <div className="space-y-2">
          <p className="text-sm uppercase tracking-widest" style={{ color: "var(--text-muted)" }}>
            Your heroes
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {characters.map((char, i) => (
              <div
                key={i}
                className="rounded-2xl border overflow-hidden"
                style={{ background: "var(--bg-card)", borderColor: "var(--border-soft)" }}
              >
                {/* Card header */}
                <div
                  className="border-b px-4 py-3"
                  style={{ background: "var(--bg-card-header)", borderColor: "var(--border-faint)" }}
                >
                  <span className="text-sm uppercase tracking-widest" style={{ color: "var(--text-muted)" }}>
                    Hero {i + 1}
                  </span>
                </div>

                {/* Card body */}
                <div className="p-4 flex gap-3 items-stretch">
                  <div
                    className="w-40 min-h-40 shrink-0 rounded-xl border flex items-center justify-center overflow-hidden"
                    style={{ background: "var(--accent-dim)", borderColor: "var(--accent-border)" }}
                  >
                    {char.job ? (
                      <img src={char.job.icon} alt={char.job.name} className="w-full h-full object-contain p-3" />
                    ) : (
                      <span className="text-4xl font-bold" style={{ color: "var(--accent)", opacity: 0.4 }}>?</span>
                    )}
                  </div>

                  <div className="flex-1 flex flex-col gap-3 justify-center">
                    <input
                      type="text"
                      value={char.name}
                      onChange={(e) => updateChar(i, "name", e.target.value)}
                      placeholder="Character name"
                      maxLength={30}
                      style={inputStyle}
                    />
                    {jobsLoading ? (
                      <p className="text-sm" style={{ color: "var(--text-muted)" }}>Loading classes...</p>
                    ) : (
                      <Dropdown
                        unstyled
                        pt={dropdownPT}
                        value={char.job}
                        onChange={(e) => updateChar(i, "job", e.value)}
                        options={jobs}
                        optionLabel="name"
                        itemTemplate={jobItemTemplate}
                        placeholder="Select class..."
                      />
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {error && (
          <p className="text-sm text-center" style={{ color: "var(--status-red-text)" }}>{error}</p>
        )}

        <button
          onClick={handleSubmit}
          disabled={!isValid || submitting}
          className="w-full py-3 rounded-xl text-sm font-bold uppercase tracking-wider transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed border"
          style={{ background: "var(--accent-dim)", borderColor: "var(--accent-border)", color: "var(--text-primary)" }}
        >
          {submitting ? "Setting up..." : "Begin Adventure"}
        </button>
      </div>
    </div>
  );
};

export default OnboardingModal;
