
import { useEffect, useState } from "react";
import API from "../services/api";

import {
  Database,
  BrainCircuit,
  ShieldAlert,
  Target,
  AlertTriangle,
  Activity
} from "lucide-react";

import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid
} from "recharts";

import StatCard from "../components/statcard";

const COLORS = [
  "#818cf8",
  "#a78bfa",
  "#c084fc",
  "#38bdf8",
  "#34d399",
  "#fbbf24",
  "#fb7185"
];

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await API.get("/api/dashboard/stats");
        setStats(response.data);
      } catch (error) {
        console.error("Error fetching dashboard stats:", error);
        setError("Unable to load dashboard statistics.");
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <Activity className="text-indigo-400 animate-pulse mx-auto mb-3" size={35} />
          <p className="text-slate-400">Loading dashboard statistics...</p>
        </div>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-5 text-red-400">
        {error || "Dashboard data is unavailable."}
      </div>
    );
  }

  const riskData = (stats.risk_distribution || []).map((item) => ({
    name: item.domain,
    value: item.count
  }));

  const summaryData = (stats.classification_distribution || []).map(
    (item) => ({
      name: item.status,
      value: item.count
    })
  );

  const totalIncidents = stats.total_incidents || 0;
  const classifiedIncidents = stats.classified_incidents || 0;
  const unclassifiedIncidents = stats.unclassified_incidents || 0;

  const coverage =
    totalIncidents > 0
      ? ((classifiedIncidents / totalIncidents) * 100).toFixed(2)
      : "0.00";

  return (
    <div className="space-y-8">

      {/* Page Heading */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          <Activity className="text-indigo-400" size={20} />
          <span className="text-indigo-400 text-sm font-medium">
            OVERVIEW
          </span>
        </div>

        <h1 className="text-3xl font-bold text-white">
          Intelligence Dashboard
        </h1>

        <p className="text-slate-400 mt-2">
          Monitor, analyze and investigate AI-related incidents.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">

        <StatCard
          title="Total Incidents"
          value={totalIncidents.toLocaleString()}
          description="Records in AIID dataset"
          icon={Database}
          color="bg-indigo-500/20 text-indigo-400"
        />

        <StatCard
          title="Classified Incidents"
          value={classifiedIncidents.toLocaleString()}
          description="Incidents with known risk domains"
          icon={BrainCircuit}
          color="bg-emerald-500/20 text-emerald-400"
        />

        <StatCard
          title="Risk Domains"
          value={stats.risk_domains_count}
          description="Available classification categories"
          icon={ShieldAlert}
          color="bg-purple-500/20 text-purple-400"
        />

        <StatCard
          title="Model Accuracy"
          value="72.67%"
          description="Logistic Regression classifier"
          icon={Target}
          color="bg-sky-500/20 text-sky-400"
        />

      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">

        {/* Risk Domain Distribution */}
        <div className="bg-[#101729] border border-slate-800 rounded-2xl p-6">

          <h2 className="text-white text-lg font-semibold">
            Risk Domain Distribution
          </h2>

          <p className="text-slate-400 text-sm mt-1">
            Distribution of classified AI incidents
          </p>

          <div className="h-80 mt-5">
            {riskData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={riskData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    innerRadius={65}
                    outerRadius={105}
                    paddingAngle={3}
                  >
                    {riskData.map((entry, index) => (
                      <Cell
                        key={entry.name}
                        fill={COLORS[index % COLORS.length]}
                      />
                    ))}
                  </Pie>

                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#172033",
                      border: "1px solid #334155",
                      borderRadius: "10px",
                      color: "#ffffff"
                    }}
                  />

                  <Legend
                    verticalAlign="bottom"
                    height={45}
                    wrapperStyle={{
                      color: "#94a3b8",
                      fontSize: "11px"
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-slate-400 text-center pt-24">
                No risk domain data available.
              </p>
            )}
          </div>
        </div>

        {/* Classification Summary */}
        <div className="bg-[#101729] border border-slate-800 rounded-2xl p-6">

          <h2 className="text-white text-lg font-semibold">
            Classification Summary
          </h2>

          <p className="text-slate-400 text-sm mt-1">
            Labeled versus unlabeled incident records
          </p>

          <div className="h-80 mt-5">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={summaryData}
                margin={{ top: 20, right: 15, left: 0, bottom: 10 }}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#273449"
                  vertical={false}
                />

                <XAxis
                  dataKey="name"
                  stroke="#94a3b8"
                  tickLine={false}
                />

                <YAxis
                  stroke="#94a3b8"
                  tickLine={false}
                />

                <Tooltip
                  contentStyle={{
                    backgroundColor: "#172033",
                    border: "1px solid #334155",
                    borderRadius: "10px",
                    color: "#ffffff"
                  }}
                />

                <Bar
                  dataKey="value"
                  radius={[8, 8, 0, 0]}
                >
                  <Cell fill="#818cf8" />
                  <Cell fill="#f59e0b" />
                </Bar>

              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

      {/* Dataset Quality Overview */}
      <div className="bg-[#101729] border border-slate-800 rounded-2xl p-6">

        <div className="flex items-center gap-3 mb-5">
          <AlertTriangle className="text-amber-400" size={22} />

          <div>
            <h2 className="text-white font-semibold">
              Dataset Quality Overview
            </h2>

            <p className="text-slate-400 text-sm">
              Incident classification coverage
            </p>
          </div>
        </div>

        <div className="flex justify-between text-sm mb-2">
          <span className="text-slate-300">
            Classification coverage
          </span>

          <span className="text-white font-semibold">
            {coverage}%
          </span>
        </div>

        <div className="w-full h-3 rounded-full bg-slate-700 overflow-hidden">
          <div
            className="h-full bg-indigo-500 rounded-full transition-all duration-500"
            style={{ width: `${coverage}%` }}
          />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-5">

          <div className="bg-slate-800/50 rounded-xl p-4">
            <p className="text-slate-400 text-sm">
              Classified records
            </p>

            <p className="text-emerald-400 text-2xl font-bold mt-2">
              {classifiedIncidents.toLocaleString()}
            </p>
          </div>

          <div className="bg-slate-800/50 rounded-xl p-4">
            <p className="text-slate-400 text-sm">
              Missing risk domain
            </p>

            <p className="text-amber-400 text-2xl font-bold mt-2">
              {unclassifiedIncidents.toLocaleString()}
            </p>
          </div>

        </div>
      </div>

    </div>
  );
}
