import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

const inputClass =
  "w-full bg-white/8 border border-white/15 rounded-lg px-4 py-2.5 text-[#f3e5c8] placeholder-[#6b5a45] text-sm focus:outline-none focus:border-[#c9973b]/60 focus:bg-white/10 transition-colors";

const labelClass = "text-xs uppercase tracking-widest text-[#a89070]";

const LogRegModal = ({ visible, setVisible, mode }) => {
  const navigate = useNavigate();
  const { login, register, loading, error } = useAuth();
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [localError, setLocalError] = useState("");

  if (!visible) return null;

  const handleRegister = async () => {
    setLocalError("");
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regex.test(email)) {
      setLocalError("Please enter a valid email address.");
      return;
    }
    try {
      await register(email, userName, password);
      navigate("/home/team");
      setVisible(false);
    } catch (e) {
      setLocalError(e.status === 409 ? "Username or email already exists." : "Registration failed. Try again.");
    }
  };

  const handleLogin = async () => {
    setLocalError("");
    try {
      await login(userName, password);
      navigate("/home/team");
      setVisible(false);
    } catch (e) {
      setLocalError("Invalid username or password.");
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center px-4"
      style={{ background: "rgba(8,4,2,0.75)", backdropFilter: "blur(4px)" }}
      onClick={() => setVisible(false)}
    >
      <div
        className="w-full max-w-sm bg-[#12090400] backdrop-blur-xl border border-white/12 rounded-2xl p-8 shadow-2xl"
        style={{ background: "rgba(20,11,4,0.92)" }}
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="text-2xl font-bold text-[#f3e5c8] mb-1">
          {mode === "login" ? "Welcome back" : "Create account"}
        </h2>
        <p className="text-[#a89070] text-xs mb-6">
          {mode === "login" ? "Sign in to continue your adventure." : "Join and start your adventure."}
        </p>

        <div className="flex flex-col gap-4">
          {mode === "register" && (
            <div className="flex flex-col gap-1.5">
              <label className={labelClass}>Email</label>
              <input
                type="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className={inputClass}
              />
            </div>
          )}

          <div className="flex flex-col gap-1.5">
            <label className={labelClass}>Username</label>
            <input
              type="text"
              placeholder="Username"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              className={inputClass}
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className={labelClass}>Password</label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={inputClass}
            />
          </div>

          {(localError || error) && (
            <p className="text-red-400 text-xs">{localError || error}</p>
          )}

          <button
            disabled={loading}
            onClick={mode === "login" ? handleLogin : handleRegister}
            className="w-full py-3 mt-2 rounded-xl bg-[#c9973b] hover:bg-[#b8862a] disabled:opacity-50 text-[#1a0f00] font-bold text-sm tracking-wide uppercase transition-colors"
          >
            {loading ? "Loading..." : mode === "login" ? "Login" : "Register"}
          </button>

          <button
            onClick={() => setVisible(false)}
            className="text-center text-xs text-[#6b5a45] hover:text-[#a89070] transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default LogRegModal;
