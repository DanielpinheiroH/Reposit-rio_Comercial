import React from "react";

const SiteTodos: React.FC = () => {
  return (
    <div className="flex flex-col h-full gap-4">
      <header>
        <h2 className="text-2xl font-semibold text-white">
          Site / Portal · Todos os conteúdos
        </h2>
        <p className="text-sm text-red-200/70">
          Visão geral de todos os conteúdos especiais do site / portal.
        </p>
      </header>

      <div className="text-red-100/80 text-sm">
        (Em construção) — aqui vamos plugar a listagem de conteúdos especiais
        com todos os formatos.
      </div>
    </div>
  );
};

export default SiteTodos;
