// frontend/src/components/ui/Modal.tsx
import React from "react";

type ModalProps = {
  open: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
};

export const Modal: React.FC<ModalProps> = ({
  open,
  onClose,
  title,
  children,
}) => {
  return (
    <div
      className={`
        fixed inset-0 z-50 flex items-center justify-center
        transition-all duration-200
        ${open ? "pointer-events-auto" : "pointer-events-none"}
      `}
      aria-hidden={!open}
    >
      {/* BACKDROP COM FADE */}
      <div
        className={`
          absolute inset-0
          bg-slate-950/70 backdrop-blur-sm
          transition-opacity duration-200
          ${open ? "opacity-100" : "opacity-0"}
        `}
        onClick={onClose}
      />

      {/* CONTAINER DO MODAL COM SCALE + TRANSLATE */}
      <div
        className={`
          relative w-full max-w-lg mx-4
          rounded-2xl border border-red-900/70
          bg-slate-950/95
          shadow-2xl shadow-red-900/40
          transition-all duration-200
          ${open
            ? "opacity-100 translate-y-0 scale-100"
            : "opacity-0 -translate-y-4 scale-95"}
        `}
      >
        {/* Cabeçalho */}
        {(title || onClose) && (
          <div className="flex items-center justify-between px-5 pt-4 pb-3 border-b border-red-900/60">
            <h2 className="text-sm font-semibold text-red-50">
              {title ?? "Novo registro"}
            </h2>
            <button
              type="button"
              onClick={onClose}
              className="
                inline-flex h-7 w-7 items-center justify-center
                rounded-full border border-red-900/70
                text-xs text-red-200
                hover:bg-red-900/60 hover:text-white
                transition-colors
              "
            >
              ✕
            </button>
          </div>
        )}

        {/* Conteúdo */}
        <div className="px-5 py-4 max-h-[70vh] overflow-y-auto custom-scroll">
          {children}
        </div>
      </div>
    </div>
  );
};
