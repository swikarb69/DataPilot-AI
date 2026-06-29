import { useState, useEffect } from "react";
import { getInsights, generateReport } from "../services/api";
import { Loader2, TrendingUp, AlertTriangle, Minus, Lightbulb, FileText, Download } from "lucide-react";

const TYPE_CONFIG = {
  positive: { icon: TrendingUp, color: "#4ade80", bg: "#4ade8010" },
  warning: { icon: AlertTriangle, color: "#fb923c", bg: "#fb923c10" },
  neutral: { icon: Minus, color: "#38bdf8", bg: "#38bdf810" },
};

export default function AIInsights({ filename }) {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    getInsights(filename)
      .then((data) => {
        setInsights(data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to generate insights. Check your Gemini API key.");
        setLoading(false);
      });
  }, [filename]);

  const handleReport = async () => {
    setGenerating(true);
    await generateReport(filename);
    setGenerating(false);
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-24 gap-4">
        <Loader2 className="w-10 h-10 animate-spin" style={{ color: "#38bdf8" }} />
        <p style={{ color: "#64748b" }}>Gemini is analyzing your data...</p>
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

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">

      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <div className="w-2 h-8 rounded-full" style={{ backgroundColor: "#38bdf8" }} />
          <div>
            <h2 className="text-2xl font-bold">AI Insights</h2>
            <p className="text-sm mt-0.5" style={{ color: "#64748b" }}>Powered by Gemini</p>
          </div>
        </div>
        <button
          onClick={handleReport}
          disabled={generating}
          className="flex items-center gap-2 px-6 py-2.5 rounded-xl font-semibold text-sm transition-opacity"
          style={{ backgroundColor: "#38bdf8", color: "#0d0f14", opacity: generating ? 0.7 : 1 }}
        >
          <Download className="w-4 h-4" />
          {generating ? "Generating..." : "Download PDF Report"}
        </button>
      </div>

      {/* Executive Summary */}
      <div className="rounded-xl border p-6 mb-6" style={{ backgroundColor: "#13161e", borderColor: "#1e2330" }}>
        <div className="flex items-center gap-2 mb-3">
          <FileText className="w-4 h-4" style={{ color: "#38bdf8" }} />
          <p className="font-semibold text-sm uppercase tracking-wider" style={{ color: "#38bdf8" }}>Executive Summary</p>
        </div>
        <p className="leading-relaxed" style={{ color: "#cbd5e1" }}>{insights.summary}</p>
      </div>

      {/* Insights Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {insights.insights.map((insight, i) => {
          const config = TYPE_CONFIG[insight.type] || TYPE_CONFIG.neutral;
          const Icon = config.icon;
          return (
            <div
              key={i}
              className="rounded-xl border p-5"
              style={{ backgroundColor: "#13161e", borderColor: "#1e2330" }}
            >
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5" style={{ backgroundColor: config.bg }}>
                  <Icon className="w-4 h-4" style={{ color: config.color }} />
                </div>
                <div>
                  <p className="font-semibold mb-1" style={{ color: config.color }}>{insight.title}</p>
                  <p className="text-sm leading-relaxed" style={{ color: "#94a3b8" }}>{insight.description}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Recommendations */}
      <div className="rounded-xl border p-6 mb-8" style={{ backgroundColor: "#13161e", borderColor: "#1e2330" }}>
        <div className="flex items-center gap-2 mb-4">
          <Lightbulb className="w-4 h-4" style={{ color: "#38bdf8" }} />
          <p className="font-semibold text-sm uppercase tracking-wider" style={{ color: "#38bdf8" }}>Recommendations</p>
        </div>
        <div className="space-y-3">
          {insights.recommendations.map((rec, i) => (
            <div key={i} className="flex items-start gap-3">
              <span className="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5" style={{ backgroundColor: "#38bdf820", color: "#38bdf8" }}>
                {i + 1}
              </span>
              <p className="text-sm leading-relaxed" style={{ color: "#94a3b8" }}>{rec}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Download CTA */}
      <div className="flex justify-center">
        <button
          onClick={handleReport}
          disabled={generating}
          className="flex items-center gap-2 px-10 py-3 rounded-xl font-semibold transition-opacity"
          style={{ backgroundColor: "#38bdf8", color: "#0d0f14", opacity: generating ? 0.7 : 1 }}
        >
          <Download className="w-5 h-5" />
          {generating ? "Generating PDF Report..." : "Download Full PDF Report"}
        </button>
      </div>

    </div>
  );
}