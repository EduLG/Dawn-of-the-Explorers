import { useState, useEffect, useMemo } from "react";
import { useOutletContext } from "react-router-dom";
import { useInventory } from "../hooks/useInventory";
import { useUpdateEquipment } from "../hooks/useUpdateEquipment";
import characterPreviewImg from "../assets/resources/character_preview.png";

const JOB_ARMOR_TYPE = {
  warrior: "plate",
  fender: "plate",
  adventurer: "leather",
  beastmaster: "leather",
  gunslinger: "leather",
  thief: "leather",
  alchemist: "cloth",
  engineer: "cloth",
  sage: "cloth",
  scholar: "cloth",
};

const SLOT_LABELS = {
  head: "Head",
  chest: "Chest",
  primary_hand: "P.Hand",
  secondary_hand: "S.Hand",
  accesory: "Acc.",
};

const SLOTS = Object.keys(SLOT_LABELS);

const EquipmentView = () => {
  const { party, refetch } = useOutletContext();
  const characters = useMemo(
    () => [...(party?.characters || [])].sort((a, b) => a.id - b.id),
    [party?.characters],
  );

  const [selectedCharId, setSelectedCharId] = useState(null);
  const [activeSlot, setActiveSlot] = useState(null);

  const selectedChar =
    characters.find((c) => c.id === selectedCharId) ?? characters[0];
  const armorType = JOB_ARMOR_TYPE[selectedChar?.current_job?.name];

  const {
    data: inventory,
    loading,
    refetch: refetchInventory,
  } = useInventory();
  const { updateEquipment, saving } = useUpdateEquipment();

  useEffect(() => {
    if (characters.length > 0 && !selectedCharId)
      setSelectedCharId(characters[0].id);
  }, [characters]);

  const equippedBySelectedChar = useMemo(
    () =>
      new Set(
        (selectedChar?.equipped_items ?? [])
          .map((ei) => ei.inventory_id)
          .filter(Boolean),
      ),
    [selectedChar],
  );

  const getEquippedItemName = (slot) =>
    selectedChar?.equipped_items?.find((i) => i.slot === slot)?.equipment
      ?.name ?? "—";

  const availableItems = useMemo(() => {
    if (!activeSlot || !selectedChar) return [];
    return inventory.filter(
      (item) =>
        item.equipment.slot === activeSlot &&
        item.equipment.equipment_type === armorType &&
        (!item.equipped || equippedBySelectedChar.has(item.id)),
    );
  }, [activeSlot, inventory, armorType, selectedChar, equippedBySelectedChar]);

  const equippedIdForActiveSlot =
    selectedChar?.equipped_items?.find((i) => i.slot === activeSlot)
      ?.inventory_id ?? null;

  const handleSlotClick = (slot) =>
    setActiveSlot((prev) => (prev === slot ? null : slot));

  const handleEquip = async (item) => {
    if (saving || equippedIdForActiveSlot === item.id) return;
    await updateEquipment(item.id, selectedChar.id, activeSlot);
    refetch();
    refetchInventory();
  };

  const handleCharSelect = (charId) => {
    setSelectedCharId(charId);
    setActiveSlot(null);
  };

  return (
    <div className="space-y-4">
      {/* CHARACTER TABS */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
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

      {/* MAIN PANEL */}
      {selectedChar && (() => {
        const slotButtons = SLOTS.map((slot) => (
          <button
            key={slot}
            onClick={() => handleSlotClick(slot)}
            className={`w-full sm:w-64 flex items-center gap-3 px-4 py-2.5 rounded-xl text-left border transition-[filter] duration-150 ${
              activeSlot === slot
                ? "bg-accent-dim border-accent text-primary"
                : "bg-input border-soft text-secondary hover:brightness-125"
            }`}
          >
            <span className="text-[10px] uppercase tracking-widest text-muted w-16 shrink-0">
              {SLOT_LABELS[slot]}
            </span>
            <span className={`text-sm truncate ${activeSlot === slot ? "font-semibold" : ""}`}>
              {getEquippedItemName(slot)}
            </span>
          </button>
        ));

        const avatar = selectedChar.current_job?.icon ? (
          <img src={selectedChar.current_job.icon} alt={selectedChar.name} className="w-28 object-contain" />
        ) : (
          <span className="text-4xl font-bold text-accent opacity-60">{selectedChar.name?.[0] ?? "?"}</span>
        );

        return (
          <>
            {/* MOBILE: avatar arriba sin fondo, botones debajo */}
            <div className="sm:hidden flex flex-col gap-4">
              <div className="flex justify-center py-6 rounded-2xl border border-soft bg-card">
                {avatar}
              </div>
              <div className="flex flex-col gap-2 w-full">
                {slotButtons}
              </div>
            </div>

            {/* DESKTOP: layout con imagen de fondo */}
            <div
              className="hidden sm:flex rounded-2xl border border-soft overflow-hidden min-h-[220px]"
              style={{ backgroundImage: `url(${characterPreviewImg})`, backgroundSize: "cover", backgroundPosition: "bottom right" }}
            >
              <div className="flex-1 flex items-center justify-center" style={{ transform: "translateX(0.5rem)" }}>
                <img src={selectedChar.current_job?.icon} alt={selectedChar.name} className="w-44 object-contain" />
              </div>
              <div className="flex items-center py-6 px-8 bg-card">
                <div className="flex flex-col gap-2">{slotButtons}</div>
              </div>
            </div>
          </>
        );
      })()}

      {/* ITEM LIST PANEL */}
      {activeSlot && selectedChar && (
        <div className="rounded-2xl border border-soft bg-card overflow-hidden">
          <div className="px-4 py-2.5 border-b border-faint bg-card-header">
            <p className="text-[10px] uppercase tracking-widest text-muted">
              {SLOT_LABELS[activeSlot]}
            </p>
          </div>

          {loading ? (
            <p className="px-4 py-4 text-sm text-muted">Loading...</p>
          ) : availableItems.length === 0 ? (
            <p className="px-4 py-4 text-sm text-muted">
              No items available for this slot.
            </p>
          ) : (
            <ul>
              {availableItems.map((item) => {
                const isEquipped = equippedIdForActiveSlot === item.id;
                return (
                  <li
                    key={item.id}
                    className="border-b border-faint last:border-0"
                  >
                    <button
                      onClick={() => handleEquip(item)}
                      disabled={saving}
                      className={`w-full flex items-center justify-between px-4 py-3 text-sm transition-colors duration-150 ${
                        isEquipped
                          ? "bg-accent-dim text-primary font-semibold cursor-default"
                          : "text-secondary hover:bg-white/5 cursor-pointer"
                      }`}
                    >
                      <span>{item.equipment.name}</span>
                      <span className="text-xs font-semibold text-accent-sub shrink-0 ml-4">
                        +{item.equipment.rating}
                      </span>
                    </button>
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default EquipmentView;
