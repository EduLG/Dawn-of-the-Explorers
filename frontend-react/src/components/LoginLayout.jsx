import { Outlet } from "react-router-dom";
import loginImage from "../assets/resources/dawn_of_the_explorers.png";

const LoginLayout = () => {
  return (
    <div
      className="min-h-screen w-full"
      style={{
        backgroundImage: `linear-gradient(rgba(10,6,2,0.65), rgba(10,6,2,0.65)), url(${loginImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center 30%",
      }}
    >
      <Outlet />
    </div>
  );
};

export default LoginLayout;
