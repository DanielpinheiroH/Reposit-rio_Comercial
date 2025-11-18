import React from "react";

const SiteSubManchetes: React.FC = () => {
  return (
    <div className="flex flex-col h-full gap-4">
      <header>
        <h2 className="text-2xl font-semibold text-white">
          Site / Portal · Sub-manchetes
        </h2>
        <p className="text-sm text-red-200/70">
          Sub-manchetes vinculadas aos conteúdos especiais.
        </p>
      </header>

      <div className="text-red-100/80 text-sm">
        (Em construção) — aqui vamos filtrar o formato &quot;sub_manchete&quot;.
      </div>
    </div>
  );
};

export default SiteSubManchetes;
