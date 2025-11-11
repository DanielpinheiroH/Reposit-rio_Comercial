import React from "react";
import { useOutletContext } from "react-router-dom";
import type { LayoutContext } from "../types/layout";

export const Dashboard: React.FC = () => {
  const { isOk, loading, error } = useOutletContext<LayoutContext>();

  return (
    <section className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-5">
        {/* Visão geral */}
        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-4 flex flex-col gap-2">
          <div className="text-[10px] uppercase tracking-[0.16em] text-slate-500">
            Visão geral
          </div>
          <div className="text-sm text-slate-200">
            Bem-vindo ao Repositório Comercial.
          </div>
          <p className="text-[10px] text-slate-500">
            Central único para todos os conteúdos, coleções e resultados comerciais.
          </p>
        </div>

        {/* Status da API */}
        <div className="bg-slate-900/40 border border-slate-800/60 rounded-2xl p-4 flex flex-col gap-1 text-[10px] text-slate-400">
          <div className="uppercase tracking-[0.16em] text-slate-500">
            Status da API
          </div>
          <div className="flex items-center gap-2 mt-1">
            <span
              className={`h-2 w-2 rounded-full ${
                loading ? "bg-amber-400" : isOk ? "bg-emerald-400" : "bg-red-500"
              }`}
            />
            <span>
              {loading
                ? "Checando conexão com o backend..."
                : error
                ? error
                : isOk
                ? "Conectado. Pronto para consumir dados reais."
                : "API não respondeu como esperado."}
            </span>
          </div>
        </div>

        {/* Próximos passos */}
        <div className="bg-slate-900/40 border border-slate-800/60 rounded-2xl p-4 text-[10px] text-slate-400 flex flex-col">
          <div className="uppercase tracking-[0.16em] text-slate-500">
            Próximos passos
          </div>
          <ul className="mt-2 space-y-1 list-disc list-inside">
            <li>Listar conteúdos especiais via API.</li>
            <li>Criar visão de posts & shorts por plataforma.</li>
            <li>Organizar coleções por campanha/segmento.</li>
            <li>Exibir métricas consolidadas por asset.</li>
          </ul>
        </div>
      </div>
    </section>
  );
};
