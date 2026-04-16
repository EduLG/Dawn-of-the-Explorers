import { useState, useEffect, useMemo } from "react";
import { useOutletContext } from "react-router-dom";
import { Dropdown } from "primereact/dropdown";
import { useEquipment } from "../hooks/useEquipment";
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
    <span className="text-xs text-[#c9973b] font-semibold shrink-0">
      +{option.rating}
    </span>
  </div>
);

const dropdownPT = {
  root: {
    className:
      "relative w-full flex items-center bg-white/8 border border-white/15 rounded-xl " +
      "cursor-pointer hover:border-[#c9973b]/40 focus-within:border-[#c9973b]/60 transition-colors duration-200",
  },
  input: {
    className:
      "flex-1 px-4 py-2.5 text-sm text-[#f3e5c8] bg-transparent outline-none cursor-pointer truncate",
  },
  trigger: {
    className: "flex items-center justify-center w-10 text-[#a89070] shrink-0",
  },
  panel: {
    className:
      "border border-white/12 rounded-xl shadow-2xl overflow-hidden z-50",
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

const buildInitialSelections = (character, equipmentBySlot) => {
  const result = {};
  SLOTS.forEach((slot) => {
    const equipped = character.equipped_items?.find((i) => i.slot === slot);
    const equippedId = equipped?.equipment?.id;
    const options = equipmentBySlot[slot] ?? [];
    result[slot] =
      options.find((o) => o.id === equippedId) ?? options[0] ?? null;
  });
  return result;
};

const EquipmentView = () => {
  const { party, refetch } = useOutletContext();
  const characters = party?.characters || [];

  const [selectedCharId, setSelectedCharId] = useState(null);
  const [selections, setSelections] = useState({});

  const selectedChar =
    characters.find((c) => c.id === selectedCharId) ?? characters[0];
  const jobId = selectedChar?.current_job?.id;

  const { data: equipment, loading } = useEquipment(jobId);
  const { updateEquipment, saving } = useUpdateEquipment();

  const equipmentBySlot = useMemo(() => {
    return equipment.reduce((acc, item) => {
      if (!acc[item.type]) acc[item.type] = [];
      acc[item.type].push(item);
      return acc;
    }, {});
  }, [equipment]);

  useEffect(() => {
    if (characters.length > 0 && !selectedCharId) {
      setSelectedCharId(characters[0].id);
    }
  }, [characters]);

  useEffect(() => {
    if (selectedChar && equipment.length > 0) {
      setSelections((prev) => ({
        ...prev,
        [selectedChar.id]: buildInitialSelections(
          selectedChar,
          equipmentBySlot,
        ),
      }));
    }
  }, [selectedChar?.id, equipment]);

  const handleChange = async (slot, value) => {
    const previous = selections[selectedChar.id]?.[slot];

    setSelections((prev) => ({
      ...prev,
      [selectedChar.id]: { ...prev[selectedChar.id], [slot]: value },
    }));

    try {
      await updateEquipment(selectedChar.id, slot, value.id);
      refetch();
    } catch {
      setSelections((prev) => ({
        ...prev,
        [selectedChar.id]: { ...prev[selectedChar.id], [slot]: previous },
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
                ? "bg-[#c9973b]/20 border-[#c9973b]/50 text-[#f3e5c8]"
                : "bg-white/5 border-white/10 text-[#a89070] hover:bg-white/10 hover:text-[#f3e5c8]"
            }`}
          >
            {char.name}
          </button>
        ))}
      </div>

      {/* EQUIPMENT CARD */}
      {selectedChar && (
        <div className="w-full rounded-2xl overflow-hidden border border-white/10 bg-white/5 backdrop-blur-md shadow-xl">
          {/* CARD HEADER */}
          <div className="bg-gradient-to-r from-[#1e1108]/90 to-[#150d05]/80 border-b border-white/8 px-6 py-4">
            <p className="text-[10px] uppercase tracking-widest text-[#a89070]">
              Managing equipment
            </p>
            <h3 className="text-xl font-bold text-[#f3e5c8]">
              {selectedChar.name}
            </h3>
            <p className="text-sm text-[#c9973b] capitalize">
              {selectedChar.current_job?.name}
            </p>
          </div>

          {/* SLOTS */}
          <div className="p-6 flex gap-5 items-stretch">
            {/* CHARACTER AVATAR */}
            <div className="w-48 h-56 shrink-0 self-start rounded-xl bg-[#c9973b]/10 border border-[#c9973b]/20 flex items-center justify-center overflow-hidden">
              {selectedChar.current_job?.icon ? (
                <img
                  src={selectedChar.current_job.icon}
                  alt={selectedChar.name}
                  className="w-full h-full object-contain p-3"
                />
              ) : (
                <span className="text-5xl font-bold text-[#c9973b]/60">
                  {selectedChar.name?.[0] ?? "?"}
                </span>
              )}
            </div>

            {/* DROPDOWNS */}
            <div className="flex-1 grid grid-cols-1 sm:grid-cols-2 gap-4 content-start">
              {loading ? (
                <p className="text-sm text-[#a89070] col-span-2">
                  Loading equipment...
                </p>
              ) : (
                SLOTS.map((slot) => (
                  <div key={slot} className="flex flex-col gap-1.5">
                    <label className="text-[10px] uppercase tracking-widest text-[#a89070]">
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
                      placeholder="No equipment available"
                      disabled={saving}
                    />
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EquipmentView;
