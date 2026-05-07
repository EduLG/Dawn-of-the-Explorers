import { useState } from "react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { Avatar, DropdownMenu } from "@radix-ui/themes";
import useUser from "../hooks/useUser";
import OnboardingModal from "../components/OnboardingModal";
import bgImage from "../assets/resources/bgImage.png";
import headerlogo from "../assets/resources/header-logo.png";

const navItems = [
  { label: "Team", mobileLabel: "Team", to: "/home/team" },
  { label: "Characters", mobileLabel: "Chars", to: "/home/equipment" },
  { label: "Inventory", mobileLabel: "Inventory", to: "/home/inventory" },
  { label: "Exploration quests", mobileLabel: "Quests", to: "/home/quests" },
  { label: "Market", mobileLabel: "Market", to: "/home/market" },
];

const sidebarLinkClass = ({ isActive }) =>
  `flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-sm transition-all duration-200 ${
    isActive
      ? "bg-accent-dim border border-accent text-primary font-semibold"
      : "text-muted hover:bg-white/8 hover:text-primary border border-transparent"
  }`;

const Home = () => {
  const { data: user, refetch } = useUser();
  const party = user?.party;
  const needsOnboarding = user && party && party.characters.length === 0;

  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
    navigate("/login");
  };

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
      <header className="sticky top-0 z-20 backdrop-blur-md bg-header border-b border-faint">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            {/* Hamburger */}
            <button
              className="lg:hidden flex flex-col justify-center gap-1.5 w-8 h-8 cursor-pointer"
              onClick={() => setMenuOpen((prev) => !prev)}
              aria-label="Toggle navigation"
            >
              <span
                className={`block h-0.5 bg-primary transition-all duration-200 ${menuOpen ? "rotate-45 translate-y-2" : ""}`}
              />
              <span
                className={`block h-0.5 bg-primary transition-all duration-200 ${menuOpen ? "opacity-0" : ""}`}
              />
              <span
                className={`block h-0.5 bg-primary transition-all duration-200 ${menuOpen ? "-rotate-45 -translate-y-2" : ""}`}
              />
            </button>
            <img src={headerlogo} alt="Logo" className="h-10 sm:h-12" />
          </div>

          <div className="flex items-center gap-3">
            <div className="text-right hidden sm:block">
              <p className="text-[10px] uppercase tracking-widest text-muted">
                Explorer
              </p>
              <p className="text-sm font-semibold text-primary">
                {user?.username || "Guest"}
              </p>
            </div>

            <DropdownMenu.Root>
              <DropdownMenu.Trigger>
                <button className="cursor-pointer">
                  <Avatar
                    fallback={user?.username?.[0]?.toUpperCase() ?? "?"}
                    className="border-2 border-accent"
                  />
                </button>
              </DropdownMenu.Trigger>
              <DropdownMenu.Content
                align="end"
                className="min-w-[180px] rounded-xl border border-soft shadow-modal bg-card p-2"
              >
                <DropdownMenu.Item
                  onSelect={handleLogout}
                  className="px-4 py-3 rounded-lg text-base font-semibold cursor-pointer text-status-red hover:bg-delete-zone outline-none"
                >
                  Logout
                </DropdownMenu.Item>
              </DropdownMenu.Content>
            </DropdownMenu.Root>
          </div>
        </div>

        {/* Menu desplegable movil */}
        {menuOpen && (
          <nav className="lg:hidden border-t border-faint bg-header px-4 py-3">
            <ul className="flex flex-col gap-1">
              {navItems.map((item) => (
                <li key={item.to}>
                  <NavLink
                    to={item.to}
                    className={sidebarLinkClass}
                    onClick={() => setMenuOpen(false)}
                  >
                    {item.label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </nav>
        )}
      </header>

      {/* LAYOUT */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 sm:py-8 grid grid-cols-1 lg:grid-cols-[220px_1fr] gap-6">
        {/* SIDEBAR DESKTOP */}
        <aside className="hidden lg:block">
          <nav className="rounded-2xl p-3 sticky top-24 border border-soft bg-card">
            <p className="text-[10px] uppercase tracking-widest text-muted px-3 mb-2">
              Navigation
            </p>
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
        <main className="space-y-5">
          <Outlet context={{ user, party, refetch }} />
        </main>
      </div>

      {/* ONBOARDING MODAL */}
      {needsOnboarding && (
        <OnboardingModal username={user.username} onComplete={refetch} />
      )}
    </div>
  );
};

export default Home;
