import React from "react";

export const ProjetoNovo: React.FC = () => {
  return (
    <section className="space-y-6">
      <div className="rounded-2xl border border-red-900/60 bg-red-900/30 p-5">
        <h3 className="text-lg font-semibold text-red-100">Novo Projeto</h3>
        <p className="text-sm text-red-100/80 mt-1">
          Aqui vai o formulário de criação do projeto (nome, cotas, metas, datas, etc.).
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-2xl border border-red-900/60 bg-red-900/20 p-4">
          <div className="text-[10px] uppercase tracking-[0.16em] text-red-200/90">Informações</div>
          <p className="text-sm text-red-100/90 mt-2">
            Estruturemos campos essenciais e validações depois. Pronto pra conectar ao backend.
          </p>
        </div>
        <div className="rounded-2xl border border-red-900/60 bg-red-900/20 p-4">
          <div className="text-[10px] uppercase tracking-[0.16em] text-red-200/90">Próximos passos</div>
          <ul className="list-disc list-inside text-sm text-red-100/90 mt-2 space-y-1">
            <li>Salvar no banco via API</li>
            <li>Criar cotas associadas</li>
            <li>Validação e feedback de sucesso</li>
          </ul>
        </div>
      </div>
    </section>
  );
};
