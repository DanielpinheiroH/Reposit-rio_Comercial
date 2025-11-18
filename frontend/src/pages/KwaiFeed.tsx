// src/pages/KwaiFeed.tsx
import React from "react";

export const KwaiFeed: React.FC = () => {
  return (
    <div className="flex flex-col h-full gap-4">
      <header>
        <h2 className="text-2xl font-semibold text-white">
          Kwai · Feed / Vídeos
        </h2>
        <p className="text-sm text-red-200/70">
          Conteúdos do Kwai cadastrados no repositório.
        </p>
      </header>

      <div className="text-red-100/80 text-sm">
        (Em construção) — aqui conectamos com post_kwai.
      </div>
    </div>
  );
};
