import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Theme } from "@radix-ui/themes";
import { PrimeReactProvider } from "primereact/api";
import "@radix-ui/themes/styles.css";
import "primereact/resources/themes/lara-dark-amber/theme.css";
import "primereact/resources/primereact.css";
import App from "./App.jsx";
import "./styles/index.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <PrimeReactProvider>
      <Theme appearance="dark" accentColor="brown">
        <App />
      </Theme>
    </PrimeReactProvider>
  </StrictMode>
);
