import { useState } from "react";
import { apiFetch } from "../utils/apiFetch";

export function useUpdateEquipment() {
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const updateEquipment = async (characterId, slot, equipmentId) => {
    setSaving(true);
    setError(null);
    try {
      const res = await apiFetch(`/api/v1/equipment/character/${characterId}`, {
        method: "PUT",
        body: JSON.stringify({ slot, equipment_id: equipmentId }),
      });
      if (!res.ok) throw new Error("Failed to update equipment");
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setSaving(false);
    }
  };

  return { updateEquipment, saving, error };
}
