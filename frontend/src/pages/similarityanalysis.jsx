
import { useState } from "react";
import {
  GitCompareArrows,
  Search,
  BrainCircuit,
  FileText,
  ArrowRight,
  Activity,
  Loader2,
  AlertCircle,
  RefreshCw,
  Database,
  CheckCircle2
} from "lucide-react";

import API from "../services/api";

export default function SimilarityAnalysis() {
  const [description, setDescription] = useState("");
  const [results, setResults] = useState([]);
  const [searched, setSearched] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    if (!description.trim()) {
      setError("Please enter an incident description.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResults([]);
      setSearched(false);

      const response = await API.post("/api/investigate", {
        title: "",
        description: description.trim(),
        generate_rag_report: false
      });

      const incidents = response.data.similar_incidents || [];

      // Sort by actual similarity score
      incidents.sort(
        (a, b) =>
          Number(b["Similarity (%)"] || 0) -
          Number(a["Similarity (%)"] || 0)
      );

      setResults(incidents);
      setSearched(true);

    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Failed to retrieve similar incidents. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setDescription("");
    setResults([]);
    setSearched(false);
    setError("");
  };

  return (
    <div className="space-y-6">

      {/* PAGE HEADING */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          <GitCompareArrows
            className="text-indigo-400"
            size={20}
          />

          <span className="text-indigo-400 text-sm font-medium">
            INCIDENT MATCHING
          </span>
        </div>

        <h1 className="text-3xl font-bold text-white">
          Similarity Analysis
        </h1>

        <p className="text-slate-400 mt-2">
          Identify historical incidents related to a newly reported
          AI incident using TF-IDF and cosine similarity.
        </p>
      </div>

      {/* INPUT SECTION */}
      <div className="bg-[#101729] border border-slate-800 rounded-2xl p-6">

        <div className="flex items-center gap-3 mb-5">

          <div className="bg-indigo-500/20 p-3 rounded-xl">
            <BrainCircuit
              className="text-indigo-400"
              size={23}
            />
          </div>

          <div>
            <h2 className="text-white font-semibold">
              Incident Description
            </h2>

            <p className="text-slate-400 text-sm">
              Enter an incident to find similar historical cases.
            </p>
          </div>

        </div>

        <textarea
          value={description}
          onChange={(e) => {
            setDescription(e.target.value);
            setSearched(false);
            setResults([]);
            setError("");
          }}
          placeholder="Describe the AI incident you want to compare..."
          rows={6}
          className="w-full bg-[#0b1020] border border-slate-700 rounded-xl p-4 text-white outline-none resize-none focus:border-indigo-500 placeholder:text-slate-500"
        />

        {/* ERROR */}
        {error && (
          <div className="flex items-start gap-2 text-red-400 text-sm mt-4 bg-red-500/10 border border-red-500/20 rounded-lg p-3">
            <AlertCircle size={18} className="shrink-0" />
            <p>{error}</p>
          </div>
        )}

        {/* ACTION BUTTONS */}
        <div className="flex flex-wrap justify-end gap-3 mt-4">

          {description && (
            <button
              onClick={handleReset}
              disabled={loading}
              className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-300 px-5 py-3 rounded-xl font-medium transition disabled:opacity-50"
            >
              <RefreshCw size={17} />
              Reset
            </button>
          )}

          <button
            onClick={handleSearch}
            disabled={loading || !description.trim()}
            className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed text-white px-5 py-3 rounded-xl font-medium transition"
          >
            {loading ? (
              <>
                <Loader2 size={18} className="animate-spin" />
                Searching...
              </>
            ) : (
              <>
                <Search size={18} />
                Find Similar Incidents
              </>
            )}
          </button>

        </div>

      </div>

      {/* LOADING STATE */}
      {loading && (
        <div className="bg-[#101729] border border-slate-800 rounded-2xl p-8 text-center">

          <Loader2
            size={32}
            className="animate-spin text-indigo-400 mx-auto mb-4"
          />

          <h3 className="text-white font-semibold">
            Analyzing Incident
          </h3>

          <p className="text-slate-400 text-sm mt-2">
            Comparing your incident with historical AIID records...
          </p>

        </div>
      )}

      {/* RESULTS */}
      {searched && !loading && (
        <div className="space-y-5">

          {/* RESULTS HEADER */}
          <div className="flex flex-wrap items-center justify-between gap-3">

            <div>
              <div className="flex items-center gap-2">
                <CheckCircle2
                  className="text-emerald-400"
                  size={20}
                />

                <h2 className="text-white text-xl font-semibold">
                  Similar Incident Results
                </h2>
              </div>

              <p className="text-slate-400 text-sm mt-2">
                Ranked matches retrieved from the historical AIID dataset.
              </p>
            </div>

            <span className="bg-indigo-500/20 text-indigo-400 px-3 py-2 rounded-lg text-sm font-medium">
              {results.length} Matches
            </span>

          </div>

          {/* RESULT SUMMARY */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">

            <div className="bg-[#101729] border border-slate-800 rounded-xl p-4">
              <div className="flex items-center gap-2 text-slate-400 text-sm">
                <Database size={17} />
                Historical Matches
              </div>

              <h3 className="text-white text-2xl font-bold mt-2">
                {results.length}
              </h3>
            </div>

            <div className="bg-[#101729] border border-slate-800 rounded-xl p-4">
              <div className="flex items-center gap-2 text-slate-400 text-sm">
                <Activity size={17} />
                Highest Similarity
              </div>

              <h3 className="text-emerald-400 text-2xl font-bold mt-2">
                {results.length > 0
                  ? `${Number(
                      results[0]["Similarity (%)"] || 0
                    ).toFixed(2)}%`
                  : "0.00%"}
              </h3>
            </div>

          </div>

          {/* MATCHED INCIDENTS */}
          {results.length > 0 ? (

            <div className="space-y-4">

              {results.map((incident, index) => {
                const similarity = Math.min(
                  Math.max(
                    Number(incident["Similarity (%)"] || 0),
                    0
                  ),
                  100
                );

                return (
                  <div
                    key={incident["Incident ID"] ?? index}
                    className="bg-[#101729] border border-slate-800 rounded-2xl p-5 hover:border-indigo-500/40 transition"
                  >

                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">

                      {/* INCIDENT DETAILS */}
                      <div className="flex items-start gap-4 flex-1 min-w-0">

                        <div className="bg-indigo-500/20 p-3 rounded-xl shrink-0">
                          <FileText
                            className="text-indigo-400"
                            size={22}
                          />
                        </div>

                        <div className="min-w-0">

                          <div className="flex items-center gap-2 flex-wrap">

                            <span className="text-xs text-indigo-400 font-medium">
                              MATCH #{index + 1}
                            </span>

                            {index === 0 && (
                              <span className="text-xs bg-emerald-500/10 text-emerald-400 px-2 py-1 rounded-md">
                                Best Match
                              </span>
                            )}

                          </div>

                          <h3 className="text-white font-semibold mt-2">
                            {incident.title ||
                              incident.Title ||
                              "Untitled Incident"}
                          </h3>

                          <p className="text-slate-400 text-sm mt-2 leading-6">
                            {incident.description ||
                              incident.Description ||
                              "No description available."}
                          </p>

                          <div className="flex flex-wrap gap-3 mt-3 text-xs">

                            <span className="text-slate-400">
                              ID: #{incident["Incident ID"] ?? "Unknown"}
                            </span>

                            <span className="text-indigo-400">
                              {incident["Risk Domain"] ||
                                "Unknown Domain"}
                            </span>

                          </div>

                        </div>

                      </div>

                      {/* SIMILARITY SCORE */}
                      <div className="min-w-32 md:w-36 shrink-0">

                        <p className="text-slate-400 text-xs mb-2">
                          Similarity Score
                        </p>

                        <p className="text-emerald-400 text-2xl font-bold">
                          {similarity.toFixed(2)}%
                        </p>

                        <div className="w-full h-2 bg-slate-700 rounded-full mt-2 overflow-hidden">

                          <div
                            className="h-full bg-emerald-400 rounded-full transition-all duration-500"
                            style={{
                              width: `${similarity}%`
                            }}
                          />

                        </div>

                      </div>

                    </div>

                  </div>
                );
              })}

            </div>

          ) : (

            <div className="bg-[#101729] border border-slate-800 rounded-2xl p-8 text-center">

              <Search
                size={32}
                className="text-slate-500 mx-auto mb-3"
              />

              <h3 className="text-white font-semibold">
                No Similar Incidents Found
              </h3>

              <p className="text-slate-400 text-sm mt-2">
                Try entering a more detailed incident description.
              </p>

            </div>

          )}

        </div>
      )}

      {/* INFORMATION / WORKFLOW */}
      {!searched && !loading && (
        <div className="bg-[#101729] border border-slate-800 rounded-2xl p-6">

          <div className="flex items-center gap-3">

            <Activity
              className="text-emerald-400"
              size={22}
            />

            <h2 className="text-white font-semibold">
              Similarity Analysis Workflow
            </h2>

          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mt-6">

            <div>
              <BrainCircuit
                className="text-indigo-400 mb-3"
                size={25}
              />

              <h3 className="text-white font-medium">
                Text Processing
              </h3>

              <p className="text-slate-400 text-sm mt-2">
                Process the incident description into numerical features
                using text vectorization.
              </p>
            </div>

            <div>
              <GitCompareArrows
                className="text-purple-400 mb-3"
                size={25}
              />

              <h3 className="text-white font-medium">
                Similarity Matching
              </h3>

              <p className="text-slate-400 text-sm mt-2">
                Compare the submitted incident against historical
                incident records using cosine similarity.
              </p>
            </div>

            <div>
              <ArrowRight
                className="text-emerald-400 mb-3"
                size={25}
              />

              <h3 className="text-white font-medium">
                Ranked Results
              </h3>

              <p className="text-slate-400 text-sm mt-2">
                Display the top matching incidents with their
                similarity scores.
              </p>
            </div>

          </div>

        </div>
      )}

    </div>
  );
}
