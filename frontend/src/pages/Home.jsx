import { useState } from "react";
import UploadZone from "../components/UploadZone";
import DataSummary from "../components/DataSummary";
import DataCleaning from "../components/DataCleaning";
import EDACharts from "../components/EDACharts";
import AIInsights from "../components/AIInsights";

const STEPS = ["upload", "summary", "clean", "eda", "insights"];

function StepNav({ step, setStep, uploadData, activeFile }) {
  const available = {
    summary: !!uploadData,
    clean: !!uploadData,
    eda: !!activeFile,
    insights: !!activeFile,
  };

  const labels = ["Upload", "Summary", "Clean", "EDA", "AI Insights"];

  return step !== "upload" ? (
    <div className="flex items-center justify-center gap-2 py-4 border-b" style={{ borderColor: "#1e2330" }}>
      {STEPS.slice(1).map((s, i) => (
        <button
          key={s}
          onClick={() => available[s] && setStep(s)}
          className="px-4 py-1.5 rounded-full text-sm font-medium transition-all"
          style={{
            backgroundColor: step === s ? "#38bdf8" : "#13161e",
            color: step === s ? "#0d0f14" : available[s] ? "#94a3b8" : "#334155",
            border: "1px solid",
            borderColor: step === s ? "#38bdf8" : "#1e2330",
            cursor: available[s] ? "pointer" : "not-allowed",
          }}
        >
          {labels[i + 1]}
        </button>
      ))}
    </div>
  ) : null;
}

export default function Home() {
  const [uploadData, setUploadData] = useState(null);
  const [step, setStep] = useState("upload");
  const [activeFile, setActiveFile] = useState(null);

  const handleUpload = (data) => {
    setUploadData(data);
    setActiveFile(data.filename);
    setStep("summary");
  };

  const handleCleaningDone = (data) => {
    setActiveFile(data.cleaned_filename);
    setStep("eda");
  };

  return (
    <main>
      <StepNav step={step} setStep={setStep} uploadData={uploadData} activeFile={activeFile} />

      {step === "upload" && <UploadZone onUploadSuccess={handleUpload} />}
      {step === "summary" && uploadData && (
        <div>
          <DataSummary data={uploadData} />
          <div className="flex justify-center pb-10">
            <button
              onClick={() => setStep("clean")}
              className="px-8 py-3 rounded-xl font-semibold text-sm"
              style={{ backgroundColor: "#38bdf8", color: "#0d0f14" }}
            >
              Run Data Quality Check →
            </button>
          </div>
        </div>
      )}
      {step === "clean" && uploadData && (
        <DataCleaning filename={uploadData.filename} onCleaningDone={handleCleaningDone} />
      )}
      {step === "eda" && activeFile && (
        <EDACharts filename={activeFile} />
      )}
      {step === "insights" && activeFile && (
        <AIInsights filename={activeFile} />
      )}
    </main>
  );
}