import { useState, useRef } from "react";
import { Upload, FileText, Loader2 } from "lucide-react";
import { uploadFile } from "../services/api";

export default function UploadZone({ onUploadSuccess }) {
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const inputRef = useRef();

  const handleFile = async (file) => {
    if (!file) return;
    setError(null);
    setLoading(true);
    try {
      const data = await uploadFile(file);
      onUploadSuccess(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    handleFile(e.dataTransfer.files[0]);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] px-4">
      <h1 className="text-4xl font-bold mb-2 text-center">
        Your AI-Powered <span className="text-brand-accent">Data Analyst</span>
      </h1>
      <p className="text-brand-muted mb-10 text-center text-lg">
        Upload any CSV or Excel file. Get instant insights, charts, and a full report.
      </p>

      <div
        onClick={() => !loading && inputRef.current.click()}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        className={`w-full max-w-xl border-2 border-dashed rounded-2xl p-14 flex flex-col items-center gap-4 cursor-pointer transition-all duration-200
          ${dragging ? "border-brand-accent bg-brand-accent/5" : "border-brand-border bg-brand-surface hover:border-brand-accent/50"}`}
      >
        {loading ? (
          <>
            <Loader2 className="w-10 h-10 text-brand-accent animate-spin" />
            <p className="text-brand-muted">Analyzing your dataset...</p>
          </>
        ) : (
          <>
            <div className="w-16 h-16 rounded-2xl bg-brand-accent/10 flex items-center justify-center">
              <Upload className="w-8 h-8 text-brand-accent" />
            </div>
            <div className="text-center">
              <p className="font-medium text-lg">Drop your file here</p>
              <p className="text-brand-muted text-sm mt-1">or click to browse — CSV, XLSX supported</p>
            </div>
          </>
        )}
        <input
          ref={inputRef}
          type="file"
          accept=".csv,.xlsx,.xls"
          className="hidden"
          onChange={(e) => handleFile(e.target.files[0])}
        />
      </div>

      {error && (
        <p className="mt-4 text-red-400 text-sm">{error}</p>
      )}
    </div>
  );
}