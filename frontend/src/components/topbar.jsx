
import {
  Search,
  Bell,
  UserCircle,
  CalendarDays,
  ShieldCheck
} from "lucide-react";

export default function Topbar() {
  return (
    <header className="h-20 bg-[#101729] border-b border-slate-800 flex items-center justify-between px-8">
      
      {/* Page Title */}
      <div>
        <h2 className="text-white text-xl font-semibold">
          AI Incident Intelligence
        </h2>
        <p className="text-slate-400 text-xs mt-1">
          AI-powered incident analysis and investigation platform
        </p>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-5">

        {/* Search */}
        <button className="text-slate-400 hover:text-white transition">
          <Search size={20} />
        </button>

        {/* Date */}
        <div className="hidden lg:flex items-center gap-2 text-slate-400 text-sm">
          <CalendarDays size={17} />
          <span>Incident Intelligence</span>
        </div>

        {/* Notification */}
        <button className="relative text-slate-400 hover:text-white transition">
          <Bell size={20} />
          <span className="absolute -top-1 -right-1 w-2 h-2 rounded-full bg-indigo-500"></span>
        </button>

        {/* Divider */}
        <div className="h-8 w-px bg-slate-700"></div>

        {/* User Profile */}
        <div className="flex items-center gap-3">
          <div className="bg-indigo-600/20 p-2 rounded-full">
            <UserCircle size={24} className="text-indigo-400" />
          </div>

          <div className="hidden md:block">
            <p className="text-white text-sm font-medium">
              Administrator
            </p>
            <p className="text-slate-500 text-xs">
              AIID Analyst
            </p>
          </div>
        </div>

      </div>
    </header>
  );
}
