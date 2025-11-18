import React from "react";

const SitePublicidadeNativa: React.FC = () => {
  return (
    <div className="flex flex-col h-full gap-4">
      <header>
        <h2 className="text-2xl font-semibold text-white">
          Site / Portal · Publicidade nativa
        </h2>
        <p className="text-sm text-red-200/70">
          Conteúdos de publicidade nativa publicados no portal.
        </p>
      </header>

      <div className="text-red-100/80 text-sm">
        (Em construção) — aqui vamos filtrar formato &quot;publicidade_nativa&quot;.
      </div>
    </div>
  );
};

export default SitePublicidadeNativa;
