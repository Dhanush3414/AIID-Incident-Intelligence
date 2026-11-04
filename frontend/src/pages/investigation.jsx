
import ReactMarkdown from "react-markdown";
import { useState } from "react";

import {
  ShieldAlert,
  Sparkles,
  Search,
  Loader2,
  AlertCircle,
  FileText,
  BrainCircuit,
  Database,
  CheckCircle2,
  Activity,
  Target
} from "lucide-react";

import API from "../services/api";

export default function Investigation() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [generateRag, setGenerateRag] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const analyzeIncident = async () => {
    if (!title.trim() && !description.trim()) {
      setError("Enter an incident title or description.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const response = await API.post("/api/investigate", {
        title,
        description,
        generate_rag_report: generateRag
      });

      setResult(response.data);

      localStorage.setItem(
        "latestInvestigationReport",
        JSON.stringify({
          title,
          description,
          predicted_domain: response.data.predicted_domain,
          probabilities: response.data.probabilities,
          investigation_report: response.data.investigation_report,
          rag_evidence: response.data.rag_evidence,
          similar_incidents: response.data.similar_incidents,
          created_at: new Date().toLocaleString()
        })
      );

    } catch (err) {
      console.error("Investigation error:", err);

      setError(
        err.response?.data?.detail ||
        "Failed to analyze incident. Please try again."
      );

    } finally {
      setLoading(false);
    }
  };

  const resetInvestigation = () => {
    setTitle("");
    setDescription("");
    setGenerateRag(false);
    setResult(null);
    setError("");
  };

  const probabilities = Object.entries(
    result?.probabilities || {}
  ).sort((a, b) => b[1] - a[1]);

  const highestConfidence = probabilities.length
    ? (probabilities[0][1] * 100).toFixed(2)
    : "N/A";

  const similarIncidents = result?.similar_incidents || [];
  const ragEvidence = result?.rag_evidence || [];

  return (
    <div className="space-y-8">

      {/* Page Heading */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          <ShieldAlert className="text-indigo-400" size={20} />

          <span className="text-indigo-400 text-sm font-medium">
            INCIDENT ANALYSIS
          </span>
        </div>

        <h1 className="text-3xl font-bold text-white">
          Incident Investigation
        </h1>

        <p className="text-slate-400 mt-2">
          Analyze AI-related incidents using machine learning,
          historical incident matching and retrieval-augmented generation.
        </p>
      </div>

      {/* Incident Input */}
      <div className="bg-[#101729] border border-slate-800 rounded-2xl p-6 space-y-5">

        <div className="flex items-center gap-2">
          <BrainCircuit className="text-indigo-400" size={21} />

          <h2 className="text-white font-semibold text-lg">
            Incident Information
          </h2>
        </div>

        {/* Title */}
        <div>
          <label className="text-sm text-slate-300">
            Incident Title
          </label>

          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter incident title..."
            className="w-full mt-2 bg-[#0b1020] border border-slate-700 rounded-xl p-4 text-white outline-none focus:border-indigo-500"
          />
        </div>

        {/* Description */}
        <div>
          <label className="text-sm text-slate-300">
            Incident Description
          </label>

          <textarea
            rows="7"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe what happened, the AI system involved, affected users, and potential consequences..."
            className="w-full mt-2 bg-[#0b1020] border border-slate-700 rounded-xl p-4 text-white placeholder-slate-500 outline-none focus:border-indigo-500 resize-none"
          />
        </div>

        {/* RAG Option */}
        <label className="flex items-center gap-3 text-sm text-slate-300 cursor-pointer">
          <input
            type="checkbox"
            checked={generateRag}
            onChange={(e) => setGenerateRag(e.target.checked)}
            className="accent-indigo-500 w-4 h-4"
          />

          Generate AI investigation report using RAG
        </label>

        <p className="text-xs text-slate-500">
          Enable this option to retrieve historical evidence and generate
          an AI investigation report.
        </p>

        {/* Error */}
        {error && (
          <div className="flex items-start gap-2 bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-400 text-sm">
            <AlertCircle size={18} className="shrink-0 mt-0.5" />
            {error}
          </div>
        )}

        {/* Buttons */}
        <div className="flex flex-wrap gap-3">

          <button
            onClick={analyzeIncident}
            disabled={loading}
            className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white px-6 py-3 rounded-xl font-medium transition"
          >
            {loading ? (
              <>
                <Loader2 size={18} className="animate-spin" />
                Analyzing Incident...
              </>
            ) : (
              <>
                <Sparkles size={18} />
                Analyze Incident
              </>
            )}
          </button>

          <button
            onClick={resetInvestigation}
            disabled={loading}
            className="inline-flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-300 px-5 py-3 rounded-xl transition"
          >
            Reset
          </button>

        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="bg-[#101729] border border-slate-800 rounded-2xl p-8 text-center">

          <Loader2
            className="text-indigo-400 animate-spin mx-auto mb-4"
            size={35}
          />

          <h3 className="text-white font-semibold">
            Investigating AI Incident
          </h3>

          <p className="text-slate-400 text-sm mt-2">
            Running ML classification and retrieving relevant historical incidents.
            {generateRag && " Generating the RAG investigation report may take longer."}
          </p>

        </div>
      )}

      {/* Analysis Results */}
      {result && (
        <div className="space-y-6">

          {/* Results Heading */}
          <div className="flex items-center gap-2">
            <CheckCircle2 className="text-emerald-400" size={22} />

            <h2 className="text-xl font-bold text-white">
              Investigation Results
            </h2>
          </div>

          {/* Result Summary */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">

            <div className="bg-[#101729] border border-slate-800 rounded-2xl p-5">
              <div className="flex items-center gap-2 text-slate-400 text-sm">
                <ShieldAlert size={18} />
                Predicted Risk Domain
              </div>

              <p className="text-indigo-400 text-lg font-bold mt-3">
                {result.predicted_domain || "Unavailable"}
              </p>
            </div>

            <div className="bg-[#101729] border border-slate-800 rounded-2xl p-5">
              <div className="flex items-center gap-2 text-slate-400 text-sm">
                <Target size={18} />
                Highest Confidence
              </div>

              <p className="text-emerald-400 text-2xl font-bold mt-3">
                {highestConfidence}
                {highestConfidence !== "N/A" ? "%" : ""}
              </p>
            </div>

            <div className="bg-[#101729] border border-slate-800 rounded-2xl p-5">
              <div className="flex items-center gap-2 text-slate-400 text-sm">
                <Database size={18} />
                Historical Matches
              </div>

              <p className="text-white text-2xl font-bold mt-3">
                {similarIncidents.length}
              </p>
            </div>

          </div>

          {/* ML Classification */}
          <div className="bg-[#101729] border border-slate-800 rounded-2xl p-6">

            <div className="flex items-center gap-2 mb-5">
              <BrainCircuit className="text-indigo-400" size={22} />

              <h2 className="text-xl font-semibold text-white">
                ML Risk Classification
              </h2>
            </div>

            <p className="text-sm text-slate-400 mb-2">
              Predicted Risk Domain
            </p>

            <p className="text-2xl font-bold text-indigo-400 mb-6">
              {result.predicted_domain}
            </p>

            <h3 className="text-white font-medium mb-5">
              Domain Probability Distribution
            </h3>

            <div className="space-y-5">

              {probabilities.map(([domain, probability]) => (
                <div key={domain}>

                  <div className="flex justify-between gap-3 text-sm mb-2">
                    <span className="text-slate-300">
                      {domain}
                    </span>

                    <span className="text-indigo-400 font-medium">
                      {(probability * 100).toFixed(2)}%
                    </span>
                  </div>

                  <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-indigo-500 rounded-full transition-all duration-500"
                      style={{
                        width: `${Math.max(0, Math.min(100, probability * 100))}%`
                      }}
                    />
                  </div>

                </div>
              ))}

              {probabilities.length === 0 && (
                <p className="text-slate-400 text-sm">
                  Probability information is unavailable.
                </p>
              )}

            </div>
          </div>

          {/* Similar Historical Incidents */}
          <div className="bg-[#101729] border border-slate-800 rounded-2xl p-6">

            <div className="flex items-center gap-2 mb-5">
              <Search className="text-indigo-400" size={22} />

              <h2 className="text-xl font-semibold text-white">
                Similar Historical Incidents
              </h2>
            </div>

            <p className="text-slate-400 text-sm mb-5">
              Top matching incidents retrieved from the historical AIID dataset.
            </p>

            {similarIncidents.length > 0 ? (

              <div className="space-y-4">

                {similarIncidents.map((incident, index) => (

                  <div
                    key={incident["Incident ID"] ?? index}
                    className="border border-slate-800 rounded-xl p-5 hover:border-indigo-500/50 transition"
                  >

                    <div className="flex flex-wrap justify-between gap-2 mb-3">

                      <span className="text-indigo-400 text-sm font-medium">
                        MATCH #{index + 1} | ID: {incident["Incident ID"] ?? "N/A"}
                      </span>

                      <span className="text-emerald-400 text-sm font-semibold">
                        Similarity: {
                          Number(incident["Similarity (%)"] || 0).toFixed(2)
                        }%
                      </span>

                    </div>

                    <h3 className="text-white font-semibold">
                      {incident.title || "Untitled incident"}
                    </h3>

                    <p className="text-indigo-300 text-sm mt-2">
                      {incident["Risk Domain"] || "Unknown Domain"}
                    </p>

                    <p className="text-slate-400 text-sm mt-3 leading-6">
                      {incident.description || "No description available."}
                    </p>

                  </div>

                ))}

              </div>

            ) : (

              <p className="text-slate-400">
                No similar historical incidents found.
              </p>

            )}

          </div>

          {/* RAG Evidence */}
          {generateRag && (
            <div className="bg-[#101729] border border-slate-800 rounded-2xl p-6">

              <div className="flex items-center gap-2 mb-5">
                <Database className="text-purple-400" size={22} />

                <h2 className="text-xl font-semibold text-white">
                  RAG Retrieved Evidence
                </h2>
              </div>

              {ragEvidence.length > 0 ? (

                <div className="space-y-4">

                  {ragEvidence.map((item, index) => (

                    <div
                      key={index}
                      className="border border-slate-800 rounded-xl p-4"
                    >

                      <p className="text-purple-300 text-xs mb-2">
                        EVIDENCE #{index + 1}
                      </p>

                      <h3 className="text-white font-medium">
                        {item.Title || item.title || "Untitled incident"}
                      </h3>

                      <p className="text-slate-400 text-sm mt-2">
                        Risk Domain: {item["Risk Domain"] || "Unknown"}
                      </p>

                      {(item.Description || item.description) && (
                        <p className="text-slate-400 text-sm mt-3 leading-6">
                          {item.Description || item.description}
                        </p>
                      )}

                    </div>

                  ))}

                </div>

              ) : (

                <p className="text-slate-400 text-sm">
                  No RAG evidence was returned for this investigation.
                </p>

              )}

            </div>
          )}

          {/* AI Investigation Report */}
          {result.investigation_report && (

            <div className="bg-[#101729] border border-slate-800 rounded-2xl p-6">

              <div className="flex items-center gap-2 mb-6">
                <FileText className="text-indigo-400" size={22} />

                <h2 className="text-xl font-semibold text-white">
                  AI Investigation Report
                </h2>
              </div>

              <div
                className="
                  text-sm text-slate-300 leading-7 space-y-4
                  [&_h1]:text-2xl [&_h1]:font-bold [&_h1]:text-indigo-400
                  [&_h2]:text-xl [&_h2]:font-semibold [&_h2]:text-indigo-300
                  [&_h3]:text-lg [&_h3]:font-semibold [&_h3]:text-white
                  [&_strong]:text-white
                  [&_ul]:list-disc [&_ul]:pl-6
                  [&_ol]:list-decimal [&_ol]:pl-6
                  [&_p]:mb-3
                  [&_li]:mb-2
                "
              >

                <ReactMarkdown>
                  {
                    typeof result.investigation_report === "string"
                      ? result.investigation_report
                      : JSON.stringify(
                          result.investigation_report,
                          null,
                          2
                        )
                  }
                </ReactMarkdown>

              </div>

            </div>

          )}

          {/* Investigation Metadata */}
          <div className="flex items-center gap-2 text-xs text-slate-500">
            <Activity size={14} />
            Investigation ID: {result.id || "N/A"}
          </div>

        </div>
      )}

    </div>
  );
}
