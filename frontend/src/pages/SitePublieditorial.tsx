import React from "react";

export const SitePublieditorial: React.FC = () => {
  return (
    <div className="flex flex-col h-full gap-4">
      <header>
        <h2 className="text-2xl font-semibold text-white">
          Site / Portal · Publieditorial
        </h2>
        <p className="text-sm text-red-200/70">
          Conteúdos de publieditorial publicados no portal.
        </p>
      </header>

      <div className="text-red-100/80 text-sm">
        (Em construção) — depois ligamos aqui no backend filtrando
        somente os conteúdos com formato &quot;publieditorial&quot;.
      </div>
    </div>
  );
};

export default SitePublieditorial;
