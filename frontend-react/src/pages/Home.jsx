import React from "react";
import { Button, Avatar } from "@radix-ui/themes";
import CharacterCard from "../components/CharacterCard";
import bgImage from "../assets/resources/bgImage.png";
import headerlogo from "../assets/resources/header-logo.png";

const Home = () => {
  const cards = [1, 2, 3, 4];

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
            <div className="text-[#f3e5c8] font-medium">eduladron</div>
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
                  Dungeons
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
          <section>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {cards.map((c) => (
                <CharacterCard
                  key={c}
                  name={`Adventurer ${c}`}
                  characterClass="Adventurer"
                  equipmentTypes={[
                    "Primary arm",
                    "Secondary arm",
                    "Head",
                    "Chest",
                    "Accessory",
                  ]}
                  equipped={[
                    "Iron Sword",
                    "Iron Shield",
                    "Helmet",
                    "Steel Chest",
                    "Silver Ring",
                  ]}
                />
              ))}
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default Home;
