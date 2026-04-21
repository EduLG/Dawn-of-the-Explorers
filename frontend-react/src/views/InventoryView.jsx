import { useState } from "react";
import { useOutletContext } from "react-router-dom";
import { useInventory } from "../hooks/useInventory";
import { apiFetch } from "../utils/apiFetch";
import headIcon from "../assets/resources/eq_icons/head.svg";
import chestIcon from "../assets/resources/eq_icons/chest.svg";
import handIcon from "../assets/resources/eq_icons/hand.svg";
import accesoryIcon from "../assets/resources/eq_icons/accesory.svg";

const SLOT_LABELS = {
  head: "Head",
  chest: "Chest",
  primary_hand: "Primary Hand",
  secondary_hand: "Secondary Hand",
  accesory: "Accessory",
};

const SLOT_FILTERS = ["All", ...Object.keys(SLOT_LABELS)];

const SLOT_ICON_MAP = {
  head: { src: headIcon },
  chest: { src: chestIcon },
  primary_hand: { src: handIcon },
  secondary_hand: { src: handIcon, flip: true },
  accesory: { src: accesoryIcon },
};

const SlotIcon = ({ type }) => {
  const icon = SLOT_ICON_MAP[type];
  if (!icon) return null;
  return (
    <img
      src={icon.src}
      alt={type}
      className="w-7 h-7"
      style={icon.flip ? { transform: "scaleX(-1)" } : undefined}
    />
  );
};

