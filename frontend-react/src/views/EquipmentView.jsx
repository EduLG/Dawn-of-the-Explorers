// src/views/EquipmentView.jsx
import { useState, useEffect, useMemo } from "react";
import { useOutletContext } from "react-router-dom";
import { Dropdown } from "primereact/dropdown";
import { useInventory } from "../hooks/useInventory";
import { useUpdateEquipment } from "../hooks/useUpdateEquipment";
import useJobs from "../hooks/useJobs";
import { apiFetch } from "../utils/apiFetch";

const JOB_ARMOR_TYPE = {
  warrior: "plate", fender: "plate",
  adventurer: "leather", beastmaster: "leather",
  gunslinger: "leather", thief: "leather",
  alchemist: "cloth", engineer: "cloth",
  sage: "cloth", scholar: "cloth",
};

const SLOT_LABELS = {
  head: "Head",
  chest: "Chest",
  primary_hand: "Primary Hand",
  secondary_hand: "Secondary Hand",
  accesory: "Accessory",
};

const SLOTS = Object.keys(SLOT_LABELS);

const itemTemplate = (option) => (
  <div className="flex items-center justify-between gap-4">
    <span>{option.name}</span>
    <span className="text-xs font-semibold shrink-0 text-accent-sub">
      +{option.rating}
    </span>
  </div>
);

const jobTemplate = (option) => (
  <div className="flex items-center gap-3">
    <img src={option.icon} alt={option.name} className="w-5 h-5 object-contain" />
    <span className="capitalize">{option.name}</span>
  </div>
);

const dropdownPT = {
  root: {
    className:
      "relative w-full flex items-center rounded-xl cursor-pointer transition-colors duration-200 border bg-input border-field",
  },
  input: {
    className:
      "flex-1 px-4 py-2.5 text-sm bg-transparent outline-none cursor-pointer truncate text-primary",
  },
  trigger: {
    className: "flex items-center justify-center w-10 shrink-0 text-muted",
  },
  panel: {
    className:
      "border rounded-xl shadow-2xl overflow-hidden z-50 bg-modal border-soft backdrop-blur-md",
  },
  wrapper: { className: "overflow-auto max-h-56" },
  list: { className: "p-1 m-0 list-none" },
  item: ({ context }) => ({
    className: `px-4 py-2.5 rounded-lg text-sm cursor-pointer transition-colors duration-150 mx-1 ${
      context.selected
        ? "bg-accent-dim text-primary font-semibold"
        : "text-secondary"
    }`,
  }),
  emptyMessage: {
    className: "px-4 py-3 text-sm text-center text-muted",
  },
};

const buildInitialSelections = (character, equipmentBySlot) => {
  const result = {};
  SLOTS.forEach((slot) => {
    const equipped = character.equipped_items?.find((i) => i.slot === slot);
    const equippedId = equipped?.equipment?.id;
    const options = equipmentBySlot[slot] ?? [];
    result[slot] = options.find((o) => o.id === equippedId) ?? null;
  });
  return result;
};

