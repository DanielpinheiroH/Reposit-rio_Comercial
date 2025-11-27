// frontend/src/pages/Dashboard.tsx
import React, { useEffect, useMemo, useState } from "react";
import { Card } from "../components/ui/Card";
import { listProjetos } from "../lib/projetos";
import type { ProjetoOut } from "../lib/projetos";

type CanalKey =
  | "site"
  | "youtube"
  | "instagram"
  | "tiktok"
  | "kwai"
  | "facebook"
  | "outros";

const LABEL_CANAL: Record<CanalKey, string> = {
  site: "Site / Portal",
  youtube: "YouTube",
  instagram: "Instagram",
  tiktok: "TikTok",
  kwai: "Kwai",
  facebook: "Facebook",
  outros: "Outros",
};

function detectarCanal(p: ProjetoOut): CanalKey {
  const pd = (p.paginaDestino || "").toLowerCase();

  if (pd.startsWith("site")) return "site";
  if (pd.includes("youtube")) return "youtube";
  if (pd.includes("instagram")) return "instagram";
  if (pd.includes("tiktok")) return "tiktok";
  if (pd.includes("kwai")) return "kwai";
  if (pd.includes("facebook")) return "facebook";

  return "outros";
}

export const Dashboard: React.FC = () => {
  const [projetos, setProjetos] = useState<ProjetoOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  // filtros
  const [segmentoSelecionado, setSegmentoSelecionado] = useState<string>("__ALL__");
  const [canalSelecionado, setCanalSelecionado] = useState<CanalKey | "__ALL__">(
    "__ALL__",
  );
  const [buscaTexto, setBuscaTexto] = useState<string>("");

  // ------------ CARREGAR DADOS ------------
  useEffect(() => {
    let isMounted = true;

    async function carregar() {
      try {
        setLoading(true);
        const data = await listProjetos();
        if (!isMounted) return;
        setProjetos(data);
        setErro(null);
      } catch (e) {
        console.error("[Dashboard] erro ao carregar projetos", e);
        if (!isMounted) return;
        setErro("Não foi possível carregar os projetos no momento.");
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    carregar();

    return () => {
      isMounted = false;
    };
  }, []);

  // ------------ DERIVADOS ------------
  const projetosComCanal = useMemo(
    () =>
      projetos.map((p) => ({
        ...p,
        canal: detectarCanal(p),
      })),
    [projetos],
  );

  const segmentos = useMemo(() => {
    const set = new Set<string>();
    projetos.forEach((p) => {
      if (p.segmento) set.add(p.segmento);
    });
    return Array.from(set).sort((a, b) => a.localeCompare(b, "pt-BR"));
  }, [projetos]);

  const canaisPresentes = useMemo(() => {
    const set = new Set<CanalKey>();
    projetosComCanal.forEach((p) => set.add(p.canal));
    return Array.from(set);
  }, [projetosComCanal]);

  const projetosFiltrados = useMemo(() => {
    return projetosComCanal.filter((p) => {
      // filtro por segmento
      if (
        segmentoSelecionado !== "__ALL__" &&
        (p.segmento || "").toLowerCase() !== segmentoSelecionado.toLowerCase()
      ) {
        return false;
      }

      // filtro por canal
      if (canalSelecionado !== "__ALL__" && p.canal !== canalSelecionado) {
        return false;
      }

      // filtro por texto (nome, cliente, campanha)
      if (buscaTexto.trim()) {
        const termo = buscaTexto.toLowerCase();
        const blob =
          `${p.nome || ""} ${p.cliente || ""} ${p.campanha || ""}`.toLowerCase();
        if (!blob.includes(termo)) return false;
      }

      return true;
    });
  }, [projetosComCanal, segmentoSelecionado, canalSelecionado, buscaTexto]);

  const totalProjetos = projetos.length;
  const totalSegmentos = segmentos.length;
  const totalViews = projetos.reduce(
    (acc, p) => acc + (p.visualizacoes ?? 0),
    0,
  );

  // contagem por canal
  const statsPorCanal = useMemo(() => {
    const base: Record<CanalKey, { qtd: number; views: number }> = {
      site: { qtd: 0, views: 0 },
      youtube: { qtd: 0, views: 0 },
      instagram: { qtd: 0, views: 0 },
      tiktok: { qtd: 0, views: 0 },
      kwai: { qtd: 0, views: 0 },
      facebook: { qtd: 0, views: 0 },
      outros: { qtd: 0, views: 0 },
    };

    projetosComCanal.forEach((p) => {
      const canal = p.canal ?? "outros";
      base[canal].qtd += 1;
      base[canal].views += p.visualizacoes ?? 0;
    });

    return base;
  }, [projetosComCanal]);

  // ranking de segmentos
  const rankingSegmentos = useMemo(() => {
    const map = new Map<string, { qtd: number; views: number }>();

    projetos.forEach((p) => {
      const seg = p.segmento || "Sem segmento";
      if (!map.has(seg)) map.set(seg, { qtd: 0, views: 0 });
      const item = map.get(seg)!;
      item.qtd += 1;
      item.views += p.visualizacoes ?? 0;
    });

    return Array.from(map.entries())
      .map(([segmento, v]) => ({ segmento, ...v }))
      .sort((a, b) => b.qtd - a.qtd)
      .slice(0, 5);
  }, [projetos]);

  const formatarData = (iso?: string | null) => {
    if (!iso) return "-";
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return "-";
    return d.toLocaleDateString("pt-BR");
  };

  const formatarNumero = (n?: number | null) => {
    if (n == null) return "-";
    return n.toLocaleString("pt-BR");
  };

  // ------------ RENDER ------------
  return (
    <section className="space-y-6">
      {/* BLOCO 1 – KPIs PRINCIPAIS */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 md:gap-5">
        <Card className="bg-red-900/30 border-red-900/60 text-red-50 lg:col-span-2">
          <div className="text-[10px] uppercase tracking-[0.16em] text-red-200/80">
            Visão geral
          </div>
          <div className="text-sm text-white mt-1">
            Repositório Comercial · Painel de Projetos
          </div>
          <p className="text-[10px] text-red-200/80 mt-1 max-w-xl">
            Consolide aqui todos os projetos por canal, segmento e cliente.
            Use os filtros para navegar por clusters específicos.
          </p>
        </Card>

        <Card className="bg-red-900/20 border-red-900/40 text-red-50">
          <div className="text-[10px] uppercase tracking-[0.16em] text-red-200/80">
            Projetos cadastrados
          </div>
          <div className="mt-1 text-2xl font-semibold text-white">
            {loading ? "…" : totalProjetos}
          </div>
          <p className="mt-1 text-[10px] text-red-200/80">
            Em {loading ? "…" : totalSegmentos || 0} segmento(s).
          </p>
        </Card>

        <Card className="bg-white text-red-950 border-red-200">
          <div className="text-[10px] uppercase tracking-[0.16em] text-red-700/80">
            Alcance estimado
          </div>
          <div className="mt-1 text-2xl font-semibold text-red-900">
            {loading ? "…" : formatarNumero(totalViews)}
          </div>
          <p className="mt-1 text-[10px] text-red-700/80">
            Soma das visualizações declaradas nos projetos.
          </p>
        </Card>
      </div>

      {/* BLOCO 2 – RESUMO POR CANAL */}
      <Card className="bg-red-950/60 border-red-900/70 text-red-50">
        <div className="flex items-center justify-between mb-3 gap-2">
          <div>
            <div className="text-[10px] uppercase tracking-[0.16em] text-red-200/80">
              Canais
            </div>
            <div className="mt-1 text-sm font-medium text-white">
              Distribuição por canal de veiculação
            </div>
          </div>
          {!loading && (
            <div className="text-[10px] text-red-200/80">
              {totalProjetos} projeto(s) no total
            </div>
          )}
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-7 gap-2">
          {(
            ["site", "youtube", "instagram", "tiktok", "kwai", "facebook", "outros"] as CanalKey[]
          ).map((canal) => {
            const stats = statsPorCanal[canal];
            const isActive = canalSelecionado === canal;
            const temProjetos = stats.qtd > 0;

            if (!temProjetos && !canaisPresentes.includes(canal)) {
              // se nunca apareceu esse canal, esconde pra não ficar poluído
              return null;
            }

            return (
              <button
                key={canal}
                type="button"
                onClick={() =>
                  setCanalSelecionado(
                    isActive ? "__ALL__" : canal,
                  )
                }
                className={[
                  "rounded-lg border px-3 py-2 text-left text-[11px] transition flex flex-col gap-1",
                  isActive
                    ? "bg-red-600 border-red-400 text-white shadow-sm"
                    : "bg-red-950/80 border-red-900/80 text-red-100 hover:bg-red-900/70",
                ].join(" ")}
              >
                <span className="font-medium">{LABEL_CANAL[canal]}</span>
                <span className="text-[10px] text-red-200/80">
                  {stats.qtd} proj. · {formatarNumero(stats.views)} views
                </span>
              </button>
            );
          })}
        </div>
      </Card>

      {/* BLOCO 3 – FILTROS + BUSCA */}
      <Card className="bg-red-950/60 border-red-900/70 text-red-50">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6">
          {/* Segmento */}
          <div>
            <label className="block text-[11px] font-medium text-red-200/80 mb-1">
              Segmento
            </label>
            <select
              value={segmentoSelecionado}
              onChange={(e) => setSegmentoSelecionado(e.target.value)}
              className="w-full rounded-lg border border-red-700/80 bg-red-950/80 px-3 py-2 text-xs text-red-50
                         focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-400"
            >
              <option value="__ALL__">Todos os segmentos</option>
              {segmentos.map((seg) => (
                <option key={seg} value={seg}>
                  {seg}
                </option>
              ))}
            </select>
            <p className="mt-1 text-[10px] text-red-200/80">
              Filtra por cluster de conteúdo (Política, Educação, Saúde, etc.).
            </p>
          </div>

          {/* Canal (espelho do de cima, mas mais direto) */}
          <div>
            <label className="block text-[11px] font-medium text-red-200/80 mb-1">
              Canal
            </label>
            <select
              value={canalSelecionado}
              onChange={(e) =>
                setCanalSelecionado(
                  e.target.value === "__ALL__"
                    ? "__ALL__"
                    : (e.target.value as CanalKey),
                )
              }
              className="w-full rounded-lg border border-red-700/80 bg-red-950/80 px-3 py-2 text-xs text-red-50
                         focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-400"
            >
              <option value="__ALL__">Todos os canais</option>
              {(
                ["site", "youtube", "instagram", "tiktok", "kwai", "facebook", "outros"] as CanalKey[]
              ).map((canal) => (
                <option key={canal} value={canal}>
                  {LABEL_CANAL[canal]}
                </option>
              ))}
            </select>
            <p className="mt-1 text-[10px] text-red-200/80">
              Foco em um único canal ou visão consolidada.
            </p>
          </div>

          {/* Busca */}
          <div>
            <label className="block text-[11px] font-medium text-red-200/80 mb-1">
              Busca rápida
            </label>
            <input
              type="text"
              value={buscaTexto}
              onChange={(e) => setBuscaTexto(e.target.value)}
              placeholder="Filtrar por nome, cliente ou campanha…"
              className="w-full rounded-lg border border-red-700/80 bg-red-950/80 px-3 py-2 text-xs text-red-50 placeholder:text-red-400/70
                         focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-400"
            />
            <p className="mt-1 text-[10px] text-red-200/80">
              Faz uma busca textual nos campos principais do projeto.
            </p>
          </div>
        </div>
      </Card>

      {/* BLOCO 4 – TABELA + RANKING SEGMENTOS */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4 md:gap-5">
        {/* Tabela (ocupa 2/3) */}
        <Card className="bg-red-950/60 border-red-900/70 text-red-50 xl:col-span-2">
          <div className="flex items-center justify-between mb-3">
            <div>
              <div className="text-[10px] uppercase tracking-[0.16em] text-red-200/80">
                Projetos
              </div>
              <div className="mt-1 text-sm font-medium text:white">
                Lista de projetos cadastrados
              </div>
            </div>
            {!loading && (
              <div className="text-[10px] text-red-200/80 text-right">
                Exibindo{" "}
                <span className="font-semibold text-red-50">
                  {projetosFiltrados.length}
                </span>{" "}
                de {totalProjetos} projeto(s)
              </div>
            )}
          </div>

          {erro && (
            <div className="mb-3 rounded-md border border-red-500/60 bg-red-950/80 px-3 py-2 text-[11px] text-red-100">
              {erro}
            </div>
          )}

          {loading ? (
            <div className="text-xs text-red-200/80 py-4">
              Carregando projetos…
            </div>
          ) : projetosFiltrados.length === 0 ? (
            <div className="text-xs text-red-200/80 py-4">
              Nenhum projeto encontrado com os filtros atuais.
            </div>
          ) : (
            <div className="overflow-x-auto rounded-xl border border-red-900/80">
              <table className="min-w-full text-xs">
                <thead className="bg-red-950/90 border-b border-red-900/80">
                  <tr>
                    <th className="px-3 py-2 text-left font-medium text-[11px] text-red-200/80">
                      Projeto
                    </th>
                    <th className="px-3 py-2 text-left font-medium text-[11px] text-red-200/80">
                      Segmento
                    </th>
                    <th className="px-3 py-2 text-left font-medium text-[11px] text-red-200/80">
                      Cliente
                    </th>
                    <th className="px-3 py-2 text-left font-medium text-[11px] text-red-200/80">
                      Canal
                    </th>
                    <th className="px-3 py-2 text-left font-medium text-[11px] text-red-200/80">
                      Publicação
                    </th>
                    <th className="px-3 py-2 text-right font-medium text-[11px] text-red-200/80">
                      Visualizações
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {projetosFiltrados.map((p) => (
                    <tr
                      key={p.id}
                      className="border-b border-red-900/60 hover:bg-red-900/40 transition-colors"
                    >
                      <td className="px-3 py-2 align-top">
                        <div className="text-[11px] font-medium text-white">
                          {p.nome}
                        </div>
                        <div className="text-[10px] text-red-200/80">
                          {p.campanha || "—"}
                        </div>
                        <div className="text-[10px] text-red-400/80">
                          {p.paginaDestino || "—"}
                          {p.tipoConteudo ? ` · ${p.tipoConteudo}` : ""}
                        </div>
                      </td>
                      <td className="px-3 py-2 align-top text-[11px] text-red-100">
                        {p.segmento || "—"}
                      </td>
                      <td className="px-3 py-2 align-top text-[11px] text-red-100">
                        {p.cliente || "—"}
                      </td>
                      <td className="px-3 py-2 align-top text-[11px] text-red-100">
                        {LABEL_CANAL[detectarCanal(p)]}
                      </td>
                      <td className="px-3 py-2 align-top text-[11px] text-red-100">
                        {formatarData(p.dataPublicacao)}
                      </td>
                      <td className="px-3 py-2 align-top text-right text-[11px] text-red-100">
                        {formatarNumero(p.visualizacoes)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>

        {/* Ranking de segmentos (1/3) */}
        <Card className="bg-red-950/60 border-red-900/70 text-red-50">
          <div className="mb-3">
            <div className="text-[10px] uppercase tracking-[0.16em] text-red-200/80">
              Segmentos
            </div>
            <div className="mt-1 text-sm font-medium text-white">
              Top segmentos por volume de projetos
            </div>
            <p className="mt-1 text-[10px] text-red-200/80">
              Ajuda a visualizar rapidamente o foco atual do portfólio.
            </p>
          </div>

          {rankingSegmentos.length === 0 ? (
            <div className="text-xs text-red-200/80">
              Ainda não há dados suficientes para montar o ranking.
            </div>
          ) : (
            <div className="space-y-2">
              {rankingSegmentos.map((item, idx) => {
                const totalSeg = totalProjetos || 1;
                const percentual = (item.qtd / totalSeg) * 100;

                return (
                  <div
                    key={item.segmento + idx}
                    className="rounded-lg border border-red-900/80 bg-red-950/90 px-3 py-2"
                  >
                    <div className="flex items-center justify-between gap-2">
                      <div>
                        <div className="text-[11px] font-medium text-white">
                          {idx + 1}. {item.segmento}
                        </div>
                        <div className="text-[10px] text-red-200/80">
                          {item.qtd} projeto(s) · {formatarNumero(item.views)} views
                        </div>
                      </div>
                      <div className="text-[11px] text-red-200/80">
                        {percentual.toFixed(1)}%
                      </div>
                    </div>
                    <div className="mt-1 h-1.5 w-full rounded-full bg-red-900/60 overflow-hidden">
                      <div
                        className="h-full bg-red-500"
                        style={{ width: `${Math.min(percentual, 100)}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </Card>
      </div>
    </section>
  );
};

export default Dashboard;
