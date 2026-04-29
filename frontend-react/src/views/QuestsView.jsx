import { useState } from "react";
import { useOutletContext } from "react-router-dom";

const LOCATIONS = [
  {
    id: 1,
    name: "Bosque Frondoso Primigenio",
    image: "/localizations/bosque_1.png",
    description: "Extensa masa forestal de árboles centenarios, ríos estrechos y claros cubiertos de niebla.",
    environment: "Senderos cambiantes, visibilidad reducida y zonas donde la vegetación se cierra o se abre dinámicamente.",
    enemies: "Bestias salvajes, bandidos ocultos y criaturas territoriales adaptadas al camuflaje.",
    difficulty: "Easy",
    minRating: 0,
  },
  {
    id: 2,
    name: "La Torre Infinita de Observación",
    image: "/localizations/torre_2.png",
    description: "Colosal estructura vertical que atraviesa las nubes y se pierde en el cielo.",
    environment: "Cada nivel altera reglas físicas: gravedad variable, distorsión temporal y condiciones climáticas internas.",
    enemies: "Guardianes autómatas, exploradores rivales y entidades ligadas a cada nivel.",
    difficulty: "Medium",
    minRating: 50,
  },
  {
    id: 3,
    name: "Cañón de las Tormentas Eternas",
    image: "/localizations/cañon_3.png",
    description: "Profunda grieta rocosa con paredes escarpadas y corrientes de aire violentas.",
    environment: "Tormentas eléctricas constantes, rayos impredecibles y zonas cargadas de energía.",
    enemies: "Criaturas conductoras, depredadores adaptados a la electricidad y recolectores de energía.",
    difficulty: "Medium",
    minRating: 80,
  },
  {
    id: 4,
    name: "Archipiélago de Nubes Errantes",
    image: "/localizations/archipielago_4.png",
    description: "Conjunto de islas flotantes suspendidas sobre un mar de nubes.",
    environment: "Islas en movimiento constante, rutas inestables y corrientes aéreas cambiantes.",
    enemies: "Fauna aérea, colonias aisladas y criaturas migratorias entre islas.",
    difficulty: "Hard",
    minRating: 120,
  },
  {
    id: 5,
    name: "Fosa de Vapor Abisal",
    image: "/localizations/Fosa_5.png",
    description: "Enorme grieta geotérmica que se adentra en la corteza terrestre.",
    environment: "Emisiones de vapor, gases tóxicos y temperaturas extremas con zonas de presión inestable.",
    enemies: "Entidades adaptadas al calor, autómatas antiguos y formas de vida resistentes.",
    difficulty: "Hard",
    minRating: 150,
  },
  {
    id: 6,
    name: "Ciudad Sumergida de Bronce",
    image: "/localizations/sumergida_6.png",
    description: "Ruinas de una antigua metrópolis tecnológica bajo aguas densas y oscuras.",
    environment: "Estructuras colapsadas, cámaras inundadas y mecanismos aún activos.",
    enemies: "Autómatas oxidados, criaturas acuáticas y guardianes de tecnología olvidada.",
    difficulty: "Hard",
    minRating: 180,
  },
  {
    id: 7,
    name: "Isla de los Ingenieros Caídos",
    image: "/localizations/ingenieros_7.png",
    description: "Isla rocosa plagada de fábricas abandonadas y laboratorios en ruinas.",
    environment: "Trampas mecánicas, prototipos defectuosos y sistemas aún operativos de forma errática.",
    enemies: "Constructos fallidos, drones hostiles y supervivientes obsesionados con sus creaciones.",
    difficulty: "Expert",
    minRating: 220,
  },
  {
    id: 8,
    name: "Desierto de Cristal Resonante",
    image: "/localizations/desierto_8.png",
    description: "Vasta extensión de dunas formadas por fragmentos de cristal translúcido.",
    environment: "Vibraciones sonoras constantes, espejismos y tormentas de fragmentos afilados.",
    enemies: "Criaturas sensibles al sonido, depredadores subterráneos y entidades cristalinas.",
    difficulty: "Expert",
    minRating: 260,
  },
  {
    id: 9,
    name: "Cementerio de Aeronaves",
    image: "/localizations/cementerio_9.png",
    description: "Llanura cubierta por restos de zeppelines y naves aéreas estrelladas.",
    environment: "Estructuras inestables, bolsas de gas residual y zonas propensas a colapsos.",
    enemies: "Carroñeros, saqueadores y criaturas que anidan en los restos metálicos.",
    difficulty: "Expert",
    minRating: 300,
  },
  {
    id: 10,
    name: "Volcán de Caldera Eterizada",
    image: "/localizations/volcan_10.png",
    description: "Volcán activo con una amplia caldera rodeada de flujos de lava.",
    environment: "Erupciones periódicas, emisiones de energía etérea y cambios bruscos del terreno.",
    enemies: "Bestias ígneas, entidades mutadas por la energía y cultos que veneran el núcleo.",
    difficulty: "Legendary",
    minRating: 400,
  },
  {
    id: 11,
    name: "Núcleo de Éter",
    image: "/localizations/nucleo_11.png",
    description: "Cavidad colosal en el corazón del planeta donde converge la energía del mundo.",
    environment: "Anomalías físicas, distorsión de la realidad y flujos energéticos impredecibles.",
    enemies: "Entidades primordiales, formas de vida mutadas y guardianes del equilibrio energético.",
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
