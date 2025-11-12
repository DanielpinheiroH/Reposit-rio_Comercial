import React, { useEffect, useState } from "react";
import { listCollections, type Collection } from "../lib/collections";

export const Colecoes: React.FC = () => {
  const [state, setState] = useState<{loading: boolean; error: string; data: Collection[]}>({
    loading: true,
    error: "",
    data: [],
  });

  useEffect(() => {
    (async () => {
      setState((s) => ({ ...s, loading: true, error: "" }));
      try {
        const data = await listCollections();
        setState({ loading: false, error: "", data });
      } catch (e: any) {
        setState({ loading: false, error: "Falha ao carregar coleções.", data: [] });
      }
    })();
  }, []);

  return (
    <section className="space-y-6">
      <div className="flex items-end justify-between">
        <div>
          <h3 className="text-lg font-semibold text-slate-100">Coleções</h3>
          <p className="text-xs text-slate-500">
            Grupos temáticos de assets (campanhas, segmentos, dossiês).
          </p>
        </div>
        <div className="text-xs text-slate-500">
          {state.loading ? "Carregando…" : `${state.data.length} coleção(ões)`}
        </div>
      </div>

      {state.error && <div className="text-red-400 text-sm">{state.error}</div>}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5">
        {state.data.map((c) => {
          const count = c.assets?.length ?? 0;
          return (
            <article
              key={c.id}
              className="bg-slate-900/70 border border-slate-800 rounded-2xl p-4 flex flex-col gap-2"
            >
              <div className="text-[10px] uppercase tracking-wider text-slate-500">
                Coleção
              </div>
              <h4 className="text-sm text-slate-100">{c.nome}</h4>
              {c.descricao && (
                <p className="text-[11px] text-slate-400 line-clamp-2">{c.descricao}</p>
              )}
              <div className="mt-2 text-[10px] text-slate-500">
                {count} item(ns)
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
};
