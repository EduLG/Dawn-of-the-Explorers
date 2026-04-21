import { NavLink, Outlet } from "react-router-dom";
import { Avatar } from "@radix-ui/themes";
import useUser from "../hooks/useUser";
import bgImage from "../assets/resources/bgImage.png";
import headerlogo from "../assets/resources/header-logo.png";

const navItems = [
  { label: "Team", mobileLabel: "Team", to: "/home/team" },
  { label: "Manage equipment", mobileLabel: "Equip", to: "/home/equipment" },
  { label: "Inventory", mobileLabel: "Inventory", to: "/home/inventory" },
  { label: "Exploration quests", mobileLabel: "Quests", to: "/home/quests" },
  { label: "Market", mobileLabel: "Market", to: "/home/market" },
];

const sidebarLinkClass = ({ isActive }) =>
  `flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-sm transition-all duration-200 ${
    isActive
      ? "bg-[#c9973b]/15 border border-[#c9973b]/30 text-[#f3e5c8] font-semibold"
      : "text-[#a89070] hover:bg-white/8 hover:text-[#f3e5c8] border border-transparent"
  }`;

const mobileLinkClass = ({ isActive }) =>
  `flex-1 flex flex-col items-center justify-center py-1.5 text-[10px] uppercase tracking-wider transition-colors ${
    isActive ? "text-[#c9973b] font-bold" : "text-[#6b5a45]"
  }`;

const Home = () => {
  const { data: user, refetch } = useUser();
  const party = user?.party;

  return (
    <div
      className="min-h-screen w-full antialiased"
      style={{
        backgroundImage: `linear-gradient(rgba(10,6,2,0.72), rgba(10,6,2,0.72)), url(${bgImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      {/* HEADER */}
      <header className="sticky top-0 z-20 backdrop-blur-md bg-black/30 border-b border-white/8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
          <img src={headerlogo} alt="Logo" className="h-10 sm:h-12" />
          <div className="flex items-center gap-3">
            <div className="text-right hidden sm:block">
              <p className="text-[10px] uppercase tracking-widest text-[#a89070]">Explorer</p>
              <p className="text-sm font-semibold text-[#f3e5c8]">{user?.username || "Guest"}</p>
            </div>
            <Avatar
              fallback={user?.username?.[0]?.toUpperCase() ?? "?"}
              className="border-2 border-[#c9973b]/30"
            />
          </div>
        </div>
      </header>

      {/* LAYOUT */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 sm:py-8 grid grid-cols-1 lg:grid-cols-[220px_1fr] gap-6">

        {/* SIDEBAR DESKTOP */}
        <aside className="hidden lg:block">
          <nav className="bg-white/4 backdrop-blur-md border border-white/8 rounded-2xl p-3 sticky top-24">
            <p className="text-[10px] uppercase tracking-widest text-[#6b5a45] px-3 mb-2">Navigation</p>
            <ul className="flex flex-col gap-1">
              {navItems.map((item) => (
                <li key={item.to}>
                  <NavLink to={item.to} className={sidebarLinkClass}>
                    {item.label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </nav>
        </aside>

        {/* MAIN CONTENT */}
        <main className="space-y-5 pb-24 lg:pb-0">
          <Outlet context={{ user, party, refetch }} />
        </main>
      </div>

      {/* MOBILE BOTTOM NAV */}
      <nav className="lg:hidden fixed bottom-0 left-0 right-0 bg-[#0d0703]/90 backdrop-blur-xl border-t border-white/8 flex z-30">
        {navItems.map((item) => (
          <NavLink key={item.to} to={item.to} className={mobileLinkClass}>
            {item.mobileLabel}
          </NavLink>
        ))}
      </nav>
    </div>
  );
};

export default Home;
