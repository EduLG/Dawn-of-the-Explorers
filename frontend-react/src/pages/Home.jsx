import React from "react";
import { Button } from "@radix-ui/themes";
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
            <div className="hidden sm:flex items-center bg-white/6 rounded-md px-3 py-1 gap-2">
              <input
                className="bg-transparent outline-none placeholder:text-[#e6d3a3] text-[#f3e5c8] w-56"
                placeholder="Search characters, equipment..."
              />
              <Button variant="ghost" size="small">
                Search
              </Button>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Button variant="ghost" className="px-3 py-2 hidden sm:inline-flex">
              New
            </Button>
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#b08d57] to-[#6b4f2a] flex items-center justify-center text-white font-semibold">
                E
              </div>
              <div className="text-sm hidden sm:block">
                <div className="text-[#f3e5c8] font-medium">eduladron</div>
                <div className="text-[#e6d3a3] text-[12px]">View profile</div>
              </div>
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
                  Equipment
                </Button>
              </li>
              <li>
                <Button variant="ghost" className="w-full justify-start">
                  Dungeons
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
                      <img
                        src={adventurer}
                        alt="Adventurer"
                        className="w-full h-full object-contain"
                      />
                    </div>
                    <div className="text-center">
                      <div className="text-base font-semibold text-[#3b2a1a]">
                        Adventurer #{card}
                      </div>
                    </div>
                    <div className="w-full flex gap-2 mt-2"></div>
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
