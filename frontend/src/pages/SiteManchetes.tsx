import React from "react";

export const SiteManchetes: React.FC = () => {
  return (
    <div className="flex flex-col h-full gap-4">
      <header>
        <h2 className="text-2xl font-semibold text-white">
          Site / Portal · Manchetes
        </h2>
        <p className="text-sm text-red-200/70">
          Manchetes de conteúdos especiais, organizadas para consulta rápida.
        </p>
      </header>

      <div className="text-red-100/80 text-sm">
        (Em construção) — aqui vamos filtrar o formato &quot;manchete&quot;.
      </div>
    </div>
  );
};

export default SiteManchetes;
