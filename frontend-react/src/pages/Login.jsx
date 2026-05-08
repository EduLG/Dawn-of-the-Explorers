import { useState } from "react";
import LogRegModal from "../components/modals/LogRegModal";
import headerlogo from "../assets/resources/header-logo.png";

const Login = () => {
  const [logRegVisible, setLogRegVisible] = useState(false);
  const [mode, setMode] = useState("login");

  const openModal = (selectedMode) => {
    setMode(selectedMode);
    setLogRegVisible(true);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4" style={{ fontFamily: "var(--font-body)" }}>
      <div className="w-full max-w-md flex flex-col items-center gap-8">
        <div
          className="w-full backdrop-blur-xl border border-[#c9973b]/20 rounded-2xl p-8 flex flex-col gap-4 shadow-2xl"
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
