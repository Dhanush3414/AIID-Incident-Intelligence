
import {
  LayoutDashboard,
  ShieldAlert,
  Database,
  GitCompareArrows,
  FileText,
  Info,
  BrainCircuit,
  Activity,
  ChevronLeft,
  ChevronRight
} from "lucide-react";

import { NavLink } from "react-router-dom";

const menuItems = [
  {
    title: "MAIN MENU",
    items: [
      { name: "Dashboard", path: "/", icon: LayoutDashboard },
      { name: "Investigation", path: "/investigation", icon: ShieldAlert },
      { name: "Historical Incidents", path: "/incidents", icon: Database },
      { name: "Similarity Analysis", path: "/similarity", icon: GitCompareArrows },
    ],
  },
  {
    title: "INTELLIGENCE",
    items: [
      { name: "AI Investigation Report", path: "/reports", icon: FileText },
      { name: "About Project", path: "/about", icon: Info },
    ],
  },
];

export default function Sidebar({ collapsed, setCollapsed }) {

  return (
    <aside
      className={`h-screen sticky top-0 z-50 flex-shrink-0 flex flex-col border-r border-slate-800 bg-[#101729] transition-all duration-300 ${
      collapsed ? "w-20" : "w-64"
      }`}
    >
      {/* Logo */}
      <div className="h-20 flex items-center justify-between px-5 border-b border-slate-800">
        <div className="flex items-center gap-3 overflow-hidden">
          <div className="bg-indigo-600 p-2 rounded-xl">
            <BrainCircuit size={25} />
          </div>

          {!collapsed && (
            <div>
              <h1 className="text-white font-bold text-lg tracking-wide">
                AIID
              </h1>
              <p className="text-slate-400 text-xs">
                Incident Intelligence
              </p>
            </div>
          )}
        </div>

        <button
          onClick={() => setCollapsed(!collapsed)}
          className="text-slate-400 hover:text-white"
          title="Toggle sidebar"
        >
          {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-6 overflow-y-auto">
        {menuItems.map((section) => (
          <div key={section.title} className="mb-8">
            {!collapsed && (
              <p className="text-slate-500 text-xs font-semibold px-3 mb-4 tracking-widest">
                {section.title}
              </p>
            )}

            <div className="space-y-2">
              {section.items.map((item) => {
                const Icon = item.icon;

                return (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    end={item.path === "/"}
                    title={collapsed ? item.name : ""}
                    className={({ isActive }) =>
                      `flex items-center gap-3 px-3 py-3 rounded-xl transition-all ${
                        isActive
                          ? "bg-indigo-600/20 text-indigo-400 border border-indigo-500/30"
                          : "text-slate-400 hover:bg-slate-800 hover:text-white"
                      }`
                    }
                  >
                    <Icon size={20} />

                    {!collapsed && (
                      <span className="text-sm font-medium">
                        {item.name}
                      </span>
                    )}
                  </NavLink>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      {/* System Status */}
      {!collapsed && (
        <div className="p-4 border-t border-slate-800">
          <div className="bg-slate-800/60 rounded-xl p-3">
            <div className="flex items-center gap-2 mb-2">
              <Activity size={16} className="text-emerald-400" />
              <span className="text-sm text-white font-medium">
                System Status
              </span>
            </div>

            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span className="text-xs text-slate-400">
                Interface initialized
              </span>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
}