const EquipmentView = () => {
  const { party, refetch } = useOutletContext();
  const characters = useMemo(
    () => [...(party?.characters || [])].sort((a, b) => a.id - b.id),
    [party?.characters],
  );

  const [selectedCharId, setSelectedCharId] = useState(null);
  const [selections, setSelections] = useState({});

  const [changingJob, setChangingJob] = useState(false);
  const [pendingJob, setPendingJob] = useState(null);
  const [jobSaving, setJobSaving] = useState(false);
  const [saveError, setSaveError] = useState(null);

  const selectedChar = characters.find((c) => c.id === selectedCharId) ?? characters[0];

  const currentJobName = pendingJob?.name ?? selectedChar?.current_job?.name;
  const armorType = JOB_ARMOR_TYPE[currentJobName];

  const { data: inventory, loading } = useInventory();
  const { updateEquipment, saving } = useUpdateEquipment();
  const { jobs } = useJobs();

  const equippedByOthers = useMemo(() => new Set(
    characters
      .filter((c) => c.id !== selectedChar?.id)
      .flatMap((c) => (c.equipped_items ?? []).map((ei) => ei.equipment?.id).filter(Boolean))
  ), [characters, selectedChar?.id]);

  const equipmentBySlot = useMemo(() => {
    const slots = {};
    inventory
      .filter((item) => item.equipment.equipment_type === armorType && !equippedByOthers.has(item.equipment.id))
      .forEach((item) => {
        const eq = item.equipment;
        if (!slots[eq.slot]) slots[eq.slot] = [];
        slots[eq.slot].push(eq);
      });
    // Only include currently equipped items if we haven't changed the job
    if (!pendingJob) {
      selectedChar?.equipped_items?.forEach(({ slot, equipment }) => {
        if (!equipment) return;
        if (!slots[slot]) slots[slot] = [];
        if (!slots[slot].find((e) => e.id === equipment.id)) slots[slot].push(equipment);
      });
    }
    return slots;
  }, [inventory, armorType, selectedChar, pendingJob, equippedByOthers]);

  useEffect(() => {
    if (characters.length > 0 && !selectedCharId) setSelectedCharId(characters[0].id);
  }, [characters]);

  // Rebuild selections whenever the relevant axes change:
  // - character switch, confirmed job change, inventory reload → restore from equipped items
  // - pending job chosen → blank slate for the new job
  // - pending job cancelled (null) → restore from equipped items
  useEffect(() => {
    if (!selectedChar || !inventory.length) return;
    if (pendingJob) {
      setSelections((prev) => ({ ...prev, [selectedChar.id]: {} }));
    } else {
      setSelections((prev) => ({
        ...prev,
        [selectedChar.id]: buildInitialSelections(selectedChar, equipmentBySlot),
      }));
    }
  }, [selectedChar?.id, selectedChar?.current_job?.id, inventory, pendingJob?.id]);

  const jobChanged = !!(pendingJob && pendingJob.id !== selectedChar?.current_job?.id);

  const hasChanges = useMemo(() => {
    if (!selectedChar) return false;
    if (jobChanged) return true;
    const charSelections = selections[selectedChar.id] ?? {};
    return SLOTS.some((slot) => {
      const selected = charSelections[slot];
      const equipped = selectedChar.equipped_items?.find((i) => i.slot === slot);
      return selected?.id !== equipped?.equipment?.id;
    });
  }, [selections, selectedChar, jobChanged]);

  const handleChange = (slot, value) => {
    setSelections((prev) => ({
      ...prev,
      [selectedChar.id]: { ...prev[selectedChar.id], [slot]: value },
    }));
  };

  const handleSave = async () => {
    setSaveError(null);
    try {
      // 1. Apply job change first if one is pending
      if (jobChanged) {
        setJobSaving(true);
        const res = await apiFetch(`/api/v1/characters/${selectedChar.id}/job`, {
          method: "PATCH",
          body: JSON.stringify({ job_id: pendingJob.id }),
        });
        if (!res.ok) {
          const body = await res.json();
          throw new Error(body.error || "Failed to change job");
        }
        setJobSaving(false);
      }

      // 2. Apply equipment changes for the (new) job
      const charSelections = selections[selectedChar.id] ?? {};
      const slotsToSave = SLOTS.filter((slot) => {
        const selected = charSelections[slot];
        if (!selected) return false;
        if (jobChanged) return true; // backend cleared all, save anything selected
        const equipped = selectedChar.equipped_items?.find((i) => i.slot === slot);
        return selected?.id !== equipped?.equipment?.id;
      });

      if (slotsToSave.length > 0) {
        await Promise.all(
          slotsToSave.map((slot) =>
            updateEquipment(selectedChar.id, slot, charSelections[slot].id)
          )
        );
      }

      setChangingJob(false);
      setPendingJob(null);
      refetch();
    } catch (err) {
      setSaveError(err.message);
      setJobSaving(false);
    }
  };

  const handleCharSelect = (charId) => {
    setSelectedCharId(charId);
    setChangingJob(false);
    setPendingJob(null);
    setSaveError(null);
  };

  const isSaving = saving || jobSaving;

  return (
    <div className="space-y-5">
      {/* CHARACTER TABS */}
      <div className="grid grid-cols-2 gap-2">
        {characters.map((char) => (
          <button
            key={char.id}
            onClick={() => handleCharSelect(char.id)}
            className={`w-full px-5 py-2 rounded-xl text-sm font-semibold text-center transition-all duration-200 border ${
              (selectedCharId ?? characters[0]?.id) === char.id
                ? "bg-accent-dim border-accent text-primary"
                : "bg-input border-soft text-secondary"
            }`}
          >
            {char.name}
          </button>
        ))}
      </div>

      {/* CHARACTER CARD */}
      {selectedChar && (
        <div className="w-full rounded-2xl overflow-hidden border border-soft bg-card shadow-card">
          {/* CARD HEADER */}
          <div className="border-b border-faint px-6 py-4 bg-card-header flex items-start justify-between gap-4">
            <div>
              <p className="text-[10px] uppercase tracking-widest text-muted">
                Character
              </p>
              <h3 className="text-xl font-bold text-primary">{selectedChar.name}</h3>
              <p className={`text-sm capitalize ${pendingJob ? "line-through text-muted" : "text-accent-sub"}`}>
                {selectedChar.current_job?.name}
              </p>
              {pendingJob && (
                <p className="text-sm capitalize text-accent-sub">{pendingJob.name}</p>
              )}
            </div>
            <button
              onClick={() => {
                setChangingJob((v) => !v);
                setPendingJob(null);
                setSaveError(null);
              }}
              className={`mt-1 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all duration-200 border shrink-0 ${
                changingJob
                  ? "bg-accent-dim border-accent text-primary"
                  : "bg-input border-soft text-secondary"
              }`}
            >
              {changingJob ? "Cancel" : "Change Job"}
            </button>
          </div>

          {/* JOB CHANGE PANEL — selection only, applied via Save changes */}
          {changingJob && (
            <div className="border-b border-faint px-6 py-4 space-y-2 bg-card-header">
              <label className="text-[10px] uppercase tracking-widest text-muted">
                New Job
              </label>
              <Dropdown
                unstyled
                pt={dropdownPT}
                value={pendingJob}
                onChange={(e) => setPendingJob(e.value)}
                options={jobs}
                optionLabel="name"
                itemTemplate={jobTemplate}
                valueTemplate={pendingJob ? jobTemplate : undefined}
                placeholder="Select a job..."
              />
              {pendingJob && (
                <p className="text-[11px] text-status-red">
                  Changing job will unequip all currently equipped items.
                </p>
              )}
            </div>
          )}

          {/* EQUIPMENT SLOTS */}
          <div className="p-6 flex flex-col sm:flex-row gap-5 items-stretch">
            {/* CHARACTER AVATAR */}
            <div className="w-full h-48 sm:w-48 sm:h-56 sm:shrink-0 sm:self-start rounded-xl border border-accent bg-accent-dim flex items-center justify-center overflow-hidden">
              {(pendingJob ?? selectedChar.current_job)?.icon ? (
                <img
                  src={(pendingJob ?? selectedChar.current_job).icon}
                  alt={selectedChar.name}
                  className="w-full h-full object-contain p-3"
                />
              ) : (
                <span className="text-5xl font-bold text-accent opacity-60">
                  {selectedChar.name?.[0] ?? "?"}
                </span>
              )}
            </div>

            {/* DROPDOWNS + SAVE */}
            <div className="flex-1 flex flex-col gap-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {loading ? (
                  <p className="text-sm col-span-2 text-muted">
                    Loading equipment...
                  </p>
                ) : (
                  SLOTS.map((slot) => (
                    <div key={slot} className="flex flex-col gap-1.5">
                      <label className="text-[10px] uppercase tracking-widest text-muted">
                        {SLOT_LABELS[slot]}
                      </label>
                      <Dropdown
                        unstyled
                        pt={dropdownPT}
                        value={selections[selectedChar.id]?.[slot] ?? null}
                        onChange={(e) => handleChange(slot, e.value)}
                        options={equipmentBySlot[slot] ?? []}
                        optionLabel="name"
                        itemTemplate={itemTemplate}
                        placeholder="No item equipped"
                        disabled={isSaving}
                      />
                    </div>
                  ))
                )}
              </div>

              {saveError && (
                <p className="text-xs text-status-red">{saveError}</p>
              )}

              <div className="flex justify-end pt-1">
                <button
                  onClick={handleSave}
                  disabled={!hasChanges || isSaving}
                  className={`px-6 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 border ${
                    hasChanges && !isSaving
                      ? "bg-accent-dim border-accent text-primary cursor-pointer"
                      : "bg-input border-faint text-disabled cursor-not-allowed"
                  }`}
                >
                  {isSaving ? "Saving..." : "Save changes"}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EquipmentView;
