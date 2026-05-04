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
    <div
      className="rounded-2xl overflow-hidden shadow-[var(--shadow-card)] border transition-all duration-300 hover:border-[--accent-border]"
      style={{ background: "var(--bg-card)", borderColor: "var(--border-soft)" }}
    >
      {/* CARD HEADER */}
      <div
        className="border-b px-5 py-4 flex items-center justify-between gap-3"
        style={{ background: "var(--bg-card-header)", borderColor: "var(--border-faint)" }}
      >
        <div className="flex flex-col gap-0.5">
          <span
            className="text-[10px] uppercase tracking-[0.2em]"
            style={{ color: "var(--text-muted)" }}
          >
            Character
          </span>
          <span
            className="text-lg font-bold tracking-wide"
            style={{ color: "var(--text-primary)" }}
          >
            {charName}
          </span>
          <span
            className="text-sm capitalize"
            style={{ color: "var(--accent-text)" }}
          >
            {characterClass}
          </span>
        </div>
        <div className="flex flex-col items-center gap-0.5">
          <span
            className="text-[10px] uppercase tracking-widest"
            style={{ color: "var(--text-muted)" }}
          >
            Rating
          </span>
          <span
            className="min-w-[2.5rem] text-center rounded-full border px-3 py-0.5 text-sm font-bold"
            style={{
              background: "var(--accent-dim)",
              borderColor: "var(--accent-border)",
              color: "var(--text-primary)",
            }}
          >
            {rating}
          </span>
        </div>
      </div>

      {/* CARD BODY */}
      <div className="p-5 flex gap-4 items-stretch">
        {/* AVATAR */}
        <div className="flex-shrink-0">
          <div
            className="w-40 h-full min-h-40 rounded-xl border flex items-center justify-center overflow-hidden"
            style={{ background: "var(--accent-dim)", borderColor: "var(--accent-border)" }}
          >
            <Avatar src={icon} size="9" fallback={charName?.[0] ?? "?"} />
          </div>
        </div>

        {/* EQUIPMENT PANEL */}
        <div
          className="flex-1 min-w-0 rounded-xl border overflow-hidden flex flex-col"
          style={{ borderColor: "var(--border-faint)", background: "var(--bg-input)" }}
        >
          <div
            className="px-4 py-2 border-b"
            style={{ borderColor: "var(--border-faint)", background: "var(--bg-card-header)" }}
          >
            <span
              className="text-xs uppercase tracking-widest font-semibold"
              style={{ color: "var(--accent-text)" }}
            >
              Equipment
            </span>
          </div>
          <ul className="flex-1 px-4 py-3 space-y-2">
            {equipmentSlots.map(({ key, label }) => (
              <li
                key={key}
                className="flex items-center justify-between gap-2 text-sm border-b last:border-b-0 pb-1 last:pb-0"
                style={{ borderColor: "var(--border-faint)" }}
              >
                <span className="w-20 shrink-0" style={{ color: "var(--text-secondary)" }}>
                  {label}
                </span>
                <span className="truncate text-right" style={{ color: "var(--text-primary)" }}>
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
