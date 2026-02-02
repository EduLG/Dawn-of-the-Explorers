import React from "react";
import { Button, Avatar } from "@radix-ui/themes";
import adventurer from "../assets/resources/character-templates/adventurer.png";
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
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {cards.map((card) => (
                <div
                  key={card}
                  className="relative rounded-xl overflow-hidden border border-white/6 bg-gradient-to-b from-white/6 to-white/3 shadow-lg hover:scale-[1.02] transition-transform duration-200"
                >
                  <div className="p-4 flex flex-col items-center gap-3">
                    <div className="w-36 h-36 rounded-full bg-[#e6d3a3] p-2 flex items-center justify-center">
                      <Avatar
                        src={adventurer}
                        alt={`Adventurer ${card}`}
                        size="8"
                      />
                    </div>
                    <div className="text-center">
                      <div className="text-base font-semibold text-[#3b2a1a]">
                        Adventurer
                      </div>
                    </div>

                    <div className="w-full mt-2">
                      <div className="flex items-start justify-between w-full text-sm text-[#6b4f2a]">
                        <div className="flex-1">
                          <div className="text-xs text-[#e6d3a3]">
                            Equipment
                          </div>
                          <ul className="mt-1 space-y-1">
                            <li className="text-[#3b2a1a]">Primary arm</li>
                            <li className="text-[#3b2a1a]">Secondary arm</li>
                            <li className="text-[#3b2a1a]">Head</li>
                            <li className="text-[#3b2a1a]">Chest</li>
                            <li className="text-[#3b2a1a]">Accessory</li>
                          </ul>
                        </div>

                        <div className="flex-1 text-right">
                          <div className="text-xs text-[#e6d3a3]">Equipped</div>
                          <ul className="mt-1 space-y-1">
                            <li className="text-[#3b2a1a]">Iron Sword</li>
                            <li className="text-[#3b2a1a]">Iron Shield</li>
                            <li className="text-[#3b2a1a]">Helmet</li>
                            <li className="text-[#3b2a1a]">Steel Chest</li>
                            <li className="text-[#3b2a1a]">Silver Ring</li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default Home;
