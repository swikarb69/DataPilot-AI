import { Database, AlertCircle, Copy, Layers } from "lucide-react";

function StatCard({ icon: Icon, label, value, accent }) {
  return (
    <div className="bg-brand-surface border border-brand-border rounded-xl p-5 flex items-center gap-4">
      <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${accent || "bg-brand-accent/10"}`}>
        <Icon className="w-5 h-5 text-brand-accent" />
      </div>
      <div>
        <p className="text-brand-muted text-xs uppercase tracking-wider">{label}</p>
        <p className="text-xl font-bold mt-0.5">{value}</p>
      </div>
    </div>
  );
}

export default function DataSummary({ data }) {
  const { filename, summary } = data;
  const totalMissing = Object.values(summary.missing_values).reduce((a, b) => a + b, 0);

  return (
    <div className="max-w-5xl mx-auto px-6 py-10">
      <div className="flex items-center gap-3 mb-8">
        <div className="w-2 h-8 bg-brand-accent rounded-full" />
        <div>
          <h2 className="text-2xl font-bold">{filename}</h2>
          <p className="text-brand-muted text-sm">{summary.memory_usage_kb} KB in memory</p>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
        <StatCard icon={Database} label="Rows" value={summary.rows.toLocaleString()} />
        <StatCard icon={Layers} label="Columns" value={summary.columns} />
        <StatCard icon={AlertCircle} label="Missing Values" value={totalMissing} />
        <StatCard icon={Copy} label="Duplicates" value={summary.duplicates} />
      </div>

      <div className="bg-brand-surface border border-brand-border rounded-xl p-6 mb-6">
        <h3 className="font-semibold mb-4 text-brand-accent">Column Overview</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-brand-muted border-b border-brand-border">
                <th className="text-left pb-3 pr-6">Column</th>
                <th className="text-left pb-3 pr-6">Type</th>
                <th className="text-left pb-3 pr-6">Missing</th>
                <th className="text-left pb-3">Missing %</th>
              </tr>
            </thead>
            <tbody>
              {summary.column_names.map((col) => (
                <tr key={col} className="border-b border-brand-border/40 hover:bg-white/[0.02]">
                  <td className="py-2.5 pr-6 font-medium">{col}</td>
                  <td className="py-2.5 pr-6">
                    <span className="text-xs px-2 py-1 rounded-md bg-brand-accent/10 text-brand-accent">
                      {summary.dtypes[col]}
                    </span>
                  </td>
                  <td className="py-2.5 pr-6 text-brand-muted">{summary.missing_values[col]}</td>
                  <td className="py-2.5 text-brand-muted">{summary.missing_percent[col]}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="bg-brand-surface border border-brand-border rounded-xl p-6">
        <h3 className="font-semibold mb-4 text-brand-accent">Data Preview</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-brand-muted border-b border-brand-border">
                {summary.column_names.map((col) => (
                  <th key={col} className="text-left pb-3 pr-6 whitespace-nowrap">{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {summary.preview.map((row, i) => (
                <tr key={i} className="border-b border-brand-border/40 hover:bg-white/[0.02]">
                  {summary.column_names.map((col) => (
                    <td key={col} className="py-2.5 pr-6 text-brand-muted whitespace-nowrap">
                      {String(row[col] ?? "")}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}