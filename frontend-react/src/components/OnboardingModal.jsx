import { useState } from "react";
import { Dropdown } from "primereact/dropdown";
import { apiFetch } from "../utils/apiFetch";
import useJobs from "../hooks/useJobs";

const dropdownPT = {
  root: {
    className:
      "relative w-full flex items-center bg-white/8 border border-white/15 rounded-xl " +
      "cursor-pointer hover:border-[#c9973b]/40 focus-within:border-[#c9973b]/60 transition-colors duration-200",
  },
  input: {
    className:
      "flex-1 px-4 py-2.5 text-sm text-[#f3e5c8] bg-transparent outline-none cursor-pointer truncate capitalize",
  },
  trigger: {
    className: "flex items-center justify-center w-10 text-[#a89070] shrink-0",
  },
  panel: {
    className: "border border-white/12 rounded-xl shadow-2xl overflow-hidden z-50",
    style: { background: "rgba(18, 9, 3, 0.97)", backdropFilter: "blur(12px)" },
  },
  wrapper: { className: "overflow-auto max-h-56" },
  list: { className: "p-1 m-0 list-none" },
  item: ({ context }) => ({
    className:
      "px-4 py-2.5 rounded-lg text-sm cursor-pointer transition-colors duration-150 mx-1 " +
      (context.selected
        ? "bg-[#c9973b]/20 text-[#f3e5c8] font-semibold"
        : "text-[#e6d3a3] hover:bg-white/8 hover:text-[#f3e5c8]"),
  }),
  emptyMessage: { className: "px-4 py-3 text-sm text-[#6b5a45] text-center" },
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
          characters: characters.map((c) => ({
            name: c.name.trim(),
            job_id: c.job.id,
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
      <div className="w-full max-w-4xl bg-[#0d0703] border border-white/10 rounded-3xl shadow-2xl p-6 sm:p-10 space-y-7 my-auto">

        {/* Header */}
        <div className="text-center space-y-1">
          <p className="text-sm uppercase tracking-widest text-[#a89070]">
            Welcome, {username}
          </p>
          <h2 className="text-2xl font-bold text-[#f3e5c8]">Set up your party</h2>
          <p className="text-sm text-[#6b5a45]">
            Name your party and choose a class for each of your four heroes.
          </p>
        </div>

        {/* Party name */}
        <div className="space-y-1.5">
          <label className="text-sm uppercase tracking-widest text-[#a89070]">
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
          <p className="text-sm uppercase tracking-widest text-[#a89070]">Your heroes</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {characters.map((char, i) => (
              <div
                key={i}
                className="rounded-2xl border border-white/10 bg-white/5 overflow-hidden"
              >
                {/* Card header */}
                <div className="bg-gradient-to-r from-[#1e1108]/90 to-[#150d05]/80 border-b border-white/8 px-4 py-3">
                  <span className="text-sm uppercase tracking-widest text-[#a89070]">Hero {i + 1}</span>
                </div>

                {/* Card body */}
                <div className="p-4 flex gap-3 items-stretch">
                  {/* Avatar */}
                  <div className="w-40 min-h-40 shrink-0 rounded-xl bg-[#c9973b]/10 border border-[#c9973b]/20 flex items-center justify-center overflow-hidden">
                    {char.job ? (
                      <img src={char.job.icon} alt={char.job.name} className="w-full h-full object-contain p-3" />
                    ) : (
                      <span className="text-4xl font-bold text-[#c9973b]/40">?</span>
                    )}
                  </div>

                  {/* Inputs */}
                  <div className="flex-1 flex flex-col gap-3 justify-center">
                    <input
                      type="text"
                      value={char.name}
                      onChange={(e) => updateChar(i, "name", e.target.value)}
                      placeholder="Character name"
                      maxLength={30}
                      className="w-full px-3 py-2 rounded-xl text-sm text-[#f3e5c8] bg-white/5 border border-white/10 outline-none focus:border-[#c9973b]/60 transition-colors placeholder:text-[#4a3a2a]"
                    />

                    {jobsLoading ? (
                      <p className="text-sm text-[#6b5a45]">Loading classes...</p>
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
          <p className="text-sm text-red-400 text-center">{error}</p>
        )}

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
