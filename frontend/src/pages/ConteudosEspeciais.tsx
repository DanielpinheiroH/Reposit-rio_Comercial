import React, { useEffect, useMemo, useState } from "react";
import { useOutletContext } from "react-router-dom";
import type { LayoutContext } from "../types/layout";
import type { Asset, PageOut, Plataforma } from "../types/api";
import { listConteudosEspeciais } from "../lib/assets";
import { ConteudosFilter } from "../components/filters/ConteudosFilter";
import { Badge } from "../components/ui/Badge";

type ViewMode = "cards" | "table";

export const ConteudosEspeciais: React.FC = () => {
  const { isOk } = useOutletContext<LayoutContext>();

  // Filtros
  const [q, setQ] = useState("");
  const [plataforma, setPlataforma] = useState<Plataforma | "">("");
  const [cliente, setCliente] = useState("");
  const [dtIni, setDtIni] = useState("");
  const [dtFim, setDtFim] = useState("");

  // Lista / paginação / UI
  const [data, setData] = useState<PageOut<Asset>>({
    items: [],
    page: 1,
    size: 12,
    total: 0,
    pages: 1,
  });
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");
  const [view, setView] = useState<ViewMode>("cards");

  const paramsMemo = useMemo(
    () => ({
      page: data.page,
      size: data.size,
      q,
      plataforma,
      cliente,
      dt_ini: dtIni,
      dt_fim: dtFim,
    }),
    [data.page, data.size, q, plataforma, cliente, dtIni, dtFim]
  );

  async function fetchPage(page = 1) {
    if (!isOk) return;
    try {
      setLoading(true);
      setErro("");
      const res = await listConteudosEspeciais({
        ...paramsMemo,
        page,
      });
      setData(res);
    } catch (e: any) {
      console.error(e);
      setErro("Não consegui carregar os conteúdos especiais.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (!isOk) return;
    fetchPage(1);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOk]);

  const aplicar = () => fetchPage(1);
  const limpar = () => {
    setQ("");
    setPlataforma("");
    setCliente("");
    setDtIni("");
    setDtFim("");
    fetchPage(1);
  };

  const changeSize = (n: number) => setData((d) => ({ ...d, size: n }));

  useEffect(() => {
    if (!isOk) return;
    // quando trocar o size, recarrega página 1
    fetchPage(1);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data.size]);

  const HeaderRight = (
    <div className="flex items-center gap-2">
      <div className="hidden md:flex items-center gap-2 text-[10px]">
        <span className="text-slate-500">Exibir:</span>
        <button
          onClick={() => setView("cards")}
          className={`px-2 py-1 rounded-md border text-[10px] ${
            view === "cards"
              ? "border-emerald-700 text-emerald-300 bg-emerald-900/10"
              : "border-slate-800 text-slate-400 hover:bg-slate-900/40"
          }`}
        >
          Cards
        </button>
        <button
          onClick={() => setView("table")}
          className={`px-2 py-1 rounded-md border text-[10px] ${
            view === "table"
              ? "border-emerald-700 text-emerald-300 bg-emerald-900/10"
              : "border-slate-800 text-slate-400 hover:bg-slate-900/40"
          }`}
        >
          Tabela
        </button>
      </div>

      <select
        className="bg-slate-950 border border-slate-800 rounded-md px-2 py-1 text-[10px] text-slate-300"
        value={data.size}
        onChange={(e) => changeSize(Number(e.target.value))}
      >
        {[6, 12, 24, 48].map((n) => (
          <option key={n} value={n}>{n}/página</option>
        ))}
      </select>
    </div>
  );

  return (
    <section className="space-y-4">
      {/* Cabeçalho + ações */}
      <div className="flex items-baseline justify-between gap-2">
        <div>
          <h2 className="text-lg font-semibold text-slate-50">Conteúdos especiais</h2>
          <p className="text-[10px] text-slate-500">
            Filtre por plataforma, cliente e período; visualize como cards ou tabela.
          </p>
        </div>
        {HeaderRight}
      </div>

      {/* Filtros */}
      <ConteudosFilter
        q={q} setQ={setQ}
        plataforma={plataforma} setPlataforma={setPlataforma}
        cliente={cliente} setCliente={setCliente}
        dtIni={dtIni} setDtIni={setDtIni}
        dtFim={dtFim} setDtFim={setDtFim}
        onApply={aplicar}
        onClear={limpar}
      />

      {/* Estado de erro */}
      {erro && (
        <div className="px-3 py-2 rounded-lg bg-red-900/30 border border-red-800 text-red-200 text-[10px]">
          {erro}
        </div>
      )}

      {/* Lista */}
      {!erro && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden">
          <div className="px-3 py-2 border-b border-slate-800 text-[9px] text-slate-500 flex justify-between">
            <span>
              {loading ? "Carregando..." : `Resultados: ${data.total}`}
            </span>
            <span>Página {data.page} de {data.pages}</span>
          </div>

          {/* GRID CARDS */}
          {view === "cards" && (
            <div className="p-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {loading && Array.from({ length: data.size }).map((_, i) => (
                <div key={i} className="h-32 rounded-xl bg-slate-950 border border-slate-800 animate-pulse" />
              ))}

              {!loading && data.items.length === 0 && (
                <div className="col-span-full px-3 py-6 text-[10px] text-slate-500">
                  Nenhum conteúdo encontrado com os filtros atuais.
                </div>
              )}

              {!loading && data.items.map((a) => (
                <article key={a.id} className="rounded-xl border border-slate-800 bg-slate-950/60 p-3 flex flex-col gap-2">
                  <div className="flex items-start justify-between gap-2">
                    <h3 className="text-xs font-medium text-slate-100 line-clamp-2">{a.titulo}</h3>
                    <Badge tone="emerald">{a.plataforma}</Badge>
                  </div>

                  <div className="text-[10px] text-slate-500 space-x-1">
                    {a.cliente && <span>{a.cliente}</span>}
                    {a.campanha && <span>• {a.campanha}</span>}
                    {a.segmento && <span>• {a.segmento}</span>}
                  </div>

                  <div className="flex items-center justify-between text-[10px] text-slate-500">
                    <div className="space-x-1">
                      {a.classificacao_conteudo_especial && (
                        <Badge tone="amber">{a.classificacao_conteudo_especial}</Badge>
                      )}
                      {a.data_publicacao && (
                        <span>
                          {new Date(a.data_publicacao).toLocaleDateString("pt-BR")}
                        </span>
                      )}
                    </div>
                    <a
                      href={a.url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-emerald-300 hover:text-emerald-200"
                    >
                      Abrir →
                    </a>
                  </div>
                </article>
              ))}
            </div>
          )}

          {/* TABELA */}
          {view === "table" && (
            <div className="overflow-x-auto">
              <table className="min-w-full text-[10px]">
                <thead className="bg-slate-950/60 border-b border-slate-800 text-slate-400">
                  <tr>
                    <th className="text-left px-3 py-2 font-medium">Título</th>
                    <th className="text-left px-3 py-2 font-medium">Cliente</th>
                    <th className="text-left px-3 py-2 font-medium">Campanha</th>
                    <th className="text-left px-3 py-2 font-medium">Plataforma</th>
                    <th className="text-left px-3 py-2 font-medium">Classificação</th>
                    <th className="text-left px-3 py-2 font-medium">Publicado</th>
                    <th className="text-left px-3 py-2 font-medium">Ação</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-900/70">
                  {loading && (
                    <tr>
                      <td colSpan={7} className="px-3 py-4 text-slate-500">Carregando…</td>
                    </tr>
                  )}
                  {!loading && data.items.length === 0 && (
                    <tr>
                      <td colSpan={7} className="px-3 py-4 text-slate-500">
                        Nenhum conteúdo encontrado com os filtros atuais.
                      </td>
                    </tr>
                  )}
                  {!loading && data.items.map((a) => (
                    <tr key={a.id}>
                      <td className="px-3 py-2 text-slate-200">{a.titulo}</td>
                      <td className="px-3 py-2 text-slate-400">{a.cliente || "-"}</td>
                      <td className="px-3 py-2 text-slate-400">{a.campanha || "-"}</td>
                      <td className="px-3 py-2">
                        <Badge tone="emerald">{a.plataforma}</Badge>
                      </td>
                      <td className="px-3 py-2 text-slate-400">
                        {a.classificacao_conteudo_especial || "-"}
                      </td>
                      <td className="px-3 py-2 text-slate-400">
                        {a.data_publicacao
                          ? new Date(a.data_publicacao).toLocaleDateString("pt-BR")
                          : "-"}
                      </td>
                      <td className="px-3 py-2">
                        <a
                          href={a.url}
                          target="_blank"
                          rel="noreferrer"
                          className="text-emerald-300 hover:text-emerald-200"
                        >
                          Abrir →
                        </a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Paginação */}
          <div className="px-3 py-2 border-t border-slate-800 flex items-center justify-between text-[10px] text-slate-500">
            <button
              disabled={loading || data.page <= 1}
              onClick={() => fetchPage(data.page - 1)}
              className="px-2 py-1 rounded-md border border-slate-800 hover:bg-slate-900/40 disabled:opacity-40"
            >
              ◀ Anterior
            </button>
            <div>
              Página <span className="text-slate-300">{data.page}</span> / {data.pages} •
              <span className="ml-1">{data.total} itens</span>
            </div>
            <button
              disabled={loading || data.page >= data.pages}
              onClick={() => fetchPage(data.page + 1)}
              className="px-2 py-1 rounded-md border border-slate-800 hover:bg-slate-900/40 disabled:opacity-40"
            >
              Próxima ▶
            </button>
          </div>
        </div>
      )}
    </section>
  );
};
