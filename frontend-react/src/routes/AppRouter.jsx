import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Home from "../pages/Home";
import Login from "../pages/Login";
import LoginLayout from "../components/LoginLayout";
import ProtectedRoute from "../components/ProtectedRoute";
import TeamView from "../views/TeamView";
import EquipmentView from "../views/EquipmentView";
import QuestsView from "../views/QuestsView";
import MarketView from "../views/MarketView";
import InventoryView from "../views/InventoryView";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<LoginLayout />}>
          <Route path="/login" element={<Login />} />
        </Route>

        <Route element={<ProtectedRoute />}>
          <Route index element={<Navigate to="/home/team" replace />} />
          <Route path="/home" element={<Home />}>
            <Route index element={<Navigate to="team" replace />} />
            <Route path="team" element={<TeamView />} />
            <Route path="equipment" element={<EquipmentView />} />
            <Route path="quests" element={<QuestsView />} />
            <Route path="market" element={<MarketView />} />
            <Route path="inventory" element={<InventoryView />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
