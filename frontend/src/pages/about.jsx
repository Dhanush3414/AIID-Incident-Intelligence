
import {
  BrainCircuit,
  Database,
  ShieldCheck,
  Target,
  Code2,
  Workflow,
  Search,
  FileText,
  Cpu,
  Layers3
} from "lucide-react";

const technologies = [
  {
    name: "Python",
    category: "Programming",
    icon: Code2
  },
  {
    name: "Scikit-learn",
    category: "Machine Learning",
    icon: BrainCircuit
  },
  {
    name: "TF-IDF",
    category: "Text Processing",
    icon: FileText
  },
  {
    name: "FAISS",
    category: "Vector Search",
    icon: Database
  },
  {
    name: "Llama 3.2",
    category: "LLM",
    icon: Cpu
  },
  {
    name: "Streamlit",
    category: "Original Interface",
    icon: Layers3
  },
  {
    name: "React",
    category: "Frontend",
    icon: Code2
  },
  {
    name: "FastAPI",
    category: "Backend API",
    icon: Workflow
  }
];

const objectives = [
  "Identify potential risks associated with AI systems.",
  "Classify incidents into relevant AI risk domains.",
  "Retrieve similar historical incidents from the AIID database.",
  "Generate investigation insights using retrieval-augmented generation.",
  "Provide recommendations to support incident analysis."
];

const workflow = [
  {
    number: "01",
    title: "Incident Input",
    description: "Collect an AI incident description from the user."
  },
  {
    number: "02",
    title: "ML Classification",
    description: "Predict the incident's risk domain using the trained classifier."
  },
  {
    number: "03",
    title: "Similarity Search",
    description: "Find related incidents using text and vector similarity."
  },
  {
    number: "04",
    title: "RAG Investigation",
    description: "Retrieve relevant evidence and generate AI-powered insights."
  },
  {
    number: "05",
    title: "Final Report",
    description: "Present findings, root cause analysis and recommendations."
  }
];

