import React, { useEffect, useState } from "react";
import { useOutletContext } from "react-router-dom";
import { api } from "../lib/api";
import type { LayoutContext } from "../types/layout";

type ConteudoEspecial = {
  id: number;
  titulo: string;
  cliente?: string;
  campanha?: string;
  segmento?: string;
  url: string;
  data_publicacao?: string;
};

export const ConteudosEspeciais: React.FC = () => {
  const { isOk } = useOutletContext<LayoutContext>();
  const [items, setItems] = useState<ConteudoEspecial[]>([]);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");

  useEffect(() => {
    if (!isOk) return;
    async function fetchConteudos() {
      try {
        setLoading(true);
        setErro("");
        // Ajusta o endpoint aqui de acordo com o router do backend
        const res = await api.get<ConteudoEspecial[]>("/conteudo-especial");
        setItems(res.data);
      } catch (e: any) {
        console.error(e);
        setErro("Não consegui carregar os conteúdos especiais da API.");
      } finally {
        setLoading(false);
      }
    }
    fetchConteudos();
  }, [isOk]);

  return (
    <section className="space-y-4">
      <div className="flex items-baseline justify-between gap-2">
        <div>
          <h2 className="text-lg font-semibold text-slate-50">
            Conteúdos especiais
          </h2>
          <p className="text-[10px] text-slate-500">
            Matérias, publis, artigos e conteúdos proprietários cadastrados.
          </p>
        </div>
        <button
          className="px-3 py-1.5 rounded-lg bg-emerald-500/90 text-slate-950 text-[10px] font-semibold hover:bg-emerald-400 transition-colors"
          disabled
        >
          + Novo conteúdo
        </button>
      </div>

      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden">
        <div className="px-3 py-2 border-b border-slate-800 text-[9px] text-slate-500 flex justify-between">
          <span>Listagem</span>
          {loading && <span>Carregando...</span>}
          {erro && <span className="text-red-400">{erro}</span>}
        </div>

        <div className="divide-y divide-slate-900/80 text-[10px]">
          {items.length === 0 && !loading && !erro && (
            <div className="px-3 py-3 text-slate-500">
              Nenhum conteúdo especial encontrado. (Depois conectamos com o cadastro real)
            </div>
          )}

          {items.map((c) => (
            <div
              key={c.id}
              className="px-3 py-3 flex flex-col md:flex-row md:items-center md:justify-between gap-1 hover:bg-slate-900/70"
            >
              <div>
                <div className="text-slate-100 text-xs font-medium">
                  {c.titulo}
                </div>
                <div className="text-slate-500">
                  {c.cliente && <span>{c.cliente}</span>}
                  {c.campanha && <span> • {c.campanha}</span>}
                  {c.segmento && <span> • {c.segmento}</span>}
                </div>
              </div>
              <div className="flex items-center gap-3 text-[9px] text-slate-500">
                {c.data_publicacao && (
                  <span>
                    Publicado em{" "}
                    {new Date(c.data_publicacao).toLocaleDateString("pt-BR")}
                  </span>
                )}
                <a
                  href={c.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-emerald-400 hover:text-emerald-300"
                >
                  Abrir link
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
