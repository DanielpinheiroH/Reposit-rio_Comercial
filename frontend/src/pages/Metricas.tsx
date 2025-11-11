import React from "react";
import { useOutletContext } from "react-router-dom";
import type { LayoutContext } from "../types/layout";

export const Metricas: React.FC = () => {
  const { isOk } = useOutletContext<LayoutContext>();

  return (
    <section className="space-y-4">
      <div className="flex items-baseline justify-between gap-2">
        <div>
          <h2 className="text-lg font-semibold text-slate-50">
            Métricas
          </h2>
          <p className="text-[10px] text-slate-500">
            Visão consolidada de performance por conteúdo, plataforma e coleção.
          </p>
        </div>
      </div>

      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 text-[10px] text-slate-400 space-y-2">
        {isOk ? (
          <>
            <p>
              Aqui vamos consumir o endpoint <code className="text-emerald-300">/metrics</code> e
              relacionar com os assets.
            </p>
            <ul className="list-disc list-inside space-y-1">
              <li>Visualizações, engajamento, alcance.</li>
              <li>Filtro por período, cliente, campanha e plataforma.</li>
              <li>Destaque de top conteúdos.</li>
            </ul>
          </>
        ) : (
          <p>
            Assim que a API estiver online, essa tela passa a exibir dados reais de performance.
          </p>
        )}
      </div>
    </section>
  );
};
