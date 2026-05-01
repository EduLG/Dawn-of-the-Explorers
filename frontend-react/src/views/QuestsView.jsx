import { useState } from "react";
import { useOutletContext } from "react-router-dom";

const LOCATIONS = [
  {
    id: 1,
    name: "Primeval Dense Forest",
    image: "/localizations/forest_1.png",
    description: "Vast woodland of ancient trees, narrow rivers and mist-covered clearings.",
    environment: "Shifting paths, reduced visibility and zones where the vegetation opens and closes dynamically.",
    enemies: "Wild beasts, hidden bandits and territorial creatures adapted to camouflage.",
    difficulty: "Easy",
    minRating: 0,
  },
  {
    id: 2,
    name: "The Infinite Observation Tower",
    image: "/localizations/tower_2.png",
    description: "Colossal vertical structure that pierces the clouds and vanishes into the sky.",
    environment: "Each floor alters physical rules: variable gravity, temporal distortion and internal weather conditions.",
    enemies: "Automaton guardians, rival explorers and entities bound to each floor.",
    difficulty: "Medium",
    minRating: 50,
  },
  {
    id: 3,
    name: "Canyon of Eternal Storms",
    image: "/localizations/canyon_3.png",
    description: "Deep rocky rift with sheer walls and violent air currents.",
    environment: "Constant electrical storms, unpredictable lightning and energy-charged zones.",
    enemies: "Conducting creatures, predators adapted to electricity and energy harvesters.",
    difficulty: "Medium",
    minRating: 80,
  },
  {
    id: 4,
    name: "Archipelago of Wandering Clouds",
    image: "/localizations/archipelago_4.png",
    description: "Collection of floating islands suspended above a sea of clouds.",
    environment: "Constantly shifting islands, unstable routes and changing aerial currents.",
    enemies: "Aerial fauna, isolated colonies and migratory creatures between islands.",
    difficulty: "Hard",
    minRating: 120,
  },
  {
    id: 5,
    name: "Abyssal Steam Pit",
    image: "/localizations/pit_5.png",
    description: "Enormous geothermal rift descending into the earth's crust.",
    environment: "Steam vents, toxic gases and extreme temperatures with unstable pressure zones.",
    enemies: "Heat-adapted entities, ancient automatons and resilient life forms.",
    difficulty: "Hard",
    minRating: 150,
  },
  {
    id: 6,
    name: "Sunken Bronze City",
    image: "/localizations/sunken_6.png",
    description: "Ruins of an ancient technological metropolis beneath dense, dark waters.",
    environment: "Collapsed structures, flooded chambers and still-active mechanisms.",
    enemies: "Rusted automatons, aquatic creatures and guardians of forgotten technology.",
    difficulty: "Hard",
    minRating: 180,
  },
  {
    id: 7,
    name: "Isle of the Fallen Engineers",
    image: "/localizations/engineers_7.png",
    description: "Rocky island overrun by abandoned factories and ruined laboratories.",
    environment: "Mechanical traps, defective prototypes and erratically operating systems.",
    enemies: "Failed constructs, hostile drones and survivors obsessed with their creations.",
    difficulty: "Expert",
    minRating: 220,
  },
  {
    id: 8,
    name: "Resonant Crystal Desert",
    image: "/localizations/desert_8.png",
    description: "Vast expanse of dunes formed by fragments of translucent crystal.",
    environment: "Constant sonic vibrations, mirages and storms of razor-sharp fragments.",
    enemies: "Sound-sensitive creatures, subterranean predators and crystalline entities.",
    difficulty: "Expert",
    minRating: 260,
  },
  {
    id: 9,
    name: "Airship Graveyard",
    image: "/localizations/graveyard_9.png",
    description: "Plains covered by the wreckage of crashed zeppelins and airships.",
    environment: "Unstable structures, residual gas pockets and collapse-prone zones.",
    enemies: "Scavengers, looters and creatures nesting in the metallic remains.",
    difficulty: "Expert",
    minRating: 300,
  },
  {
    id: 10,
    name: "Etherized Caldera Volcano",
    image: "/localizations/volcano_10.png",
    description: "Active volcano with a wide caldera surrounded by lava flows.",
    environment: "Periodic eruptions, ethereal energy emissions and sudden terrain shifts.",
    enemies: "Igneous beasts, energy-mutated entities and cults that worship the core.",
    difficulty: "Legendary",
    minRating: 400,
  },
  {
    id: 11,
    name: "Ether Core",
    image: "/localizations/core_11.png",
    description: "Colossal cavity at the planet's core where the world's energy converges.",
    environment: "Physical anomalies, reality distortion and unpredictable energy flows.",
    enemies: "Primordial entities, mutated life forms and guardians of the energy balance.",
    difficulty: "Legendary",
    minRating: 600,
  },
];

const DIFFICULTY_STYLE = {
  Easy:      { label: "Fácil",      color: "text-emerald-400 bg-emerald-400/15 border-emerald-400/30" },
  Medium:    { label: "Medio",      color: "text-yellow-400 bg-yellow-400/15 border-yellow-400/30" },
  Hard:      { label: "Difícil",    color: "text-orange-400 bg-orange-400/15 border-orange-400/30" },
  Expert:    { label: "Experto",    color: "text-red-400 bg-red-400/15 border-red-400/30" },
  Legendary: { label: "Legendario", color: "text-purple-400 bg-purple-400/15 border-purple-400/30" },
};

