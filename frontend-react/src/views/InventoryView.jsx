// src/views/InventoryView.jsx
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
  const [equipping, setEquipping] = useState(null);
  const [equipState, setEquipState] = useState({});
  const [saving, setSaving] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);
  const [pendingDelete, setPendingDelete] = useState(null);
  const [deleting, setDeleting] = useState(false);

  const characters = party?.characters || [];
  const filtered =
    filter === "All"
      ? inventory
      : inventory.filter((i) => i.equipment.type === filter);

  const handleEquipToggle = (invId) => {
    setPendingDelete(null);
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

  const handleDeleteClick = (invItem) => {
    setEquipping(null);
    setErrorMsg(null);
    const equippedByChar = characters.find((c) =>
      c.equipped_items?.some((ei) => ei.equipment?.id === invItem.equipment.id),
    );
    setPendingDelete({
      invId: invItem.id,
      equippedByName: equippedByChar ? equippedByChar.name : null,
    });
  };

  const handleCancelDelete = () => setPendingDelete(null);

  const handleConfirmDelete = async (force = false) => {
    if (!pendingDelete) return;
    setDeleting(true);
    try {
      const res = await apiFetch(`/api/v1/inventory/${pendingDelete.invId}`, {
        method: "DELETE",
        body: JSON.stringify({ force }),
      });
      if (!res.ok) {
        const body = await res.json();
        throw new Error(body.error || "Failed to delete item");
      }
      setPendingDelete(null);
      refetchInventory();
      refetchParty();
    } catch {
      /* ignore */
    } finally {
      setDeleting(false);
    }
  };

  return (
    <div className="space-y-5">
      {/* HEADER */}
      <div className="border border-soft rounded-2xl px-6 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 bg-card">
        <div>
          <h2 className="text-2xl font-bold text-primary">Inventory</h2>
        </div>
        <span className="text-sm text-muted">
          {inventory.length} item{inventory.length !== 1 ? "s" : ""}
        </span>
      </div>

      {/* SLOT FILTER TABS */}
      <div className="grid grid-cols-2 gap-2">
        {SLOT_FILTERS.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`w-full px-4 py-1.5 rounded-xl text-xs font-semibold text-center transition-all duration-200 border ${
              filter === f
                ? "bg-accent-dim border-accent text-primary"
                : "bg-input border-soft text-secondary"
            }`}
          >
            {f === "All" ? "All" : SLOT_LABELS[f]}
          </button>
        ))}
      </div>

      {/* CONTENT */}
      {loading ? (
        <p className="text-sm text-muted">Loading inventory...</p>
      ) : filtered.length === 0 ? (
        <div className="rounded-2xl border border-soft bg-card p-10 text-center">
          <p className="text-sm text-muted">
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
            const isConfirmingDelete = pendingDelete?.invId === invItem.id;
            const state = equipState[invItem.id] || {};
            const compatibleChars = characters.filter(
              (c) => c.current_job?.id === eq.job_id,
            );

            return (
              <div
                key={invItem.id}
                className="rounded-2xl border border-soft bg-card overflow-hidden shadow-card"
              >
                {/* ITEM ROW */}
                <div className="flex items-center gap-4 px-5 py-4">
                  <div className="w-12 h-12 shrink-0 rounded-xl border border-accent bg-accent-dim flex items-center justify-center">
                    <SlotIcon type={eq.type} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold truncate text-primary">
                      {eq.name}
                    </p>
                    <p className="text-xs capitalize text-muted">
                      {SLOT_LABELS[eq.type] ?? eq.type} · {eq.job_name}
                    </p>
                  </div>
                  <div className="flex flex-col items-end shrink-0 gap-1">
                    <p className="text-lg font-bold text-accent">+{eq.rating}</p>
                    <button
                      onClick={() => handleDeleteClick(invItem)}
                      className="text-[10px] uppercase tracking-wider transition-colors text-disabled hover:text-status-red"
                    >
                      Remove
                    </button>
                  </div>
                </div>

                {/* EQUIP BUTTON */}
                <div className="px-5 pb-4">
                  <button
                    onClick={() => handleEquipToggle(invItem.id)}
                    className={`w-full py-2 rounded-xl text-sm font-semibold transition-all duration-200 border ${
                      isExpanded
                        ? "bg-accent-dim border-accent text-primary"
                        : "bg-input border-soft text-secondary"
                    }`}
                  >
                    {isExpanded ? "Cancel" : "Equip"}
                  </button>
                </div>

                {/* DELETE CONFIRMATION PANEL */}
                {isConfirmingDelete && (
                  <div className="border-t border-faint px-5 py-4 space-y-3 bg-delete-zone">
                    {pendingDelete.equippedByName ? (
                      <p className="text-xs text-status-red">
                        <span className="font-semibold">
                          {pendingDelete.equippedByName}
                        </span>{" "}
                        currently has this item equipped. Delete and unequip?
                      </p>
                    ) : (
                      <p className="text-xs text-muted">
                        Remove this item from inventory?
                      </p>
                    )}
                    <div className="flex gap-2">
                      <button
                        onClick={() =>
                          handleConfirmDelete(!!pendingDelete.equippedByName)
                        }
                        disabled={deleting}
                        className="flex-1 py-2 rounded-xl text-xs font-semibold transition-all duration-200 disabled:opacity-50 border border-status-red bg-status-red text-status-red"
                      >
                        {deleting ? "Deleting..." : "Confirm"}
                      </button>
                      <button
                        onClick={handleCancelDelete}
                        disabled={deleting}
                        className="flex-1 py-2 rounded-xl text-xs font-semibold transition-all duration-200 border border-soft bg-input text-secondary"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                )}

                {/* EQUIP PANEL */}
                {isExpanded && (
                  <div className="border-t border-faint px-5 py-4 space-y-3 bg-card-header">
                    {compatibleChars.length === 0 ? (
                      <p className="text-xs text-center text-muted">
                        No characters with the required job ({eq.job_name}).
                      </p>
                    ) : (
                      <>
                        <div className="flex flex-col gap-1.5">
                          <label className="text-[10px] uppercase tracking-widest text-muted">
                            Character
                          </label>
                          <select
                            value={state.charId || ""}
                            onChange={(e) =>
                              handleEquipStateChange(invItem.id, "charId", e.target.value)
                            }
                            className="field-select"
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
                          <label className="text-[10px] uppercase tracking-widest text-muted">
                            Slot
                          </label>
                          <select
                            value={state.slot || ""}
                            onChange={(e) =>
                              handleEquipStateChange(invItem.id, "slot", e.target.value)
                            }
                            className="field-select"
                          >
                            <option value="">Select slot...</option>
                            <option value={eq.type}>
                              {SLOT_LABELS[eq.type] ?? eq.type}
                            </option>
                          </select>
                        </div>
                        {errorMsg && (
                          <p className="text-xs text-status-red">{errorMsg}</p>
                        )}
                        <button
                          onClick={() => handleConfirmEquip(invItem.id)}
                          disabled={saving}
                          className="w-full py-2 rounded-xl text-sm font-semibold transition-all duration-200 disabled:opacity-50 border border-accent bg-accent-dim text-primary"
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
