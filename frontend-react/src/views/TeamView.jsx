import { useOutletContext } from "react-router-dom";
import CharacterCard from "../components/CharacterCard";

const getEquippedItemName = (equippedItems, slot) =>
  equippedItems?.find((item) => item.slot === slot)?.equipment?.name || "—";

const TeamView = () => {
  const { party } = useOutletContext();
  const partyCharacters = party?.characters || [];

  return (
    <>
      {/* PARTY HEADER */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 bg-white/5 border border-white/10 rounded-2xl px-6 py-4 backdrop-blur-sm">
        <div>
          <p className="text-[10px] uppercase tracking-widest text-[#a89070] mb-0.5">Active Party</p>
          <h2 className="text-xl sm:text-2xl font-bold text-[#f3e5c8]">
            {party?.name || "Your Party"}
          </h2>
        </div>
        <div className="flex flex-col items-start sm:items-end gap-0.5">
          <p className="text-[10px] uppercase tracking-widest text-[#a89070]">Party Strength</p>
          <span className="text-2xl font-bold text-[#c9973b]">{party?.rating ?? "—"}</span>
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
              secondaryArm={getEquippedItemName(equippedItems, "secondary_hand")}
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
