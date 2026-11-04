import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Sidebar from "./components/sidebar";
import Topbar from "./components/topbar";

import Dashboard from "./pages/dashboard";
import Investigation from "./pages/investigation";
import HistoricalIncidents from "./pages/historicalincidents";
import SimilarityAnalysis from "./pages/similarityanalysis";
import InvestigationReport from "./pages/investigationreport";
import About from "./pages/about";

function AppLayout() {
  const [collapsed, setCollapsed] = useState(true);

  return (
    <div className="min-h-screen flex bg-[#0b1020]">

      {/* Sidebar */}
      <Sidebar
        collapsed={collapsed}
        setCollapsed={setCollapsed}
      />

      {/* Main Application Area */}
      <div className="flex-1 min-w-0 min-h-screen flex flex-col">

        {/* Top Navigation */}
        <Topbar />

        {/* Page Content */}
        <main className="flex-1 min-w-0 p-8 overflow-x-hidden">

          <Routes>
            <Route path="/" element={<Dashboard />} />

            <Route
              path="/investigation"
              element={<Investigation />}
            />

            <Route
              path="/incidents"
              element={<HistoricalIncidents />}
            />

            <Route
              path="/similarity"
              element={<SimilarityAnalysis />}
            />

            <Route
              path="/reports"
              element={<InvestigationReport />}
            />

            <Route
              path="/about"
              element={<About />}
            />
          </Routes>

        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppLayout />
    </BrowserRouter>
  );
}