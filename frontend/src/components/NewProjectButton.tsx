import React from "react";

type Props = { onClick: () => void };

export const NewProjectButton: React.FC<Props> = ({ onClick }) => {
  return (
    <button
      onClick={onClick}
      className="
        fixed bottom-6 right-6 z-[60]
        inline-flex items-center gap-2
        rounded-xl border border-red-900/70
        bg-red-900/60 backdrop-blur
        px-4 py-3
        text-sm font-medium text-red-50
        shadow-lg
        hover:bg-red-800/70 hover:border-red-700
        active:scale-[0.98]
        transition-all
      "
      title="Novo projeto (N)"
    >
      <span className="inline-block h-2 w-2 rounded-full bg-white/90" />
      <span>Novo projeto</span>
    </button>
  );
};
