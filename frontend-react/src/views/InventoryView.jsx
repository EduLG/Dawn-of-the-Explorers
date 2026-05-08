import { useState } from "react";
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

const InventoryView = () => {
  const { party, refetch: refetchParty } = useOutletContext();
  const { data: inventory, loading, refetch: refetchInventory } = useInventory();

  const [jobFilter, setJobFilter] = useState("all");
  const [pendingDelete, setPendingDelete] = useState(null);
  const [deleting, setDeleting] = useState(false);

  const characters = party?.characters || [];

  const jobNames = [
    ...new Set(inventory.map((i) => i.equipment.job_name).filter(Boolean)),
  ];

  const filtered =
    jobFilter === "all"
      ? inventory
      : inventory.filter((i) => i.equipment.job_name === jobFilter);

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
        <h2 className="text-2xl font-bold text-primary">Inventory</h2>
        <span className="text-sm text-muted">
          {inventory.length} item{inventory.length !== 1 ? "s" : ""}
        </span>
      </div>

      {/* JOB FILTER */}
      <Flex align="center" gap="3">
        <Text size="1" color="gray" className="uppercase tracking-widest shrink-0">
          Filter by class
        </Text>
        <Select.Root value={jobFilter} onValueChange={setJobFilter}>
          <Select.Trigger placeholder="No filter" />
          <Select.Content>
            <Select.Item value="all">No filter</Select.Item>
            <Select.Separator />
            {jobNames.map((job) => (
              <Select.Item key={job} value={job}>
                {job}
              </Select.Item>
            ))}
          </Select.Content>
        </Select.Root>
      </Flex>

      {/* TABLE */}
      {loading ? (
        <p className="text-sm text-muted">Loading inventory...</p>
      ) : filtered.length === 0 ? (
        <div className="rounded-2xl border border-soft bg-card p-10 text-center">
          <p className="text-sm text-muted">
            {jobFilter === "all"
              ? "Your inventory is empty. Complete quests to earn loot!"
              : `No items for "${jobFilter}" in inventory.`}
          </p>
        </div>
      ) : (
        <div className="rounded-xl border border-soft bg-card overflow-x-auto">
        <Table.Root variant="ghost">
          <Table.Header>
            <Table.Row>
              <Table.ColumnHeaderCell style={{ width: "3rem", minWidth: "3rem" }} />
              <Table.ColumnHeaderCell>Name</Table.ColumnHeaderCell>
              <Table.ColumnHeaderCell className="hidden sm:table-cell">Class</Table.ColumnHeaderCell>
              <Table.ColumnHeaderCell justify="end">Rating</Table.ColumnHeaderCell>
              <Table.ColumnHeaderCell style={{ width: "4.5rem" }} />
            </Table.Row>
          </Table.Header>

          <Table.Body>
            {filtered.map((invItem) => {
              const eq = invItem.equipment;
              return (
                <Table.Row key={invItem.id} align="center">
                  <Table.Cell style={{ minWidth: "3rem" }}>
                    <SlotIcon type={eq.type} />
                  </Table.Cell>
                  <Table.Cell>
                    <Text weight="bold">{eq.name}</Text>
                  </Table.Cell>
                  <Table.Cell className="hidden sm:table-cell">
                    <Text color="gray">{eq.job_name}</Text>
                  </Table.Cell>
                  <Table.Cell justify="end">
                    <Text weight="bold" color="bronze">+{eq.rating}</Text>
                  </Table.Cell>
                  <Table.Cell justify="end">
                    <button
                      onClick={() => handleDeleteClick(invItem)}
                      className="text-[10px] uppercase tracking-wider text-disabled hover:text-status-red transition-colors"
                    >
                      Remove
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
              <Button variant="soft" color="gray" disabled={deleting}>
                Cancel
              </Button>
            </Dialog.Close>
            <Button
              variant="soft"
              color="red"
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
