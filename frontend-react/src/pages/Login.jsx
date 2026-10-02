import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import LogRegModal from "../components/modals/LogRegModal";

const Login = () => {
  const navigate = useNavigate();
  const { loginDemo, loading } = useAuth();
  const [logRegVisible, setLogRegVisible] = useState(false);
  const [mode, setMode] = useState("login");
  const [demoError, setDemoError] = useState("");

  const openModal = (selectedMode) => {
    setMode(selectedMode);
    setLogRegVisible(true);
  };

  const handleDemo = async () => {
    setDemoError("");
    try {
      await loginDemo();
      navigate("/home/team");
    } catch {
      setDemoError("Could not start demo. Try again.");
    }
  };

  return (
    // The title is painted in the background image and always ends near 30% of the viewport height,
    // so the content starts just below it instead of being centered over it.
    <div className="min-h-full flex flex-col items-center px-4 pb-6 pt-[calc(30dvh+1rem)]" style={{ fontFamily: "var(--font-body)" }}>
      <div className="w-full max-w-md flex flex-col items-center gap-8">
        <div
          className={`w-full backdrop-blur-xl border border-[#c9973b]/20 rounded-2xl p-6 sm:p-8 flex flex-col gap-4 shadow-2xl ${
            logRegVisible ? "invisible" : ""
          }`}
          style={{ background: "rgba(13,7,3,0.88)" }}
        >
          <button
            onClick={() => openModal("login")}
            className="w-full py-3 rounded-xl bg-[#c9973b] hover:bg-[#b8862a] text-[#1a0f00] font-bold text-sm tracking-wide uppercase transition-colors shadow-lg"
          >
            Login
          </button>
          <button
            onClick={() => openModal("register")}
            className="w-full py-3 rounded-xl bg-[#c9973b]/10 hover:bg-[#c9973b]/20 border border-[#c9973b]/30 text-[#f3e5c8] font-semibold text-sm tracking-wide uppercase transition-colors"
          >
            Create Account
          </button>

          <div className="flex items-center gap-3 my-1">
            <div className="flex-1 h-px bg-white/10" />
            <span className="text-[#6b5a45] text-xs uppercase tracking-widest">or</span>
            <div className="flex-1 h-px bg-white/10" />
          </div>

          <button
            onClick={handleDemo}
            disabled={loading}
            className="w-full py-3 rounded-xl bg-transparent hover:bg-white/5 border border-white/10 text-[#a89070] hover:text-[#f3e5c8] font-semibold text-sm tracking-wide uppercase transition-colors disabled:opacity-50"
          >
            {loading ? "Starting..." : "Try Demo"}
          </button>

          {demoError && (
            <p className="text-red-400 text-xs text-center">{demoError}</p>
          )}

          <p className="text-[#8a7458] text-xs text-center">
            Demo mode — no account needed, changes are not saved
          </p>
        </div>
      </div>

      <LogRegModal
        visible={logRegVisible}
        setVisible={setLogRegVisible}
        mode={mode}
      />
    </div>
  );
};

export default Login;
