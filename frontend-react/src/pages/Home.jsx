import React from "react";
import { Button, Avatar } from "@radix-ui/themes";
import useUser from "../hooks/useUser";
import CharacterCard from "../components/CharacterCard";
import bgImage from "../assets/resources/bgImage.png";
import headerlogo from "../assets/resources/header-logo.png";

const Home = () => {
  const { data: user } = useUser();
  const party = user?.party;
  const partyCharacters = party?.characters || [];

  const getEquippedItemName = (equippedItems, slot) => {
    return (
      equippedItems?.find((item) => item.slot === slot)?.equipment?.name || "-"
    );
  };

  const getCharacterRating = (equippedItems) => {
    return (
      equippedItems?.reduce(
        (total, item) => total + (item?.equipment?.rating || 0),
        0,
      ) || 0
    );
  };

  return (
    <div
      className="min-h-screen w-full antialiased text-[#2b1e14]"
      style={{
        backgroundImage: `linear-gradient(rgba(15,10,8,0.6), rgba(15,10,8,0.6)), url(${bgImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <header className="backdrop-blur-sm bg-white/5 border-b border-white/6 sticky top-0 z-20">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <img src={headerlogo} alt="Logo" className="h-15" />
          </div>

          <div className="flex items-center gap-3">
            <Avatar fallback="E" />
            <div className="text-[#f3e5c8] font-medium">
              {user?.username || "Guest"}
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-[220px_1fr] gap-6">
        <aside className="hidden lg:block">
          <nav className="bg-white/6 p-4 rounded-xl border border-white/6 backdrop-blur-sm">
            <ul className="flex flex-col gap-3">
              <li>
                <Button variant="ghost" className="w-full justify-start">
                  Team
                </Button>
              </li>
              <li>
                <Button variant="ghost" className="w-full justify-start">
                  Manage equipment
                </Button>
              </li>
              <li>
                <Button variant="ghost" className="w-full justify-start">
                  Exploration quests
                </Button>
              </li>
              <li>
                <Button variant="ghost" className="w-full justify-start">
                  Market
                </Button>
              </li>
            </ul>
          </nav>
        </aside>

        <main className="space-y-6">
          <div className="flex items-center justify-between bg-white/5 border border-white/6 rounded-xl p-4 backdrop-blur-sm">
            <div>
              <h2 className="text-2xl font-bold text-[#f3e5c8]">
                {party?.name || "Your Party"}
              </h2>
            </div>
            <div className="flex items-center gap-2">
              <p className="text-sm text-[#e6d3a3]">
                Party strength value:
                <span className="font-medium text-2xl"> {party?.rating}</span>
              </p>
            </div>
          </div>

          <section>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {partyCharacters.map((character) => {
                const equippedItems = character.equipped_items || [];
                return (
                  <div key={character.id} className="relative">
                    <CharacterCard
                      charName={character.name}
                      characterClass={character.current_job?.name}
                      rating={getCharacterRating(equippedItems)}
                      icon={character.current_job?.icon}
                      primaryArm={getEquippedItemName(
                        equippedItems,
                        "primary_hand",
                      )}
                      secondaryArm={getEquippedItemName(
                        equippedItems,
                        "secondary_hand",
                      )}
                      head={getEquippedItemName(equippedItems, "head")}
                      chest={getEquippedItemName(equippedItems, "chest")}
                      accesory={getEquippedItemName(equippedItems, "accesory")}
                    />
                  </div>
                );
              })}
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default Home;
