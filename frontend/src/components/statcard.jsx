
export default function StatCard({
  title,
  value,
  description,
  icon: Icon,
  color
}) {
  return (
    <div className="bg-[#101729] border border-slate-800 rounded-2xl p-5 hover:border-indigo-500/40 transition-all duration-300">

      {/* Card Header */}
      <div className="flex items-center justify-between mb-5">
        <p className="text-slate-400 text-sm font-medium">
          {title}
        </p>

        <div className={`p-3 rounded-xl ${color}`}>
          <Icon size={21} />
        </div>
      </div>

      {/* Metric */}
      <h2 className="text-white text-3xl font-bold tracking-tight">
        {value}
      </h2>

      {/* Description */}
      <p className="text-slate-500 text-xs mt-3">
        {description}
      </p>

    </div>
  );
}