const QuestsView = () => {
  const { party } = useOutletContext();
  const [activeQuest, setActiveQuest] = useState(null);
  const partyRating = party?.rating ?? 0;

  const handleSend = (locationId) => {
    setActiveQuest((prev) => (prev === locationId ? null : locationId));
  };

  const activeLocation = LOCATIONS.find((l) => l.id === activeQuest);

  return (
    <>
      {/* Header */}
      <div className="bg-white/5 border border-white/10 rounded-2xl px-6 py-4 backdrop-blur-sm flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <p className="text-[10px] uppercase tracking-widest text-[#a89070] mb-0.5">Misiones</p>
          <h2 className="text-xl sm:text-2xl font-bold text-[#f3e5c8]">Exploration Quests</h2>
        </div>
        <div className="flex flex-col items-start sm:items-end gap-0.5">
          <p className="text-[10px] uppercase tracking-widest text-[#a89070]">Party Rating</p>
          <span className="text-2xl font-bold text-[#c9973b]">{partyRating}</span>
        </div>
      </div>

      {/* Active quest banner */}
      {activeLocation && (
        <div className="bg-[#c9973b]/10 border border-[#c9973b]/30 rounded-xl px-5 py-3 flex items-center justify-between gap-4">
          <div>
            <p className="text-[10px] uppercase tracking-widest text-[#c9973b] mb-0.5">Party en misión</p>
            <p className="text-sm font-semibold text-[#f3e5c8]">{activeLocation.name}</p>
          </div>
          <button
            onClick={() => setActiveQuest(null)}
            className="text-xs text-[#a89070] hover:text-[#f3e5c8] transition-colors shrink-0"
          >
            Cancelar misión
          </button>
        </div>
      )}

      {/* Locations grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-5">
        {LOCATIONS.map((location) => {
          const diff = DIFFICULTY_STYLE[location.difficulty];
          const isActive = activeQuest === location.id;
          const partyBusy = activeQuest !== null && !isActive;
          const ratingOk = partyRating >= location.minRating;

          let buttonLabel;
          let buttonClass;
          if (isActive) {
            buttonLabel = "En curso — Cancelar";
            buttonClass = "bg-[#c9973b]/20 border border-[#c9973b]/50 text-[#c9973b] hover:bg-[#c9973b]/30";
          } else if (partyBusy) {
            buttonLabel = "Party en misión";
            buttonClass = "bg-white/5 border border-white/10 text-[#4a3a2a] cursor-not-allowed";
          } else if (!ratingOk) {
            buttonLabel = `Requiere ${location.minRating} rating`;
            buttonClass = "bg-white/5 border border-white/10 text-[#4a3a2a] cursor-not-allowed";
          } else {
            buttonLabel = "Enviar Party";
            buttonClass = "bg-[#c9973b]/15 border border-[#c9973b]/30 text-[#f3e5c8] hover:bg-[#c9973b]/25";
          }

          return (
            <div
              key={location.id}
              className={`flex flex-col rounded-2xl overflow-hidden border backdrop-blur-sm transition-all duration-200 ${
                isActive
                  ? "border-[#c9973b]/50 bg-[#c9973b]/8"
                  : "border-white/10 bg-white/5 hover:border-white/20 hover:bg-white/8"
              }`}
            >
              {/* Cover image */}
              <div className="relative h-44 overflow-hidden shrink-0">
                <img
                  src={location.image}
                  alt={location.name}
                  className="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/10 to-transparent" />

                <span
                  className={`absolute top-2.5 right-2.5 text-[10px] uppercase tracking-wider font-bold px-2 py-0.5 rounded-full border ${diff.color}`}
                >
                  {diff.label}
                </span>

                {location.minRating > 0 && (
                  <span className="absolute bottom-2.5 right-2.5 text-[10px] text-[#a89070] bg-black/60 px-2 py-0.5 rounded-full">
                    Min. {location.minRating}
                  </span>
                )}
              </div>

              {/* Card body */}
              <div className="flex flex-col flex-1 p-4 gap-3">
                <h3 className="text-sm font-bold text-[#f3e5c8] leading-snug">{location.name}</h3>
                <p className="text-xs text-[#a89070] leading-relaxed">{location.description}</p>

                <div className="space-y-2.5 flex-1">
                  <div>
                    <p className="text-[10px] uppercase tracking-widest text-[#6b5a45] mb-1">Entorno</p>
                    <p className="text-[11px] text-[#7a6548] leading-relaxed">{location.environment}</p>
                  </div>
                  <div>
                    <p className="text-[10px] uppercase tracking-widest text-[#6b5a45] mb-1">Amenazas</p>
                    <p className="text-[11px] text-[#7a6548] leading-relaxed">{location.enemies}</p>
                  </div>
                </div>

                <button
                  onClick={() => handleSend(location.id)}
                  disabled={!isActive && (partyBusy || !ratingOk)}
                  className={`mt-2 w-full py-2 rounded-xl text-xs font-semibold uppercase tracking-wider transition-all duration-200 ${buttonClass}`}
                >
                  {buttonLabel}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </>
  );
};

export default QuestsView;
