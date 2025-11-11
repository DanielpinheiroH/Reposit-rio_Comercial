import React from "react";

export const Footer: React.FC = () => {
  return (
    <footer className="w-full border-t border-slate-900/80 bg-slate-950/80 backdrop-blur px-4 md:px-8 py-2 flex items-center justify-between text-[9px] text-slate-500">
      <div className="flex items-center gap-1">
        <span className="h-1.5 w-1.5 rounded-full bg-emerald-400/80" />
        <span>Repositório Comercial • painel interno</span>
      </div>
      <div className="hidden md:flex gap-3">
        <span>v0.1</span>
        <span className="text-slate-600">API pronta pra escalar</span>
      </div>
    </footer>
  );
};
