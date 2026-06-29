import { useState, useEffect } from "react";
import Plot from "react-plotly.js";
import { getEDA } from "../services/api";
import { BarChart2, Loader2 } from "lucide-react";

const CHART_FILTERS = ["all", "histogram", "boxplot", "heatmap", "bar", "scatter", "missing"];

export default function EDACharts({ filename }) {
  const [eda, setEda] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [error, setError] = useState(null);

  useEffect(() => {
    getEDA(filename)
      .then((data) => {
        setEda(data);
        setLoading(false);
      })
      .catch((err) => {
        setError("Failed to generate EDA. Please try again.");
        setLoading(false);
      });
  }, [filename]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-24 gap-4">
        <Loader2 className="w-10 h-10 animate-spin" style={{ color: "#38bdf8" }} />
        <p style={{ color: "#64748b" }}>Generating charts and statistics...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center py-20">
        <p style={{ color: "#f87171" }}>{error}</p>
      </div>
    );
  }

  const filteredCharts = filter === "all"
    ? eda.charts
    : eda.charts.filter((c) => c.type === filter);

  const statCols = Object.keys(eda.stats);

  return (
    <div className="max-w-6xl mx-auto px-6 py-10">

      {/* Header */}
      <div className="flex items-center gap-3 mb-8">
        <div className="w-2 h-8 rounded-full" style={{ backgroundColor: "#38bdf8" }} />
        <div>
          <h2 className="text-2xl font-bold">Exploratory Data Analysis</h2>
          <p className="text-sm mt-0.5" style={{ color: "#64748b" }}>
            {eda.total_charts} charts · {eda.numeric_columns.length} numeric · {eda.categorical_columns.length} categorical columns
          </p>
        </div>
      </div>

      {/* Stats Summary */}
      {statCols.length > 0 && (
        <div className="rounded-xl border mb-8 overflow-x-auto" style={{ backgroundColor: "#13161e", borderColor: "#1e2330" }}>
          <div className="p-5" style={{ borderBottom: "1px solid #1e2330" }}>
            <p className="font-semibold" style={{ color: "#38bdf8" }}>Statistical Summary</p>
          </div>
          <table className="w-full text-sm">
            <thead>
              <tr style={{ borderBottom: "1px solid #1e2330" }}>
                <th className="text-left px-5 py-3" style={{ color: "#64748b" }}>Metric</th>
                {statCols.map((col) => (
                  <th key={col} className="text-left px-5 py-3" style={{ color: "#64748b" }}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {["count", "mean", "std", "min", "25%", "50%", "75%", "max"].map((metric) => (
                <tr key={metric} style={{ borderBottom: "1px solid #1e2330" }}>
                  <td className="px-5 py-3 font-medium" style={{ color: "#38bdf8" }}>{metric}</td>
                  {statCols.map((col) => (
                    <td key={col} className="px-5 py-3" style={{ color: "#94a3b8" }}>
                      {eda.stats[col][metric] !== undefined ? eda.stats[col][metric] : "—"}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Filter Tabs */}
      <div className="flex gap-2 mb-6 flex-wrap">
        {CHART_FILTERS.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className="px-4 py-1.5 rounded-full text-sm font-medium capitalize transition-all"
            style={{
              backgroundColor: filter === f ? "#38bdf8" : "#13161e",
              color: filter === f ? "#0d0f14" : "#64748b",
              border: "1px solid",
              borderColor: filter === f ? "#38bdf8" : "#1e2330",
            }}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Charts Grid */}
      {filteredCharts.length === 0 ? (
        <div className="text-center py-16" style={{ color: "#64748b" }}>
          <BarChart2 className="w-10 h-10 mx-auto mb-3 opacity-40" />
          <p>No charts of this type for your dataset.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredCharts.map((chart) => (
            <div
              key={chart.id}
              className="rounded-xl border overflow-hidden"
              style={{ backgroundColor: "#13161e", borderColor: "#1e2330" }}
            >
              <Plot
                data={chart.data.data}
                layout={{
                  ...chart.data.layout,
                  autosize: true,
                  height: 320,
                }}
                config={{ displayModeBar: false, responsive: true }}
                style={{ width: "100%" }}
                useResizeHandler
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}