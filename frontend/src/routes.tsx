import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/dashboard";
import Expenses from "./pages/expense";
import Categories from "./pages/categories";
import Settings from "./pages/settings";
import Stats from "./pages/Stats";

function AppRoutes() {
  return (
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/expenses" element={<Expenses />} />
        <Route path="/categories" element={<Categories />} />
        <Route path="/statistics" element={<Stats />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
  );
}

export default AppRoutes;

