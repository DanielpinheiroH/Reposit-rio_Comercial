import React from "react";

type Props = { onClick: () => void };

export const NewProjectButton: React.FC<Props> = ({ onClick }) => {
  return (
    <button
      onClick={onClick}
      className="fixed bottom-6 right-6 z-[60] inline-flex items-center gap-2 rounded-xl border border-red-900/70 bg-red-900/40 backdrop-blur px-4 py-3 text-sm text-red-100 hover:bg-red-800/50 shadow-lg"
      title="Novo projeto (N)"
    >
      <span className="inline-block h-2 w-2 rounded-full bg-white/90" />
      <span>Novo projeto</span>
    </button>
  );
};
