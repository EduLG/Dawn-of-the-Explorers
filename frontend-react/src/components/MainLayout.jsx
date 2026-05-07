import bgImage from "../assets/resources/bgImage.png";
import { Outlet } from "react-router-dom";

const MainLayout = () => {
  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundImage: `url(${bgImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        margin: "0px",
      }}
    >
      <Outlet />
    </div>
  );
};

export default MainLayout;