const InventoryView = () => {
  const { party, refetch: refetchParty } = useOutletContext();
  const {
    data: inventory,
    loading,
    refetch: refetchInventory,
  } = useInventory();

  const [filter, setFilter] = useState("All");
  const [equipping, setEquipping] = useState(null); // inventory_id being equipped
  const [equipState, setEquipState] = useState({}); // { [invId]: { charId, slot } }
  const [saving, setSaving] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  const characters = party?.characters || [];

  const filtered =
    filter === "All"
      ? inventory
      : inventory.filter((i) => i.equipment.type === filter);

  const handleEquipToggle = (invId) => {
    setEquipping((prev) => (prev === invId ? null : invId));
    setErrorMsg(null);
  };

  const handleEquipStateChange = (invId, field, value) => {
    setEquipState((prev) => ({
      ...prev,
      [invId]: { ...(prev[invId] || {}), [field]: value },
    }));
  };

  const handleConfirmEquip = async (invId) => {
    const { charId, slot } = equipState[invId] || {};
    if (!charId || !slot) {
      setErrorMsg("Select a character and a slot.");
      return;
    }

    setSaving(true);
    setErrorMsg(null);
    try {
      const res = await apiFetch(`/api/v1/inventory/${invId}/equip`, {
        method: "POST",
        body: JSON.stringify({ character_id: parseInt(charId), slot }),
      });
      if (!res.ok) {
        const body = await res.json();
        throw new Error(body.error || "Failed to equip item");
      }
      setEquipping(null);
      setEquipState((prev) => {
        const next = { ...prev };
        delete next[invId];
        return next;
      });
      refetchInventory();
      refetchParty();
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-5">
      {/* HEADER */}
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <p className="text-[10px] uppercase tracking-widest text-[#a89070]">
            Party Loot
          </p>
          <h2 className="text-2xl font-bold text-[#f3e5c8]">Inventory</h2>
        </div>
        <span className="text-sm text-[#a89070]">
          {inventory.length} item{inventory.length !== 1 ? "s" : ""}
        </span>
      </div>

      {/* SLOT FILTER TABS */}
      <div className="flex gap-2 flex-wrap">
        {SLOT_FILTERS.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-4 py-1.5 rounded-xl text-xs font-semibold transition-all duration-200 border ${
              filter === f
                ? "bg-[#c9973b]/20 border-[#c9973b]/50 text-[#f3e5c8]"
                : "bg-white/5 border-white/10 text-[#a89070] hover:bg-white/10 hover:text-[#f3e5c8]"
            }`}
          >
            {f === "All" ? "All" : SLOT_LABELS[f]}
          </button>
        ))}
      </div>

      {/* CONTENT */}
      {loading ? (
        <p className="text-sm text-[#a89070]">Loading inventory...</p>
      ) : filtered.length === 0 ? (
        <div className="rounded-2xl border border-white/10 bg-white/5 p-10 text-center">
          <p className="text-[#a89070] text-sm">
            {filter === "All"
              ? "Your inventory is empty. Complete quests to earn loot!"
              : "No items of this type in inventory."}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
          {filtered.map((invItem) => {
            const eq = invItem.equipment;
            const isExpanded = equipping === invItem.id;
            const state = equipState[invItem.id] || {};
            const compatibleChars = characters.filter(
              (c) => c.current_job?.id === eq.job_id,
            );

            return (
              <div
                key={invItem.id}
                className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-md overflow-hidden shadow-lg"
              >
                {/* ITEM ROW */}
                <div className="flex items-center gap-4 px-5 py-4">
                  {/* SLOT ICON */}
                  <div className="w-12 h-12 shrink-0 rounded-xl bg-[#c9973b]/10 border border-[#c9973b]/20 flex items-center justify-center">
                    <SlotIcon type={eq.type} />
                  </div>

                  {/* INFO */}
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold text-[#f3e5c8] truncate">
                      {eq.name}
                    </p>
                    <p className="text-xs text-[#a89070] capitalize">
                      {SLOT_LABELS[eq.type] ?? eq.type} · {eq.job_name}
                    </p>
                  </div>

                  {/* RATING */}
                  <div className="text-right shrink-0">
                    <p className="text-lg font-bold text-[#c9973b]">
                      +{eq.rating}
                    </p>
                    <p className="text-[10px] uppercase tracking-wider text-[#6b5a45]">
                      Rating
                    </p>
                  </div>
                </div>

                {/* EQUIP BUTTON */}
                <div className="px-5 pb-4">
                  <button
                    onClick={() => handleEquipToggle(invItem.id)}
                    className={`w-full py-2 rounded-xl text-sm font-semibold transition-all duration-200 border ${
                      isExpanded
                        ? "bg-[#c9973b]/20 border-[#c9973b]/40 text-[#f3e5c8]"
                        : "bg-white/5 border-white/10 text-[#a89070] hover:bg-white/10 hover:text-[#f3e5c8]"
                    }`}
                  >
                    {isExpanded ? "Cancel" : "Equip"}
                  </button>
                </div>

                {/* EQUIP PANEL */}
                {isExpanded && (
                  <div className="border-t border-white/8 bg-[#1e1108]/60 px-5 py-4 space-y-3">
                    {compatibleChars.length === 0 ? (
                      <p className="text-xs text-[#a89070] text-center">
                        No characters with the required job ({eq.job_name}).
                      </p>
                    ) : (
                      <>
                        <div className="flex flex-col gap-1.5">
                          <label className="text-[10px] uppercase tracking-widest text-[#a89070]">
                            Character
                          </label>
                          <select
                            value={state.charId || ""}
                            onChange={(e) =>
                              handleEquipStateChange(
                                invItem.id,
                                "charId",
                                e.target.value,
                              )
                            }
                            className="w-full px-3 py-2 rounded-xl text-sm text-[#f3e5c8] bg-white/8 border border-white/15 outline-none focus:border-[#c9973b]/60 transition-colors"
                            style={{ background: "rgba(255,255,255,0.05)" }}
                          >
                            <option value="">Select character...</option>
                            {compatibleChars.map((c) => (
                              <option key={c.id} value={c.id}>
                                {c.name}
                              </option>
                            ))}
                          </select>
                        </div>

                        <div className="flex flex-col gap-1.5">
                          <label className="text-[10px] uppercase tracking-widest text-[#a89070]">
                            Slot
                          </label>
                          <select
                            value={state.slot || ""}
                            onChange={(e) =>
                              handleEquipStateChange(
                                invItem.id,
                                "slot",
                                e.target.value,
                              )
                            }
                            className="w-full px-3 py-2 rounded-xl text-sm text-[#f3e5c8] bg-white/8 border border-white/15 outline-none focus:border-[#c9973b]/60 transition-colors"
                            style={{ background: "rgba(255,255,255,0.05)" }}
                          >
                            <option value="">Select slot...</option>
                            <option value={eq.type}>
                              {SLOT_LABELS[eq.type] ?? eq.type}
                            </option>
                          </select>
                        </div>

                        {errorMsg && (
                          <p className="text-xs text-red-400">{errorMsg}</p>
                        )}

                        <button
                          onClick={() => handleConfirmEquip(invItem.id)}
                          disabled={saving}
                          className="w-full py-2 rounded-xl text-sm font-semibold bg-[#c9973b]/20 border border-[#c9973b]/40 text-[#f3e5c8] hover:bg-[#c9973b]/30 transition-all duration-200 disabled:opacity-50"
                        >
                          {saving ? "Equipping..." : "Confirm"}
                        </button>
                      </>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default InventoryView;
