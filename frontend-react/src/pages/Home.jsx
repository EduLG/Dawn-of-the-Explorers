import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { Avatar, DropdownMenu } from "@radix-ui/themes";
import useUser from "../hooks/useUser";
import OnboardingModal from "../components/OnboardingModal";
import { isDemoToken } from "../utils/jwt";
import bgImage from "../assets/resources/bgImage.png";
import headerlogo from "../assets/resources/header-logo.png";

const navItems = [
  { label: "Team", mobileLabel: "Team", icon: "pi-users", to: "/home/team" },
  { label: "Characters", mobileLabel: "Chars", icon: "pi-user", to: "/home/equipment" },
  { label: "Inventory", mobileLabel: "Inventory", icon: "pi-box", to: "/home/inventory" },
  { label: "Exploration quests", mobileLabel: "Quests", icon: "pi-compass", to: "/home/quests" },
  { label: "Market", mobileLabel: "Market", icon: "pi-shopping-bag", to: "/home/market" },
];

const sidebarLinkClass = ({ isActive }) =>
  `flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-sm transition-all duration-200 ${
    isActive
      ? "bg-accent-dim border border-accent text-primary font-semibold"
      : "text-muted hover:bg-white/8 hover:text-primary border border-transparent"
  }`;

const bottomLinkClass = ({ isActive }) =>
  `flex flex-col items-center justify-center gap-1 min-h-14 px-1 border-t-2 transition-colors duration-200 ${
    isActive
      ? "border-[var(--accent)] text-accent bg-accent-dim"
      : "border-transparent text-muted"
  }`;

const Home = () => {
  const { data: user, refetch } = useUser();
  const party = user?.party;
  const needsOnboarding = user && party && party.characters.length === 0;
  const isDemo = isDemoToken(localStorage.getItem("token"));

  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
    navigate("/login");
  };

  return (
    <div
      className="min-h-screen w-full antialiased px-safe"
      style={{
        backgroundImage: `linear-gradient(rgba(10,6,2,0.72), rgba(10,6,2,0.72)), url(${bgImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      {/* HEADER */}
      <header className="sticky top-0 z-20 backdrop-blur-md bg-header border-b border-faint pt-safe">
        {/* DEMO BANNER */}
        {isDemo && (
          <div className="w-full py-1.5 px-4 text-center text-xs font-semibold tracking-wide uppercase bg-[#c9973b]/15 border-b border-[#c9973b]/20 text-[#c9973b]">
            <span className="sm:hidden">Demo mode — not saved</span>
            <span className="hidden sm:inline">Demo mode — changes are not saved</span>
          </div>
        )}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
          <img src={headerlogo} alt="Logo" className="h-10 sm:h-12" />

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

      </header>

      {/* LAYOUT (extra bottom padding on mobile leaves room for the bottom nav) */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 pt-6 sm:pt-8 pb-[calc(6rem_+_env(safe-area-inset-bottom))] lg:pb-8 grid grid-cols-1 lg:grid-cols-[220px_1fr] gap-6">
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

      {/* BOTTOM NAV MOBILE */}
      <nav className="lg:hidden fixed bottom-0 inset-x-0 z-20 backdrop-blur-md bg-header border-t border-faint pb-safe px-safe">
        <ul className="grid grid-cols-5">
          {navItems.map((item) => (
            <li key={item.to}>
              <NavLink to={item.to} className={bottomLinkClass}>
                <i className={`pi ${item.icon} text-lg`} aria-hidden="true" />
                <span className="text-[13px] leading-none">{item.mobileLabel}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      {/* ONBOARDING MODAL */}
      {needsOnboarding && (
        <OnboardingModal username={user.username} onComplete={refetch} />
      )}
    </div>
  );
};

export default Home;
