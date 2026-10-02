import { useState, useMemo } from "react";
import { useOutletContext } from "react-router-dom";
import { Table, Select, Dialog, Button, Text, Flex } from "@radix-ui/themes";
import { useInventory } from "../hooks/useInventory";
import { apiFetch } from "../utils/apiFetch";
import headIcon from "../assets/resources/eq_icons/head.svg";
import chestIcon from "../assets/resources/eq_icons/chest.svg";
import handIcon from "../assets/resources/eq_icons/hand.svg";
import accesoryIcon from "../assets/resources/eq_icons/accesory.svg";

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
      className="w-8 h-8 shrink-0"
      style={icon.flip ? { transform: "scaleX(-1)" } : undefined}
    />
  );
};

const SLOT_LABELS = {
  head: "Head",
  chest: "Chest",
  primary_hand: "Primary hand",
  secondary_hand: "Secondary hand",
  accesory: "Accessory",
};

const SortIndicator = ({ active, dir }) => (
  <span className={`ml-1 text-[12px] ${active ? "text-primary" : "text-muted opacity-40"}`}>
    {active && dir === "desc" ? "▼" : "▲"}
  </span>
);

const SORTABLE_COLS = [
  { key: "name",           label: "Name",   justify: undefined,  className: "" },
  { key: "equipment_type", label: "Type",   justify: undefined,  className: "hidden sm:table-cell" },
  { key: "rating",         label: "Rating", justify: undefined,  className: "" },
];

