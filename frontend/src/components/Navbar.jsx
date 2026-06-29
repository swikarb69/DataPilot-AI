export default function Navbar() {
  return (
    <nav className="border-b border-brand-border bg-brand-surface px-8 py-4 flex items-center gap-3">
      <div className="w-8 h-8 rounded-lg bg-brand-accent flex items-center justify-center">
        <span className="text-brand-bg font-bold text-sm">D</span>
      </div>
      <span className="font-semibold text-lg tracking-tight">DataPilot <span className="text-brand-accent">AI</span></span>
    </nav>
  );
}