import React from "react";

export const Footer: React.FC = () => {
  return (
    <footer className="w-full border-t border-red-900 bg-red-950/80 backdrop-blur px-4 md:px-8 py-2 flex items-center justify-between text-[9px] text-red-200/80">
      <div className="flex items-center gap-1">
        <span className="h-1.5 w-1.5 rounded-full bg-white/90" />
        <span>Repositório Comercial • painel interno</span>
      </div>
      <div className="hidden md:flex gap-3">
        <span>v0.1</span>
        <span className="text-red-200/60">API pronta pra escalar</span>
      </div>
    </footer>
  );
};