const InventoryView = () => {
  const { party, refetch: refetchParty } = useOutletContext();
  const { data: inventory, loading, refetch: refetchInventory } = useInventory();

  const [armorFilter, setArmorFilter] = useState("all");
  const [slotFilter, setSlotFilter] = useState("all");
  const [sortConfig, setSortConfig] = useState({ key: "rating", dir: "asc" });
  const [pendingDelete, setPendingDelete] = useState(null);
  const [deleting, setDeleting] = useState(false);

  const characters = party?.characters || [];

  const armorTypes = useMemo(
    () => [...new Set(inventory.map((i) => i.equipment.equipment_type).filter(Boolean))],
    [inventory]
  );

  // Slots present among the items of the selected type, in equipment order
  const slotsForType = useMemo(() => {
    const present = new Set(
      inventory
        .filter((i) => i.equipment.equipment_type === armorFilter)
        .map((i) => i.equipment.slot),
    );
    return Object.keys(SLOT_LABELS).filter((slot) => present.has(slot));
  }, [inventory, armorFilter]);

  const handleArmorFilterChange = (value) => {
    setArmorFilter(value);
    setSlotFilter("all");
  };

  const handleSort = (key) => {
    setSortConfig((prev) =>
      prev.key === key
        ? { key, dir: prev.dir === "asc" ? "desc" : "asc" }
        : { key, dir: "asc" }
    );
  };

  const sorted = useMemo(() => {
    const base = inventory.filter(
      (i) =>
        (armorFilter === "all" || i.equipment.equipment_type === armorFilter) &&
        (slotFilter === "all" || i.equipment.slot === slotFilter),
    );

    return [...base].sort((a, b) => {
      const eq1 = a.equipment;
      const eq2 = b.equipment;
      let cmp = 0;
      if (sortConfig.key === "rating") {
        cmp = eq1.rating - eq2.rating;
      } else {
        cmp = (eq1[sortConfig.key] ?? "").localeCompare(eq2[sortConfig.key] ?? "");
      }
      return sortConfig.dir === "asc" ? cmp : -cmp;
    });
  }, [inventory, armorFilter, slotFilter, sortConfig]);

  const handleDeleteClick = (invItem) => {
    const equippedByChar = characters.find((c) =>
      c.equipped_items?.some((ei) => ei.equipment?.id === invItem.equipment.id),
    );
    setPendingDelete({
      invId: invItem.id,
      name: invItem.equipment.name,
      equippedByName: equippedByChar ? equippedByChar.name : null,
    });
  };

  const handleConfirmDelete = async () => {
    if (!pendingDelete) return;
    setDeleting(true);
    try {
      const res = await apiFetch(`/api/v1/inventory/${pendingDelete.invId}`, {
        method: "DELETE",
        body: JSON.stringify({ force: !!pendingDelete.equippedByName }),
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
        <h2 className="text-base font-semibold text-primary">Inventory</h2>
        <span className="text-sm text-muted">
          {inventory.length} item{inventory.length !== 1 ? "s" : ""}
        </span>
      </div>

      {/* FILTER */}
      <Flex align="center" gap="3" wrap="wrap">
        <Select.Root value={armorFilter} onValueChange={handleArmorFilterChange} size="3">
          <Select.Trigger placeholder="No filter" aria-label="Filter by type" style={{ minHeight: 44 }} />
          <Select.Content>
            <Select.Item value="all" style={{ minHeight: 44 }}>No filter</Select.Item>
            <Select.Separator />
            {armorTypes.map((type) => (
              <Select.Item key={type} value={type} style={{ minHeight: 44 }}>
                {type}
              </Select.Item>
            ))}
          </Select.Content>
        </Select.Root>

        {/* Second filter, shown once a type is chosen */}
        {armorFilter !== "all" && (
          <Select.Root value={slotFilter} onValueChange={setSlotFilter} size="3">
            <Select.Trigger placeholder="All slots" aria-label="Filter by slot" style={{ minHeight: 44 }} />
            <Select.Content>
              <Select.Item value="all" style={{ minHeight: 44 }}>All slots</Select.Item>
              <Select.Separator />
              {slotsForType.map((slot) => (
                <Select.Item key={slot} value={slot} style={{ minHeight: 44 }}>
                  {SLOT_LABELS[slot]}
                </Select.Item>
              ))}
            </Select.Content>
          </Select.Root>
        )}
      </Flex>

      {/* TABLE */}
      {loading ? (
        <p className="text-sm text-muted">Loading inventory...</p>
      ) : sorted.length === 0 ? (
        <div className="rounded-2xl border border-soft bg-card p-10 text-center">
          <p className="text-sm text-muted">
            {armorFilter === "all"
              ? "Your inventory is empty. Complete quests to earn loot!"
              : `No items for "${armorFilter}"${slotFilter !== "all" ? ` / "${SLOT_LABELS[slotFilter]}"` : ""} in inventory.`}
          </p>
        </div>
      ) : (
        <div className="rounded-xl border border-soft bg-card overflow-x-auto">
          <Table.Root variant="ghost">
            <Table.Header>
              <Table.Row>
                <Table.ColumnHeaderCell style={{ width: "3rem", minWidth: "3rem" }} />
                {SORTABLE_COLS.map(({ key, label, justify, className }) => (
                  <Table.ColumnHeaderCell key={key} justify={justify} className={className}>
                    <button
                      onClick={() => handleSort(key)}
                      className="flex items-center gap-0.5 min-h-11 cursor-pointer select-none hover:text-primary transition-colors"
                    >
                      {label}
                      <SortIndicator active={sortConfig.key === key} dir={sortConfig.dir} />
                    </button>
                  </Table.ColumnHeaderCell>
                ))}
                <Table.ColumnHeaderCell />
              </Table.Row>
            </Table.Header>

            <Table.Body>
              {sorted.map((invItem) => {
                const eq = invItem.equipment;
                return (
                  <Table.Row key={invItem.id} align="center">
                    <Table.Cell style={{ minWidth: "3rem" }}>
                      <SlotIcon type={eq.slot} />
                    </Table.Cell>
                    <Table.Cell>
                      <Text weight="bold">{eq.name}</Text>
                    </Table.Cell>
                    <Table.Cell className="hidden sm:table-cell">
                      <Text color="gray" className="capitalize">{eq.equipment_type}</Text>
                    </Table.Cell>
                    <Table.Cell>
                      <Text weight="bold" color="bronze">+{eq.rating}</Text>
                    </Table.Cell>
                    <Table.Cell justify="end">
                      {/* Icon only on mobile to leave room for the item name */}
                      <button
                        onClick={() => handleDeleteClick(invItem)}
                        aria-label={`Discard ${eq.name}`}
                        className="min-w-11 min-h-11 inline-flex items-center justify-center gap-1.5 sm:px-2 text-[12px] uppercase tracking-wider text-secondary hover:text-status-red transition-colors"
                      >
                        <i className="pi pi-trash" aria-hidden="true" />
                        <span className="hidden sm:inline">Discard</span>
                      </button>
                    </Table.Cell>
                  </Table.Row>
                );
              })}
            </Table.Body>
          </Table.Root>
        </div>
      )}

      {/* DELETE CONFIRMATION DIALOG */}
      <Dialog.Root
        open={!!pendingDelete}
        onOpenChange={(open) => !open && !deleting && setPendingDelete(null)}
      >
        <Dialog.Content maxWidth="360px">
          <Dialog.Title>Remove item</Dialog.Title>
          <Dialog.Description size="2" color={pendingDelete?.equippedByName ? "red" : "gray"}>
            {pendingDelete?.equippedByName ? (
              <>
                <Text weight="bold">{pendingDelete.equippedByName}</Text> currently has{" "}
                <Text weight="bold">{pendingDelete.name}</Text> equipped. Removing it will
                also unequip it.
              </>
            ) : (
              <>
                Remove <Text weight="bold">{pendingDelete?.name}</Text> from your inventory?
              </>
            )}
          </Dialog.Description>

          <Flex gap="3" justify="end" mt="4">
            <Dialog.Close>
              <Button variant="soft" color="gray" size="3" style={{ minHeight: 44 }} disabled={deleting}>
                Cancel
              </Button>
            </Dialog.Close>
            <Button
              variant="soft"
              color="red"
              size="3"
              style={{ minHeight: 44 }}
              disabled={deleting}
              onClick={handleConfirmDelete}
            >
              {deleting ? "Removing..." : "Confirm"}
            </Button>
          </Flex>
        </Dialog.Content>
      </Dialog.Root>
    </div>
  );
};

export default InventoryView;
