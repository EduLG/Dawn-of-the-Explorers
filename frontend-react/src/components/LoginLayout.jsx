import { Outlet } from "react-router-dom";
import loginImage from "../assets/resources/dawn_of_the_explorers.png";

const LoginLayout = () => {
  return (
    <div
      className="min-h-screen w-full"
      style={{
        backgroundImage: `url(${loginImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center 30%",
      }}
    >
      <Outlet />
    </div>
  );
};

export default LoginLayout;
