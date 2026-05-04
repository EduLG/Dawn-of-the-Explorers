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
          className="w-full object-cover brightness-80"
        />

        {/* PARTY HEADER OVERLAY */}
        <div className="absolute top-0 left-0 right-0 flex items-start px-6 py-4 bg-gradient-to-b from-black/70 to-transparent">
          <div className="flex flex-col gap-1 bg-black/20 border border-white/8 rounded-xl px-4 py-3 backdrop-blur-sm">
            <h2 className="text-xl sm:text-2xl font-bold text-primary">
              {party?.name || "Your Party"}
            </h2>
            <div className="flex items-center gap-2 mt-0.5">
              <p className="text-[10px] uppercase tracking-widest text-muted">
                Party Strength
              </p>
              <span className="text-sm font-bold text-accent">
                {party?.rating ?? "—"}
              </span>
            </div>
          </div>
        </div>

        {/* CHARACTER SPRITES */}
        <div className="absolute bottom-[6.25%] left-0 right-0 flex justify-center items-end gap-6 sm:gap-10 px-16 sm:px-24 md:px-32">
          {partyCharacters.map((character) => (
            <img
              key={character.id}
              src={character.current_job?.icon}
              alt={character.name}
              className="h-[82px] sm:h-[102px] md:h-[121px] object-contain drop-shadow-xl brightness-80"
            />
          ))}
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