export default function About() {
  return (
    <div className="space-y-8">

      {/* Heading */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          <BrainCircuit size={20} className="text-indigo-400" />
          <span className="text-indigo-400 text-sm font-medium">
            PROJECT INFORMATION
          </span>
        </div>

        <h1 className="text-3xl font-bold text-white">
          About AIID Incident Intelligence
        </h1>

        <p className="text-slate-400 mt-2">
          Understanding AI incidents through machine learning,
          historical evidence and generative AI.
        </p>
      </div>

      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-br from-indigo-950 via-[#101729] to-purple-950 border border-indigo-500/20 rounded-2xl p-8">

        <div className="relative z-10 max-w-3xl">
          <div className="inline-flex items-center gap-2 bg-indigo-500/20 text-indigo-300 px-3 py-2 rounded-full text-xs mb-5">
            <ShieldCheck size={15} />
            AI-POWERED INCIDENT INTELLIGENCE
          </div>

          <h2 className="text-white text-3xl font-bold leading-tight">
            AI Incident Investigator
          </h2>

          <p className="text-slate-300 leading-relaxed mt-4">
            An intelligent incident investigation platform designed
            to analyze AI-related incidents using machine learning,
            similarity matching and Retrieval-Augmented Generation.
            It helps identify risk domains, discover historical cases
            and generate structured investigation insights.
          </p>

          <div className="flex flex-wrap gap-3 mt-6">
            <span className="bg-white/10 text-slate-200 px-4 py-2 rounded-lg text-sm">
              Machine Learning
            </span>
            <span className="bg-white/10 text-slate-200 px-4 py-2 rounded-lg text-sm">
              RAG
            </span>
            <span className="bg-white/10 text-slate-200 px-4 py-2 rounded-lg text-sm">
              Generative AI
            </span>
          </div>
        </div>

        <BrainCircuit
          size={190}
          className="absolute -right-8 -bottom-10 text-indigo-400/10"
        />
      </div>

      {/* Project Overview */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">

        <div className="bg-[#101729] border border-slate-800 rounded-2xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-indigo-500/20 p-3 rounded-xl">
              <Target className="text-indigo-400" size={23} />
            </div>
            <h2 className="text-white text-lg font-semibold">
              Project Objective
            </h2>
          </div>

          <p className="text-slate-400 text-sm leading-relaxed">
            The primary objective is to develop an intelligent
            system that assists in investigating AI-related incidents
            by combining predictive machine learning models with
            historical incident retrieval and LLM-based analysis.
          </p>
        </div>

        <div className="bg-[#101729] border border-slate-800 rounded-2xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-emerald-500/20 p-3 rounded-xl">
              <Database className="text-emerald-400" size={23} />
            </div>
            <h2 className="text-white text-lg font-semibold">
              Dataset Overview
            </h2>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-slate-800/50 rounded-xl p-4">
              <p className="text-slate-400 text-sm">Total Records</p>
              <h3 className="text-white text-2xl font-bold mt-2">
                1,749
              </h3>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-4">
              <p className="text-slate-400 text-sm">Data Columns</p>
              <h3 className="text-white text-2xl font-bold mt-2">
                81
              </h3>
            </div>
          </div>

          <p className="text-slate-500 text-xs mt-4">
            Based on the processed AI Incident Database dataset.
          </p>
        </div>

      </div>

      {/* Objectives */}
      <div className="bg-[#101729] border border-slate-800 rounded-2xl p-6">

        <h2 className="text-white text-lg font-semibold mb-5">
          Key Project Objectives
        </h2>

        <div className="space-y-4">
          {objectives.map((objective, index) => (
            <div key={index} className="flex items-start gap-3">
              <div className="w-7 h-7 shrink-0 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-sm font-semibold">
                {index + 1}
              </div>

              <p className="text-slate-300 text-sm pt-1">
                {objective}
              </p>
            </div>
          ))}
        </div>

      </div>

      {/* Technology Stack */}
      <div className="bg-[#101729] border border-slate-800 rounded-2xl p-6">

        <h2 className="text-white text-lg font-semibold">
          Technology Stack
        </h2>

        <p className="text-slate-400 text-sm mt-1 mb-6">
          Frameworks, libraries and tools used in the project.
        </p>

        <div className="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-4 gap-4">
          {technologies.map((tech) => {
            const Icon = tech.icon;

            return (
              <div
                key={tech.name}
                className="bg-slate-800/40 border border-slate-700/60 rounded-xl p-4 hover:border-indigo-500/50 transition"
              >
                <Icon size={23} className="text-indigo-400 mb-3" />

                <h3 className="text-white font-semibold text-sm">
                  {tech.name}
                </h3>

                <p className="text-slate-500 text-xs mt-1">
                  {tech.category}
                </p>
              </div>
            );
          })}
        </div>

      </div>

      {/* System Workflow */}
      <div className="bg-[#101729] border border-slate-800 rounded-2xl p-6">

        <div className="flex items-center gap-3 mb-6">
          <Workflow className="text-purple-400" size={24} />
          <h2 className="text-white text-lg font-semibold">
            System Architecture Workflow
          </h2>
        </div>

        <div className="space-y-4">
          {workflow.map((step, index) => (
            <div
              key={step.number}
              className="flex items-start gap-4"
            >
              <div className="w-11 h-11 shrink-0 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold">
                {step.number}
              </div>

              <div className="flex-1 border-b border-slate-800 pb-4">
                <h3 className="text-white font-medium">
                  {step.title}
                </h3>

                <p className="text-slate-400 text-sm mt-1">
                  {step.description}
                </p>
              </div>
            </div>
          ))}
        </div>

      </div>

      {/* Footer */}
      <div className="text-center py-5 border-t border-slate-800">
        <p className="text-slate-400 text-sm">
          AIID Incident Intelligence
        </p>
        <p className="text-slate-600 text-xs mt-2">
          Machine Learning • Retrieval-Augmented Generation • Generative AI
        </p>
      </div>

    </div>
  );
}
