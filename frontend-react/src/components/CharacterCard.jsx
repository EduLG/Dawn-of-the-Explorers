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
    <div className="rounded-2xl overflow-hidden border border-white/10 bg-white/5 backdrop-blur-md shadow-xl hover:border-[#c9973b]/40 hover:shadow-[#c9973b]/10 hover:shadow-lg transition-all duration-300">

      {/* CARD HEADER */}
      <div className="bg-gradient-to-r from-[#1e1108]/90 to-[#150d05]/80 border-b border-white/8 px-5 py-4 flex items-center justify-between gap-3">
        <div className="flex flex-col gap-0.5">
          <span className="text-[10px] uppercase tracking-[0.2em] text-[#a89070]">Character</span>
          <span className="text-lg font-bold text-[#f3e5c8] tracking-wide">{charName}</span>
          <span className="text-sm text-[#c9973b] capitalize">{characterClass}</span>
        </div>
        <div className="flex flex-col items-center gap-0.5">
          <span className="text-[10px] uppercase tracking-widest text-[#a89070]">Rating</span>
          <span className="min-w-[2.5rem] text-center rounded-full bg-[#c9973b]/20 border border-[#c9973b]/40 px-3 py-0.5 text-sm font-bold text-[#f3e5c8]">
            {rating}
          </span>
        </div>
      </div>

      {/* CARD BODY */}
      <div className="p-5 flex gap-5 items-start">

        {/* AVATAR */}
        <div className="flex-shrink-0">
          <div className="w-40 h-40 rounded-xl bg-[#c9973b]/10 border border-[#c9973b]/20 flex items-center justify-center overflow-hidden">
            <Avatar src={icon} size="9" fallback={charName?.[0] ?? "?"} />
          </div>
        </div>

        {/* EQUIPMENT LIST */}
        <div className="flex-1 min-w-0">
          <span className="text-[10px] uppercase tracking-widest text-[#a89070] mb-2 block">Equipment</span>
          <ul className="space-y-2">
            {equipmentSlots.map(({ key, label }) => (
              <li key={key} className="flex items-center justify-between gap-2 text-sm">
                <span className="text-[#a89070] w-20 shrink-0">{label}</span>
                <span className="text-[#f3e5c8] truncate text-right">{slots[key] || "—"}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default CharacterCard;
