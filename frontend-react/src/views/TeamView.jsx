import { useOutletContext } from "react-router-dom";
import CharacterCard from "../components/CharacterCard";
import hangarImg from "../assets/resources/Hangar.png";

const getEquippedItemName = (equippedItems, slot) =>
  equippedItems?.find((item) => item.slot === slot)?.equipment?.name || "—";

const TeamView = () => {
  const { party } = useOutletContext();
  const partyCharacters = party?.characters || [];

  return (
    <>
      {/* HANGAR IMAGE */}
      <div className="relative bg-white/5 border border-white/10 rounded-2xl overflow-hidden backdrop-blur-sm">
        <img
          src={hangarImg}
          alt="Party Hangar"
          className="w-full object-cover"
          style={{ filter: "brightness(80%)" }}
        />

        {/* CHARACTER SPRITES */}
        <div className="absolute bottom-[6.25%] left-0 right-0 flex justify-center items-end gap-6 sm:gap-10 px-16 sm:px-24 md:px-32">
          {partyCharacters.map((character) => (
            <img
              key={character.id}
              src={character.current_job?.icon}
              alt={character.name}
              className="h-[82px] sm:h-[102px] md:h-[121px] object-contain drop-shadow-xl"
              style={{ filter: "brightness(80%)" }}
            />
          ))}
        </div>
      </div>

      {/* PARTY HEADER */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 bg-white/5 border border-white/10 rounded-2xl px-6 py-4 backdrop-blur-sm">
        <div>
          <p className="text-[10px] uppercase tracking-widest text-[#a89070] mb-0.5">
            Active Party
          </p>
          <h2 className="text-xl sm:text-2xl font-bold text-[#f3e5c8]">
            {party?.name || "Your Party"}
          </h2>
        </div>
        <div className="flex flex-col items-start sm:items-end gap-0.5">
          <p className="text-[10px] uppercase tracking-widest text-[#a89070]">
            Party Strength
          </p>
          <span className="text-2xl font-bold text-[#c9973b]">
            {party?.rating ?? "—"}
          </span>
        </div>
      </div>

      {/* CHARACTERS GRID */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-5">
        {partyCharacters.map((character) => {
          const equippedItems = character.equipped_items || [];
          return (
            <CharacterCard
              key={character.id}
              charName={character.name}
              characterClass={character.current_job?.name}
              rating={character.rating || 0}
              icon={character.current_job?.icon}
              primaryArm={getEquippedItemName(equippedItems, "primary_hand")}
              secondaryArm={getEquippedItemName(
                equippedItems,
                "secondary_hand",
              )}
              head={getEquippedItemName(equippedItems, "head")}
              chest={getEquippedItemName(equippedItems, "chest")}
              accesory={getEquippedItemName(equippedItems, "accesory")}
            />
          );
        })}
      </div>
    </>
  );
};

export default TeamView;
