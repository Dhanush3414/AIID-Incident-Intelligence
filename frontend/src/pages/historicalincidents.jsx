
import { useEffect, useState } from "react";
import {
  Search,
  Filter,
  Database,
  AlertTriangle,
  Loader2,
  ChevronLeft,
  ChevronRight
} from "lucide-react";

import API from "../services/api";

const domains = [
  "All Domains",
  "Malicious Actors & Misuse",
  "AI system safety, failures, and limitations",
  "Discrimination and Toxicity",
  "Misinformation",
  "Privacy & Security",
  "Human-Computer Interaction",
  "Socioeconomic & Environmental Harms"
];

export default function HistoricalIncidents() {
  const [incidents, setIncidents] = useState([]);
  const [search, setSearch] = useState("");
  const [selectedDomain, setSelectedDomain] = useState("All Domains");
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchIncidents = async () => {
      setLoading(true);
      setError("");

      try {
        const response = await API.get("/api/incidents", {
          params: {
            page,
            page_size: 100,
            search,
            domain: selectedDomain
          }
        });

        setIncidents(response.data.incidents);
        setTotal(response.data.total);
        setTotalPages(response.data.total_pages);
      } catch (err) {
        console.error(err);
        setError("Unable to load incidents. Check the backend.");
      } finally {
        setLoading(false);
      }
    };

    fetchIncidents();
  }, [page, search, selectedDomain]);

  const handleSearch = (value) => {
    setSearch(value);
    setPage(1);
  };

  const handleDomain = (value) => {
    setSelectedDomain(value);
    setPage(1);
  };

  return (
    <div className="space-y-6">

      {/* Heading */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          <Database className="text-indigo-400" size={20} />
          <span className="text-indigo-400 text-sm font-medium">
            INCIDENT DATABASE
          </span>
        </div>

        <h1 className="text-3xl font-bold text-white">
          Historical Incidents
        </h1>

        <p className="text-slate-400 mt-2">
          Explore and analyze previously reported AI-related incidents.
        </p>
      </div>

      {/* Summary */}
      <div className="bg-[#101729] border border-slate-800 rounded-2xl p-5">
        <p className="text-slate-400 text-sm">Matching Incidents</p>
        <h2 className="text-white text-2xl font-bold">
          {total.toLocaleString()}
        </h2>
        <p className="text-slate-500 text-xs mt-1">
          From the AIID incident database
        </p>
      </div>

      {/* Search and Filter */}
      <div className="bg-[#101729] border border-slate-800 rounded-2xl p-5">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

          <div>
            <label className="text-slate-300 text-sm mb-2 block">
              Search Incidents
            </label>

            <div className="flex items-center gap-3 bg-[#0b1020] border border-slate-700 rounded-xl px-4">
              <Search size={18} className="text-slate-400" />
              <input
                value={search}
                onChange={(e) => handleSearch(e.target.value)}
                placeholder="Search by title or description..."
                className="w-full bg-transparent py-3 text-white outline-none placeholder:text-slate-500"
              />
            </div>
          </div>

          <div>
            <label className="text-slate-300 text-sm mb-2 block">
              Filter by Risk Domain
            </label>

            <div className="flex items-center gap-3 bg-[#0b1020] border border-slate-700 rounded-xl px-4">
              <Filter size={18} className="text-slate-400" />
              <select
                value={selectedDomain}
                onChange={(e) => handleDomain(e.target.value)}
                className="w-full bg-transparent py-3 text-white outline-none"
              >
                {domains.map((domain) => (
                  <option key={domain} value={domain} className="bg-[#101729]">
                    {domain}
                  </option>
                ))}
              </select>
            </div>
          </div>

        </div>
      </div>

      {/* Table */}
      <div className="bg-[#101729] border border-slate-800 rounded-2xl overflow-hidden">

        <div className="p-5 border-b border-slate-800">
          <h2 className="text-white text-lg font-semibold">
            Incident Records
          </h2>
          <p className="text-slate-400 text-sm mt-1">
            Browse actual AI incidents and their classifications.
          </p>
        </div>

        {loading ? (
          <div className="flex justify-center items-center gap-3 py-16 text-indigo-400">
            <Loader2 className="animate-spin" />
            Loading incidents...
          </div>
        ) : error ? (
          <div className="p-10 text-center text-red-400">
            <AlertTriangle className="mx-auto mb-2" />
            {error}
          </div>
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead className="bg-slate-800/50">
                  <tr className="text-slate-400 text-xs uppercase">
                    <th className="px-5 py-4">Incident ID</th>
                    <th className="px-5 py-4">Incident Title</th>
                    <th className="px-5 py-4">Risk Domain</th>
                    <th className="px-5 py-4">Year</th>
                    <th className="px-5 py-4">AI Harm Level</th>
                  </tr>
                </thead>

                <tbody>
                  {incidents.map((incident, index) => (
                    <tr
                      key={incident["Incident ID"] || index}
                      className="border-t border-slate-800 hover:bg-slate-800/30 transition"
                    >
                      <td className="px-5 py-4 text-indigo-400 text-sm">
                        #{incident["Incident ID"] || "Unknown"}
                      </td>

                      <td className="px-5 py-4 min-w-64">
                        <p className="text-white text-sm font-medium">
                          {incident.title || "Untitled Incident"}
                        </p>
                        <p className="text-slate-500 text-xs mt-1">
                          {incident.description || "No description available"}
                        </p>
                      </td>

                      <td className="px-5 py-4 text-slate-300 text-sm">
                        {incident["Risk Domain"] || "Unknown"}
                      </td>

                      <td className="px-5 py-4 text-slate-400 text-sm">
                        {incident.year || incident["Incident Year"] || "Unknown"}
                      </td>

                      <td className="px-5 py-4 text-slate-300 text-sm">
                        {incident["AI Harm Level"] || "Unknown"}
                      </td>
                    </tr>
                  ))}

                  {incidents.length === 0 && (
                    <tr>
                      <td colSpan="5" className="px-5 py-12 text-center">
                        <AlertTriangle className="mx-auto text-amber-400 mb-3" size={28} />
                        <p className="text-slate-300">No incidents found.</p>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            <div className="flex flex-wrap items-center justify-between gap-4 p-5 border-t border-slate-800">
              <p className="text-slate-400 text-sm">
                Showing {total === 0 ? 0 : (page - 1) * 100 + 1}–{Math.min(page * 100, total)} of {total.toLocaleString()} incidents
              </p>

              <div className="flex items-center gap-3">
                <button
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1 || loading}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800 text-white disabled:opacity-40 hover:bg-slate-700"
                >
                  <ChevronLeft size={17} />
                  Previous
                </button>

                <span className="text-slate-300 text-sm">
                  Page {page} of {totalPages}
                </span>

                <button
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={page >= totalPages || loading}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white disabled:opacity-40 hover:bg-indigo-500"
                >
                  Next
                  <ChevronRight size={17} />
                </button>
              </div>
            </div>
          </>
        )}
      </div>

    </div>
  );
}
