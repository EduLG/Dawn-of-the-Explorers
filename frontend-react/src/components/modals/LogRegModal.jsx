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

  const passwordRules = [
    { label: "8+ characters", valid: password.length >= 8 },
    { label: "Uppercase letter", valid: /[A-Z]/.test(password) },
    { label: "Lowercase letter", valid: /[a-z]/.test(password) },
  ];

  const validatePassword = (pwd) => {
    if (pwd.length < 8) return "Password must be at least 8 characters.";
    if (!/[A-Z]/.test(pwd)) return "Password must contain at least one uppercase letter.";
    if (!/[a-z]/.test(pwd)) return "Password must contain at least one lowercase letter.";
    return null;
  };

  const handleRegister = async () => {
    setLocalError("");
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setLocalError("Please enter a valid email address.");
      return;
    }
    const pwdError = validatePassword(password);
    if (pwdError) {
      setLocalError(pwdError);
      return;
    }
    try {
      await register(email, userName, password);
      await login(userName, password);
      navigate("/home/team");
      setVisible(false);
    } catch (err) {
      setLocalError(err.status === 409 ? "Username or email already exists." : "Registration failed. Try again.");
    }
  };

  const handleLogin = async () => {
    setLocalError("");
    try {
      await login(userName, password);
      navigate("/home/team");
      setVisible(false);
    } catch {
      setLocalError("Invalid username or password.");
    }
  };

  return (
    // Same top offset as the login page so the modal sits below the background title.
    // It scrolls when the keyboard leaves too little height.
    <div
      className="fixed inset-0 z-50 overflow-y-auto flex flex-col items-center px-4 pb-6 pt-[calc(30dvh+1rem)]"
      style={{ background: "rgba(8,4,2,0.75)", backdropFilter: "blur(4px)", fontFamily: "var(--font-body)" }}
      onClick={() => setVisible(false)}
    >
      <div
        className="w-full max-w-sm bg-[#12090400] backdrop-blur-xl border border-white/12 rounded-2xl p-6 shadow-2xl"
        style={{ background: "rgba(20,11,4,0.92)" }}
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="text-xl font-bold text-[#f3e5c8] mb-0.5">
          {mode === "login" ? "Welcome back" : "Create account"}
        </h2>
        <p className="text-[#a89070] text-xs mb-4">
          {mode === "login" ? "Sign in to continue your adventure." : "Join and start your adventure."}
        </p>

        <div className="flex flex-col gap-3">
          {mode === "register" && (
            <div className="flex flex-col gap-1">
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

          <div className="flex flex-col gap-1">
            <label className={labelClass}>Username</label>
            <input
              type="text"
              placeholder="Username"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              className={inputClass}
            />
          </div>

          <div className="flex flex-col gap-1">
            <label className={labelClass}>Password</label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={inputClass}
            />
            {mode === "register" && password.length > 0 && (
              <ul className="flex flex-col gap-0.5 mt-1">
                {passwordRules.map((rule) => (
                  <li
                    key={rule.label}
                    className={`text-xs flex items-center gap-1.5 transition-colors ${
                      rule.valid ? "text-green-400" : "text-[#6b5a45]"
                    }`}
                  >
                    <span>{rule.valid ? "+" : "-"}</span>
                    {rule.label}
                  </li>
                ))}
              </ul>
            )}
          </div>

          {(localError || error) && (
            <p className="text-red-400 text-xs">{localError || error}</p>
          )}

          <button
            disabled={loading}
            onClick={mode === "login" ? handleLogin : handleRegister}
            className="w-full py-3 mt-1 rounded-xl bg-[#c9973b] hover:bg-[#b8862a] disabled:opacity-50 text-[#1a0f00] font-bold text-sm tracking-wide uppercase transition-colors"
          >
            {loading ? "Loading..." : mode === "login" ? "Login" : "Register"}
          </button>

          <button
            onClick={() => setVisible(false)}
            className="-mt-1 -mb-2 py-3 text-center text-xs text-[#8a7458] hover:text-[#a89070] transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default LogRegModal;
