// src/views/EquipmentView.jsx
import { useState, useEffect, useMemo } from "react";
import { useOutletContext } from "react-router-dom";
import { Dropdown } from "primereact/dropdown";
import { useInventory } from "../hooks/useInventory";
import { useUpdateEquipment } from "../hooks/useUpdateEquipment";

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
  const characters = party?.characters || [];

  const [selectedCharId, setSelectedCharId] = useState(null);
  const [selections, setSelections] = useState({});

  const selectedChar = characters.find((c) => c.id === selectedCharId) ?? characters[0];
  const jobId = selectedChar?.current_job?.id;

  const { data: inventory, loading } = useInventory();
  const { updateEquipment, saving } = useUpdateEquipment();

  const equipmentBySlot = useMemo(() => {
    const slots = {};
    inventory
      .filter((item) => item.equipment.job_id === jobId)
      .forEach((item) => {
        const eq = item.equipment;
        if (!slots[eq.type]) slots[eq.type] = [];
        slots[eq.type].push(eq);
      });
    selectedChar?.equipped_items?.forEach(({ slot, equipment }) => {
      if (!equipment) return;
      if (!slots[slot]) slots[slot] = [];
      if (!slots[slot].find((e) => e.id === equipment.id)) slots[slot].push(equipment);
    });
    return slots;
  }, [inventory, jobId, selectedChar]);

  useEffect(() => {
    if (characters.length > 0 && !selectedCharId) setSelectedCharId(characters[0].id);
  }, [characters]);

  useEffect(() => {
    if (selectedChar && inventory.length > 0) {
      setSelections((prev) => ({
        ...prev,
        [selectedChar.id]: buildInitialSelections(selectedChar, equipmentBySlot),
      }));
    }
  }, [selectedChar?.id, inventory]);

  const hasChanges = useMemo(() => {
    if (!selectedChar) return false;
    const charSelections = selections[selectedChar.id] ?? {};
    return SLOTS.some((slot) => {
      const selected = charSelections[slot];
      const equipped = selectedChar.equipped_items?.find((i) => i.slot === slot);
      return selected?.id !== equipped?.equipment?.id;
    });
  }, [selections, selectedChar]);

  const handleChange = (slot, value) => {
    setSelections((prev) => ({
      ...prev,
      [selectedChar.id]: { ...prev[selectedChar.id], [slot]: value },
    }));
  };

  const handleSave = async () => {
    const charSelections = selections[selectedChar.id] ?? {};
    const slotsToSave = SLOTS.filter((slot) => {
      const selected = charSelections[slot];
      const equipped = selectedChar.equipped_items?.find((i) => i.slot === slot);
      return selected?.id !== equipped?.equipment?.id;
    });
    try {
      await Promise.all(
        slotsToSave.map((slot) =>
          updateEquipment(selectedChar.id, slot, charSelections[slot].id)
        )
      );
      refetch();
    } catch {
      setSelections((prev) => ({
        ...prev,
        [selectedChar.id]: buildInitialSelections(selectedChar, equipmentBySlot),
      }));
    }
  };

  return (
    <div className="space-y-5">
      {/* CHARACTER TABS */}
      <div className="flex gap-2 flex-wrap">
        {characters.map((char) => (
          <button
            key={char.id}
            onClick={() => setSelectedCharId(char.id)}
            className={`px-5 py-2 rounded-xl text-sm font-semibold transition-all duration-200 border ${
              (selectedCharId ?? characters[0]?.id) === char.id
                ? "bg-accent-dim border-accent text-primary"
                : "bg-input border-soft text-secondary"
            }`}
          >
            {char.name}
          </button>
        ))}
      </div>

      {/* EQUIPMENT CARD */}
      {selectedChar && (
        <div className="w-full rounded-2xl overflow-hidden border border-soft bg-card shadow-card">
          {/* CARD HEADER */}
          <div className="border-b border-faint px-6 py-4 bg-card-header">
            <p className="text-[10px] uppercase tracking-widest text-muted">
              Managing equipment
            </p>
            <h3 className="text-xl font-bold text-primary">{selectedChar.name}</h3>
            <p className="text-sm capitalize text-accent-sub">
              {selectedChar.current_job?.name}
            </p>
          </div>

          {/* SLOTS */}
          <div className="p-6 flex gap-5 items-stretch">
            {/* CHARACTER AVATAR */}
            <div className="w-48 h-56 shrink-0 self-start rounded-xl border border-accent bg-accent-dim flex items-center justify-center overflow-hidden">
              {selectedChar.current_job?.icon ? (
                <img
                  src={selectedChar.current_job.icon}
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
                        disabled={saving}
                      />
                    </div>
                  ))
                )}
              </div>

              <div className="flex justify-end pt-1">
                <button
                  onClick={handleSave}
                  disabled={!hasChanges || saving}
                  className={`px-6 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 border ${
                    hasChanges && !saving
                      ? "bg-accent-dim border-accent text-primary cursor-pointer"
                      : "bg-input border-faint text-disabled cursor-not-allowed"
                  }`}
                >
                  {saving ? "Saving..." : "Save changes"}
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
