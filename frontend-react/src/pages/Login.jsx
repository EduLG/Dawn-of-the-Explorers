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
    <div className="min-h-screen flex flex-col items-center justify-center px-4">
      <div className="w-full max-w-md flex flex-col items-center gap-8">

        <div className="flex flex-col items-center gap-4">
          <img src={headerlogo} alt="Dawn of Explorers" className="h-24 drop-shadow-xl" />
          <p className="text-[#a89070] text-sm tracking-widest uppercase">
            Your adventure awaits
          </p>
        </div>

        <div className="w-full bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-8 flex flex-col gap-4 shadow-2xl">
          <button
            onClick={() => openModal("login")}
            className="w-full py-3 rounded-xl bg-[#c9973b] hover:bg-[#b8862a] text-[#1a0f00] font-bold text-sm tracking-wide uppercase transition-colors shadow-lg"
          >
            Login
          </button>
          <button
            onClick={() => openModal("register")}
            className="w-full py-3 rounded-xl bg-white/8 hover:bg-white/12 border border-white/15 text-[#f3e5c8] font-semibold text-sm tracking-wide uppercase transition-colors"
          >
            Create Account
          </button>
        </div>

      </div>

      <LogRegModal visible={logRegVisible} setVisible={setLogRegVisible} mode={mode} />
    </div>
  );
};

export default Login;
