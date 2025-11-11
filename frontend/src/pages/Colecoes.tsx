import React, { useEffect, useState } from "react";
import { useOutletContext } from "react-router-dom";
import { api } from "../lib/api";
import type { LayoutContext } from "../types/layout";

type Colecao = {
  id: number;
  nome: string;
  descricao?: string;
  created_at?: string;
};

export const Colecoes: React.FC = () => {
  const { isOk } = useOutletContext<LayoutContext>();
  const [items, setItems] = useState<Colecao[]>([]);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");

  useEffect(() => {
    if (!isOk) return;
    async function fetchColecoes() {
      try {
        setLoading(true);
        setErro("");
        // Ajuste ao seu router: ex: GET /collections
        const res = await api.get<Colecao[]>("/collections");
        setItems(res.data);
      } catch (e: any) {
        console.error(e);
        setErro("Não consegui carregar as coleções.");
      } finally {
        setLoading(false);
      }
    }
    fetchColecoes();
  }, [isOk]);

  return (
    <section className="space-y-4">
      <div className="flex items-baseline justify-between gap-2">
        <div>
          <h2 className="text-lg font-semibold text-slate-50">
            Coleções
          </h2>
          <p className="text-[10px] text-slate-500">
            Agrupamentos de conteúdos por campanha, cliente, segmento ou uso interno.
          </p>
        </div>
        <button
          className="px-3 py-1.5 rounded-lg bg-emerald-500/90 text-slate-950 text-[10px] font-semibold hover:bg-emerald-400 transition-colors"
          disabled
        >
          + Nova coleção
        </button>
      </div>

      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden">
        <div className="px-3 py-2 border-b border-slate-800 text-[9px] text-slate-500 flex justify-between">
          <span>Lista de coleções</span>
          {loading && <span>Carregando...</span>}
          {erro && <span className="text-red-400">{erro}</span>}
        </div>

        <div className="divide-y divide-slate-900/80 text-[10px]">
          {items.length === 0 && !loading && !erro && (
            <div className="px-3 py-3 text-slate-500">
              Nenhuma coleção cadastrada ainda.
            </div>
          )}

          {items.map((c) => (
            <div
              key={c.id}
              className="px-3 py-3 flex flex-col md:flex-row md:items-center md:justify-between gap-1 hover:bg-slate-900/70"
            >
              <div>
                <div className="text-slate-100 text-xs font-medium">
                  {c.nome}
                </div>
                {c.descricao && (
                  <div className="text-slate-500">
                    {c.descricao}
                  </div>
                )}
              </div>
              <div className="text-[9px] text-slate-500">
                {c.created_at &&
                  `Criada em ${new Date(c.created_at).toLocaleDateString(
                    "pt-BR"
                  )}`}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
