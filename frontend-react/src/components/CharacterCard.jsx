import { Avatar, Card } from "@radix-ui/themes";
import adventurer from "../assets/resources/character-templates/adventurer.png";

const CharacterCard = ({
  name = "Edu",
  characterClass = "rer",
  equipmentTypes = [
    "Primary arm",
    "Secondary arm",
    "Head",
    "Chest",
    "Accessory",
  ],
  equipped = [
    "Iron Sword",
    "Iron Shield",
    "Helmet",
    "Steel Chest",
    "Silver Ring",
  ],
  avatarSrc = adventurer,
}) => {
  return (
    <Card className="relative rounded-xl overflow-hidden border border-white/6 bg-gradient-to-b from-white/6 to-white/3 shadow-lg hover:scale-[1.02] transition-transform duration-200">
      <div className="p-2 h-full flex flex-col md:flex-row items-center md:items-stretch gap-6">
        <div className="flex-shrink-0 flex items-center justify-center md:pl-2">
          <div className="rounded-full bg-[#e6d3a3] flex items-center justify-center">
            <Avatar src={avatarSrc} alt={name} size="9" />
          </div>
        </div>

        <div className="flex-1 flex flex-col justify-center w-full">
          <div className="text-lg font-bold text-[#3b2a1a] mb-1">{name}</div>
          <div className="text-sm text-[#6b4f2a] mb-3">
            Class: {characterClass}
          </div>

          <div className="w-full mt-0 text-sm text-[#6b4f2a]">
            <div className="flex items-start justify-between w-full">
              <div className="flex-1">
                <div className="text-xs text-[#e6d3a3]">Type</div>
                <ul className="mt-1 space-y-1 text-[#3b2a1a]">
                  {equipmentTypes.map((t, i) => (
                    <li key={i}>{t}</li>
                  ))}
                </ul>
              </div>

              <div className="flex-1 text-right">
                <div className="text-xs text-[#e6d3a3]">Equipped</div>
                <ul className="mt-1 space-y-1 text-[#3b2a1a]">
                  {equipped.map((e, i) => (
                    <li key={i}>{e}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default CharacterCard;
