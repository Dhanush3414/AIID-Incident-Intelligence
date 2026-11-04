
import { useEffect, useState } from "react";
import {
  FileText,
  BrainCircuit,
  Database,
  ShieldCheck,
  RefreshCw,
  AlertCircle,
  Clock,
  Search,
  Sparkles,
  ChevronRight,
  Download,
} from "lucide-react";

import ReactMarkdown from "react-markdown";
import jsPDF from "jspdf";
import API from "../services/api";

export default function InvestigationReport() {
  const [reports, setReports] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Fetch all saved reports
  const fetchReports = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await API.get("/api/reports");
      const reportList = response.data.reports || [];

      setReports(reportList);

      setSelectedReport((current) => {
        if (!reportList.length) return null;

        return (
          reportList.find((report) => report.id === current?.id) ||
          reportList[0]
        );
      });
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to load investigation reports."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  // Report data
  const probabilities = selectedReport?.probabilities || {};

  const probabilityEntries = Object.entries(probabilities).sort(
    (a, b) => b[1] - a[1]
  );

  const similarIncidents = selectedReport?.similar_incidents || [];
  const ragEvidence = selectedReport?.rag_evidence || [];

  const reportText = selectedReport?.investigation_report;

  // Format date
  const formatDate = (date) => {
    if (!date) return "Date unavailable";

    return new Date(date).toLocaleString();
  };

  // Format probability
  const percentage = (value) =>
    `${(Number(value) * 100).toFixed(2)}%`;

  // Download selected investigation as PDF
  const downloadPDF = () => {
    if (!selectedReport) return;

    const doc = new jsPDF();

    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();

    const margin = 15;
    const maxWidth = pageWidth - margin * 2;

    let y = 20;

    // Add text with automatic page breaks
    const addText = (text, size = 10, bold = false) => {
      doc.setFont("helvetica", bold ? "bold" : "normal");
      doc.setFontSize(size);

      const lines = doc.splitTextToSize(
        String(text ?? "N/A"),
        maxWidth
      );

      const lineHeight = size * 0.48;
      const requiredHeight = lines.length * lineHeight + 4;

      if (y + requiredHeight > pageHeight - 15) {
        doc.addPage();
        y = 20;
      }

      doc.text(lines, margin, y);
      y += requiredHeight;
    };

    const addSection = (heading) => {
      y += 4;
      addText(heading, 13, true);
    };

    // Report title
    doc.setTextColor(45, 55, 110);
    addText("AI INCIDENT INTELLIGENCE", 18, true);

    doc.setTextColor(30, 30, 30);
    addText("AI Investigation Report", 15, true);

    addText(
      `Generated: ${formatDate(selectedReport.created_at)}`
    );

    y += 5;

    // 1. Incident details
    addSection("1. INCIDENT DETAILS");

    addText(`Title: ${selectedReport.title}`, 11, true);

    addText(
      `Description: ${selectedReport.description}`
    );

    addText(
      `Predicted Risk Domain: ${selectedReport.predicted_domain}`
    );

    // 2. ML classification
    addSection("2. ML RISK CLASSIFICATION");

    probabilityEntries.forEach(([domain, value]) => {
      addText(`${domain}: ${percentage(value)}`);
    });

    // 3. Similar historical incidents
    addSection("3. SIMILAR HISTORICAL INCIDENTS");

    if (similarIncidents.length === 0) {
      addText("No similar historical incidents found.");
    }

    similarIncidents.forEach((incident, index) => {
      addText(
        `${index + 1}. ${
          incident.title ||
          incident.Title ||
          "Untitled Incident"
        }`,
        10,
        true
      );

      addText(
        `Incident ID: ${incident["Incident ID"] || "Unknown"}`
      );

      addText(
        `Risk Domain: ${incident["Risk Domain"] || "Unknown"}`
      );

      addText(
        `Similarity: ${
          incident["Similarity (%)"] != null
            ? Number(incident["Similarity (%)"]).toFixed(2) + "%"
            : "N/A"
        }`
      );

      addText(
        incident.description ||
        incident.Description ||
        "Description unavailable."
      );
    });

    // 4. RAG evidence
    addSection("4. RAG RETRIEVED HISTORICAL EVIDENCE");

    if (ragEvidence.length === 0) {
      addText("No RAG evidence available.");
    }

    ragEvidence.forEach((evidence, index) => {
      addText(
        `${index + 1}. ${
          evidence.Title ||
          evidence.title ||
          "Untitled Incident"
        }`,
        10,
        true
      );

      addText(
        `Incident ID: ${evidence["Incident ID"] || "Unknown"}`
      );

      addText(
        `Risk Domain: ${evidence["Risk Domain"] || "Unknown"}`
      );

      addText(
        `Similarity Score: ${
          evidence["Similarity Score"] ??
          evidence["Similarity (%)"] ??
          "N/A"
        }`
      );
    });

    // 5. AI-generated report
    addSection("5. AI-GENERATED INVESTIGATION REPORT");

    const finalReport =
      typeof reportText === "string"
        ? reportText
        : JSON.stringify(reportText || "Report not generated", null, 2);

    addText(finalReport);

    // Footer
    y += 5;
    addText("End of Investigation Report", 10, true);

    // Save PDF
    const filename = `AIID_Report_${selectedReport.id}.pdf`;

    doc.save(filename);
  };

  return (
    <div className="space-y-6 text-slate-200">

      {/* PAGE HEADING */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          <FileText className="text-indigo-400" size={20} />

          <span className="text-indigo-400 text-sm font-medium">
            INTELLIGENCE REPORTS
          </span>
        </div>

        <h1 className="text-3xl font-bold text-white">
          AI Investigation Report
        </h1>

        <p className="text-slate-400 mt-2">
          Review ML classification, historical evidence and AI-generated
          investigation findings.
        </p>
      </div>

      {/* LOADING */}
      {loading && (
        <div className="bg-[#101729] border border-slate-800 rounded-xl p-8 text-center">
          <RefreshCw className="animate-spin mx-auto mb-3 text-indigo-400" />

          <p className="text-slate-400">
            Loading investigation reports...
          </p>
        </div>
      )}

      {/* ERROR */}
      {!loading && error && (
        <div className="bg-red-950/30 border border-red-800 rounded-xl p-4 flex gap-3">
          <AlertCircle className="text-red-400 shrink-0" />

          <p className="text-red-300">{error}</p>
        </div>
      )}

      {!loading && !error && (
        <>
          {/* STATISTICS */}
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">

            <StatCard
              icon={<FileText className="text-indigo-400" />}
              label="Saved Reports"
              value={reports.length}
              description="Total investigations"
            />

            <StatCard
              icon={<BrainCircuit className="text-purple-400" />}
              label="ML Analysis"
              value={selectedReport ? "Completed" : "Pending"}
              description="Risk classification module"
            />

            <StatCard
              icon={<Database className="text-emerald-400" />}
              label="RAG Evidence"
              value={selectedReport ? ragEvidence.length : 0}
              description="Retrieved historical records"
            />

            <StatCard
              icon={<ShieldCheck className="text-cyan-400" />}
              label="Report Status"
              value={
                selectedReport?.investigation_report
                  ? "Generated"
                  : "Pending"
              }
              description="RAG investigation report"
            />

          </div>

          {/* NO REPORTS */}
          {reports.length === 0 && (
            <div className="bg-[#101729] border border-slate-800 rounded-2xl p-12 text-center">

              <FileText
                size={42}
                className="mx-auto text-indigo-400 mb-4"
              />

              <h2 className="text-xl font-bold text-white">
                No Investigation Reports Yet
              </h2>

              <p className="text-slate-400 mt-3">
                Submit an incident through the Incident Investigation page.
                Your ML classification, similar incidents and RAG report
                will appear here.
              </p>

            </div>
          )}

          {/* REPORT HISTORY */}
          {reports.length > 0 && (
            <div className="grid grid-cols-1 xl:grid-cols-4 gap-5">

              {/* HISTORY SIDEBAR */}
              <div className="xl:col-span-1 bg-[#101729] border border-slate-800 rounded-2xl p-4 h-fit">

                <div className="flex items-center justify-between mb-4">

                  <h2 className="font-semibold text-white">
                    Report History
                  </h2>

                  <button
                    onClick={fetchReports}
                    disabled={loading}
                    className="text-indigo-400 hover:text-indigo-300"
                    title="Refresh reports"
                  >
                    <RefreshCw size={17} />
                  </button>

                </div>

                <div className="space-y-2">

                  {reports.map((report, index) => (
                    <button
                      key={report.id || index}
                      onClick={() => setSelectedReport(report)}
                      className={`w-full text-left rounded-xl p-3 border transition ${
                        selectedReport?.id === report.id
                          ? "bg-indigo-600/20 border-indigo-500"
                          : "bg-[#0b1020] border-slate-800 hover:border-slate-600"
                      }`}
                    >

                      <div className="flex items-start justify-between gap-2">

                        <FileText
                          size={17}
                          className="text-indigo-400 shrink-0 mt-1"
                        />

                        <ChevronRight
                          size={16}
                          className="text-slate-500 shrink-0"
                        />

                      </div>

                      <p className="text-sm font-medium text-white mt-2 line-clamp-2">
                        {report.title || "Untitled Investigation"}
                      </p>

                      <p className="text-xs text-slate-500 mt-2">
                        {formatDate(report.created_at)}
                      </p>

                      {index === 0 && (
                        <span className="inline-block mt-2 text-xs text-emerald-400">
                          Latest report
                        </span>
                      )}

                    </button>
                  ))}

                </div>
              </div>

              {/* SELECTED REPORT */}
              <div className="xl:col-span-3 space-y-5">

                {selectedReport && (
                  <>

                    {/* INCIDENT DETAILS */}
                    <section className="bg-[#101729] border border-slate-800 rounded-2xl p-5">

                      <div className="flex items-center justify-between flex-wrap gap-3 mb-4">

                        <div className="flex items-center gap-2">

                          <ShieldCheck
                            className="text-emerald-400"
                            size={20}
                          />

                          <h2 className="text-lg font-bold text-white">
                            Investigation Details
                          </h2>

                        </div>

                        {/* DOWNLOAD PDF BUTTON */}
                        <button
                          onClick={downloadPDF}
                          className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition"
                        >
                          <Download size={16} />
                          Download PDF
                        </button>

                      </div>

                      <p className="text-xs text-slate-500 mb-1">
                        Incident Title
                      </p>

                      <h3 className="text-xl font-bold text-white mb-4">
                        {selectedReport.title}
                      </h3>

                      <p className="text-xs text-slate-500 mb-1">
                        Incident Description
                      </p>

                      <p className="text-slate-300 leading-7">
                        {selectedReport.description}
                      </p>

                      <div className="mt-5">

                        <p className="text-xs text-slate-500 mb-2">
                          Predicted Risk Domain
                        </p>

                        <span className="inline-block bg-indigo-500/15 text-indigo-300 border border-indigo-500/30 px-3 py-2 rounded-lg text-sm font-medium">
                          {selectedReport.predicted_domain || "Unknown"}
                        </span>

                      </div>

                    </section>

                    {/* ML PROBABILITIES */}
                    <section className="bg-[#101729] border border-slate-800 rounded-2xl p-5">

                      <div className="flex items-center gap-2 mb-5">

                        <BrainCircuit
                          className="text-purple-400"
                          size={20}
                        />

                        <h2 className="text-lg font-bold text-white">
                          ML Risk Classification Probabilities
                        </h2>

                      </div>

                      {probabilityEntries.length > 0 ? (

                        <div className="space-y-4">

                          {probabilityEntries.map(([domain, value]) => (
                            <div key={domain}>

                              <div className="flex justify-between gap-3 text-sm mb-2">

                                <span className="text-slate-300">
                                  {domain}
                                </span>

                                <span className="text-indigo-400 font-medium">
                                  {percentage(value)}
                                </span>

                              </div>

                              <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">

                                <div
                                  className="bg-indigo-500 h-2 rounded-full transition-all"
                                  style={{
                                    width: `${Math.min(
                                      Math.max(Number(value) * 100, 0),
                                      100
                                    )}%`,
                                  }}
                                />

                              </div>

                            </div>
                          ))}

                        </div>

                      ) : (
                        <p className="text-slate-500">
                          No classification probabilities available.
                        </p>
                      )}

                    </section>

                    {/* SIMILAR HISTORICAL INCIDENTS */}
                    <section className="bg-[#101729] border border-slate-800 rounded-2xl p-5">

                      <div className="flex items-center gap-2 mb-4">

                        <Search className="text-cyan-400" size={20} />

                        <h2 className="text-lg font-bold text-white">
                          Similar Historical Incidents
                        </h2>

                      </div>

                      {similarIncidents.length > 0 ? (

                        <div className="space-y-3">

                          {similarIncidents.map((incident, index) => (
                            <div
                              key={incident["Incident ID"] || index}
                              className="bg-[#0b1020] border border-slate-800 rounded-xl p-4"
                            >

                              <div className="flex justify-between gap-3">

                                <h3 className="font-semibold text-white">
                                  {incident.title ||
                                    incident.Title ||
                                    "Untitled Incident"}
                                </h3>

                                <span className="text-emerald-400 text-sm shrink-0">
                                  {incident["Similarity (%)"] != null
                                    ? `${Number(
                                        incident["Similarity (%)"]
                                      ).toFixed(2)}%`
                                    : ""}
                                </span>

                              </div>

                              <p className="text-sm text-slate-400 mt-2">
                                {incident.description ||
                                  incident.Description ||
                                  "No description available."}
                              </p>

                              <p className="text-xs text-indigo-400 mt-3">
                                Incident ID:{" "}
                                {incident["Incident ID"] || "Unknown"}
                                {" | "}
                                {incident["Risk Domain"] ||
                                  incident.risk_domain ||
                                  "Unknown"}
                              </p>

                            </div>
                          ))}

                        </div>

                      ) : (
                        <p className="text-slate-500">
                          No similar incidents found.
                        </p>
                      )}

                    </section>

                    {/* RAG EVIDENCE */}
                    <section className="bg-[#101729] border border-slate-800 rounded-2xl p-5">

                      <div className="flex items-center gap-2 mb-4">

                        <Database
                          className="text-emerald-400"
                          size={20}
                        />

                        <h2 className="text-lg font-bold text-white">
                          RAG Retrieved Historical Evidence
                        </h2>

                      </div>

                      {ragEvidence.length > 0 ? (

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">

                          {ragEvidence.map((evidence, index) => (
                            <div
                              key={evidence["Incident ID"] || index}
                              className="bg-[#0b1020] border border-slate-800 rounded-xl p-4"
                            >

                              <p className="text-xs text-emerald-400 mb-2">
                                Historical Incident #
                                {evidence["Incident ID"] || "Unknown"}
                              </p>

                              <h3 className="font-semibold text-white">
                                {evidence.Title ||
                                  evidence.title ||
                                  "Untitled Incident"}
                              </h3>

                              <p className="text-sm text-slate-400 mt-2">
                                Risk Domain:{" "}
                                {evidence["Risk Domain"] ||
                                  evidence.risk_domain ||
                                  "Unknown"}
                              </p>

                              <p className="text-sm text-indigo-400 mt-2">
                                Similarity Score:{" "}
                                {evidence["Similarity Score"] != null
                                  ? Number(
                                      evidence["Similarity Score"]
                                    ).toFixed(4)
                                  : evidence["Similarity (%)"] != null
                                  ? Number(
                                      evidence["Similarity (%)"]
                                    ).toFixed(2) + "%"
                                  : "N/A"}
                              </p>

                            </div>
                          ))}

                        </div>

                      ) : (
                        <p className="text-slate-500">
                          No RAG evidence available for this report.
                        </p>
                      )}

                    </section>

                    {/* AI INVESTIGATION REPORT */}
                    <section className="bg-[#101729] border border-slate-800 rounded-2xl p-5">

                      <div className="flex items-center gap-2 mb-4">

                        <Sparkles
                          className="text-indigo-400"
                          size={21}
                        />

                        <div>

                          <h2 className="text-lg font-bold text-white">
                            AI Investigation Report
                          </h2>

                          <p className="text-xs text-slate-400">
                            Generated using Retrieval-Augmented Generation
                            (RAG).
                          </p>

                        </div>

                      </div>

                      {reportText ? (

                        <div className="prose prose-invert prose-sm max-w-none text-slate-300 leading-7">

                          <ReactMarkdown>
                            {typeof reportText === "string"
                              ? reportText
                              : JSON.stringify(reportText, null, 2)}
                          </ReactMarkdown>

                        </div>

                      ) : (
                        <p className="text-slate-500">
                          An AI-generated investigation report is not
                          available for this investigation.
                        </p>
                      )}

                    </section>

                  </>
                )}

              </div>
            </div>
          )}
        </>
      )}

    </div>
  );
}

// STATISTICS CARD
function StatCard({ icon, label, value, description }) {
  return (
    <div className="bg-[#101729] border border-slate-800 rounded-2xl p-4">

      <div className="mb-2">
        {icon}
      </div>

      <p className="text-sm text-slate-400">
        {label}
      </p>

      <h2 className="text-2xl font-bold text-white mt-1">
        {value}
      </h2>

      <p className="text-xs text-slate-500 mt-1">
        {description}
      </p>

    </div>
  );
}
