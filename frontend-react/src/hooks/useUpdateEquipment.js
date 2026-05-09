import { useState } from "react";
import { apiFetch } from "../utils/apiFetch";

export function useUpdateEquipment() {
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const updateEquipment = async (inventoryId, characterId, slot) => {
    setSaving(true);
    setError(null);
    try {
      const res = await apiFetch(`/api/v1/inventory/${inventoryId}/equip`, {
        method: "POST",
        body: JSON.stringify({ character_id: characterId, slot }),
      });
      if (!res.ok) {
        const body = await res.json();
        throw new Error(body.error || "Failed to equip item");
      }
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setSaving(false);
    }
  };

  return { updateEquipment, saving, error };
}
