import React from "react";

export const SiteArtigoOpiniaoDigital: React.FC = () => {
  return (
    <div className="flex flex-col h-full gap-4">
      <header>
        <h2 className="text-2xl font-semibold text-white">
          Site / Portal · Artigo / opinião digital
        </h2>
        <p className="text-sm text-red-200/70">
          Artigos e expressões de opinião digital cadastrados no repositório.
        </p>
      </header>

      <div className="text-red-100/80 text-sm">
        (Em construção) — aqui vamos filtrar o formato
        &quot;expressao_de_opiniao_digital&quot;.
      </div>
    </div>
  );
};

export default SiteArtigoOpiniaoDigital;
