// src/components/CharacterCard.jsx
import { Avatar } from "@radix-ui/themes";

const equipmentSlots = [
  { key: "head", label: "Head" },
  { key: "chest", label: "Chest" },
  { key: "primaryArm", label: "Primary" },
  { key: "secondaryArm", label: "Secondary" },
  { key: "accesory", label: "Accessory" },
];

const CharacterCard = ({
  charName,
  characterClass,
  rating,
  icon,
  primaryArm,
  secondaryArm,
  head,
  chest,
  accesory,
}) => {
  const slots = { head, chest, primaryArm, secondaryArm, accesory };

  return (
    <div className="rounded-2xl overflow-hidden shadow-card border border-soft bg-card transition-all duration-300 hover:border-[--accent-border]">
      {/* CARD HEADER */}
      <div className="border-b border-faint px-5 py-4 flex items-center justify-between gap-3 bg-card-header">
        <div className="flex flex-col gap-0.5">
          <span className="text-xs uppercase tracking-[0.2em] text-muted">
            Character
          </span>
          <span className="text-lg font-bold tracking-wide text-primary">
            {charName}
          </span>
          <span className="text-sm capitalize text-accent-sub">
            {characterClass}
          </span>
        </div>
        <div className="flex flex-col items-center gap-0.5">
          <span className="text-xs uppercase tracking-widest text-muted">
            Rating
          </span>
          <span className="min-w-[2.5rem] text-center rounded-full border border-accent bg-accent-dim px-3 py-0.5 text-sm font-bold text-primary">
            {rating}
          </span>
        </div>
      </div>

      {/* CARD BODY */}
      <div className="p-5 flex gap-4 items-stretch">
        {/* AVATAR */}
        <div className="flex-shrink-0">
          <div className="w-40 h-full min-h-40 rounded-xl border border-accent bg-accent-dim flex items-center justify-center overflow-hidden">
            <Avatar src={icon} size="9" fallback={charName?.[0] ?? "?"} />
          </div>
        </div>

        {/* EQUIPMENT PANEL */}
        <div className="flex-1 min-w-0 rounded-xl border border-faint bg-input overflow-hidden flex flex-col">
          <div className="px-4 py-2 border-b border-faint bg-card-header">
            <span className="text-xs uppercase tracking-widest font-semibold text-accent-sub">
              Equipment
            </span>
          </div>
          <ul className="flex-1 px-4 py-3 space-y-2">
            {equipmentSlots.map(({ key, label }) => (
              <li
                key={key}
                className="flex items-center justify-between gap-2 text-sm border-b border-faint last:border-b-0 pb-1 last:pb-0"
              >
                <span className="w-20 shrink-0 text-secondary">{label}</span>
                <span className="truncate text-right text-primary">
                  {slots[key] || "—"}
                </span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default CharacterCard;
