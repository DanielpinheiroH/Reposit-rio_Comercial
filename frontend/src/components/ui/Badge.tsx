import React from "react";

export const Badge: React.FC<{
  children: React.ReactNode;
  tone?: "emerald" | "slate" | "blue" | "amber" | "red";
  className?: string;
}> = ({ children, tone = "slate", className = "" }) => {
  const map: Record<string, string> = {
    emerald: "bg-emerald-900/30 text-emerald-300 border-emerald-800/60",
    slate: "bg-slate-900/40 text-slate-300 border-slate-800",
    blue: "bg-blue-900/30 text-blue-300 border-blue-800/60",
    amber: "bg-amber-900/30 text-amber-300 border-amber-800/60",
    red: "bg-red-900/30 text-red-300 border-red-800/60",
  };

  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-md border text-[10px] ${map[tone]} ${className}`}
    >
      {children}
    </span>
  );
};
