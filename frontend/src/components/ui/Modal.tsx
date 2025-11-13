// src/components/ui/Modal.tsx
import React, { useEffect } from "react";

type ModalProps = {
  open: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  widthClass?: string; // ex: "max-w-2xl"
};

export const Modal: React.FC<ModalProps> = ({
  open,
  onClose,
  title,
  children,
  widthClass = "max-w-2xl",
}) => {
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") onClose();
    }
    if (open) document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-[100] flex items-center justify-center"
      aria-modal="true"
      role="dialog"
    >
      {/* backdrop vermelho translúcido */}
      <div
        className="absolute inset-0 bg-red-950/70 backdrop-blur-sm"
        onClick={onClose}
      />
      <div
        className={`relative w-full ${widthClass} mx-4 rounded-2xl border border-red-900/60 bg-red-900/30 shadow-xl`}
      >
        {title && (
          <div className="px-5 py-4 border-b border-red-900/60 flex items-center justify-between">
            <h3 className="text-red-100 font-semibold">{title}</h3>
            <button
              onClick={onClose}
              className="text-red-200/80 hover:text-white text-sm px-2 py-1 rounded-md border border-red-900/60 hover:bg-red-900/60"
              aria-label="Fechar"
            >
              fechar
            </button>
          </div>
        )}
        <div className="p-5">{children}</div>
      </div>
    </div>
  );
};
