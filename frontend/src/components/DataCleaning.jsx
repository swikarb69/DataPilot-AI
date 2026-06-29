import { useState, useEffect } from "react";
import { analyzeIssues, cleanDataset, getDownloadUrl } from "../services/api";
import { AlertTriangle, Copy, Download, CheckCircle, Loader2 } from "lucide-react";

export default function DataCleaning({ filename, onCleaningDone }) {
  const [issues, setIssues] = useState(null);
  const [loading, setLoading] = useState(true);
  const [applying, setApplying] = useState(false);
  const [result, setResult] = useState(null);
  const [fixes, setFixes] = useState({});
  const [removeDuplicates, setRemoveDuplicates] = useState(false);

  useEffect(() => {
    analyzeIssues(filename).then((data) => {
      setIssues(data);
      const defaultFixes = {};
      data.missing_issues.forEach((issue) => {
        defaultFixes[issue.column] = issue.suggestions[0];
      });
      setFixes(defaultFixes);
      setLoading(false);
    });
  }, [filename]);

  const handleApply = async () => {
    setApplying(true);
    const instructions = {
      remove_duplicates: removeDuplicates,
      missing_fixes: Object.entries(fixes).map(([col, strategy]) => ({
        column: col,
        strategy,
      })),
    };
    const data = await cleanDataset(filename, instructions);
    setResult(data);
    setApplying(false);
    onCleaningDone(data);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="w-8 h-8 animate-spin" style={{ color: "#38bdf8" }} />
      </div>
    );
  }

  if (result) {
    return (
      <div className="max-w-3xl mx-auto px-6 py-10">
        <div className="rounded-2xl border p-8 text-center" style={{ backgroundColor: "#13161e", borderColor: "#1e2330" }}>
          <CheckCircle className="w-12 h-12 mx-auto mb-4" style={{ color: "#38bdf8" }} />
          <h2 className="text-2xl font-bold mb-2">Dataset Cleaned</h2>
          <p className="mb-6" style={{ color: "#64748b" }}>
            {result.rows_removed} rows removed · {result.cleaned_rows} rows remaining
          </p>
          <div className="text-left rounded-xl p-4 mb-6 space-y-2" style={{ backgroundColor: "#0d0f14" }}>
            {result.changes.map((c, i) => (
              <p key={i} className="text-sm" style={{ color: "#64748b" }}>✓ {c}</p>
            ))}
          </div>
          <a
            href={getDownloadUrl(result.cleaned_filename)}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl font-medium text-sm"
            style={{ backgroundColor: "#38bdf8", color: "#0d0f14" }}
          >
            <Download className="w-4 h-4" />
            Download Cleaned Dataset
          </a>
        </div>
      </div>
    );
  }

  const hasIssues = issues.missing_issues.length > 0 || issues.duplicate_count > 0;

  return (
    <div className="max-w-3xl mx-auto px-6 py-10">
      <div className="flex items-center gap-3 mb-8">
        <div className="w-2 h-8 rounded-full" style={{ backgroundColor: "#38bdf8" }} />
        <h2 className="text-2xl font-bold">Data Quality Check</h2>
      </div>

      {!hasIssues ? (
        <div className="rounded-2xl border p-8 text-center" style={{ backgroundColor: "#13161e", borderColor: "#1e2330" }}>
          <CheckCircle className="w-10 h-10 mx-auto mb-3" style={{ color: "#38bdf8" }} />
          <p className="font-semibold text-lg">Your dataset looks clean!</p>
          <p className="text-sm mt-1" style={{ color: "#64748b" }}>No missing values or duplicates detected.</p>
        </div>
      ) : (
        <div>
          {issues.duplicate_count > 0 && (
            <div className="rounded-xl border p-5 mb-4 flex items-center justify-between" style={{ backgroundColor: "#13161e", borderColor: "#1e2330" }}>
              <div className="flex items-center gap-3">
                <Copy className="w-5 h-5" style={{ color: "#38bdf8" }} />
                <div>
                  <p className="font-medium">{issues.duplicate_count} duplicate rows detected</p>
                  <p className="text-sm" style={{ color: "#64748b" }}>These are exact copies of other rows</p>
                </div>
              </div>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={removeDuplicates}
                  onChange={(e) => setRemoveDuplicates(e.target.checked)}
                  className="w-4 h-4"
                />
                <span className="text-sm">Remove</span>
              </label>
            </div>
          )}

          {issues.missing_issues.length > 0 && (
            <div className="rounded-xl border mb-6" style={{ backgroundColor: "#13161e", borderColor: "#1e2330" }}>
              <div className="flex items-center gap-3 p-5" style={{ borderBottom: "1px solid #1e2330" }}>
                <AlertTriangle className="w-5 h-5" style={{ color: "#38bdf8" }} />
                <p className="font-medium">Missing Values</p>
              </div>
              <div>
                {issues.missing_issues.map((issue) => (
                  <div key={issue.column} className="p-5 flex items-center justify-between gap-4" style={{ borderBottom: "1px solid #1e2330" }}>
                    <div>
                      <p className="font-medium">{issue.column}</p>
                      <p className="text-sm mt-0.5" style={{ color: "#64748b" }}>
                        {issue.count} missing · {issue.percent}% · {issue.dtype}
                      </p>
                    </div>
                    <select
                      value={fixes[issue.column] || ""}
                      onChange={(e) => setFixes({ ...fixes, [issue.column]: e.target.value })}
                      className="text-sm px-3 py-2 rounded-lg border outline-none"
                      style={{ backgroundColor: "#0d0f14", borderColor: "#1e2330", color: "#f1f5f9" }}
                    >
                      {issue.suggestions.map((s) => (
                        <option key={s} value={s}>{s}</option>
                      ))}
                    </select>
                  </div>
                ))}
              </div>
            </div>
          )}

          {issues.outlier_info.length > 0 && (
            <div className="rounded-xl border p-5 mb-6" style={{ backgroundColor: "#13161e", borderColor: "#1e2330" }}>
              <p className="font-medium mb-3" style={{ color: "#38bdf8" }}>Outliers Detected (informational)</p>
              {issues.outlier_info.map((o) => (
                <p key={o.column} className="text-sm" style={{ color: "#64748b" }}>
                  · {o.column}: {o.count} outliers ({o.percent}%)
                </p>
              ))}
            </div>
          )}

          <button
            onClick={handleApply}
            disabled={applying}
            className="w-full py-3 rounded-xl font-semibold transition-opacity"
            style={{ backgroundColor: "#38bdf8", color: "#0d0f14", opacity: applying ? 0.7 : 1 }}
          >
            {applying ? "Cleaning..." : "Apply Cleaning"}
          </button>
        </div>
      )}
    </div>
  );
}