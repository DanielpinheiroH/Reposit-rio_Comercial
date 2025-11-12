import React, { useEffect, useMemo, useState } from "react";
import { listPosts, type PostPlatform } from "../lib/posts";
import type { Asset, PageIn, PageOut } from "../types/api";

const platformOptions: { label: string; value: PostPlatform }[] = [
  { label: "Instagram", value: "instagram" },
  { label: "TikTok", value: "tiktok" },
  { label: "Kwai", value: "kwai" },
  { label: "YouTube Shorts", value: "youtube_shorts" },
];

export const PostsShorts: React.FC = () => {
  const [platform, setPlatform] = useState<PostPlatform>("instagram");
  const [q, setQ] = useState("");
  const [page, setPage] = useState(1);
  const size = 12;

  const [state, setState] = useState<{
    loading: boolean;
    error: string;
    data: PageOut<Asset> | null;
  }>({ loading: true, error: "", data: null });

  const params = useMemo<PageIn>(() => ({ q, page, size }), [q, page, size]);

  useEffect(() => {
    let mounted = true;
    (async () => {
      setState((s) => ({ ...s, loading: true, error: "" }));
      try {
        const res = await listPosts(platform, params);
        if (!mounted) return;
        setState({ loading: false, error: "", data: res });
      } catch (e: any) {
        if (!mounted) return;
        setState({ loading: false, error: "Falha ao carregar posts.", data: null });
      }
    })();
    return () => {
      mounted = false;
    };
  }, [platform, params]);

  const items = state.data?.items ?? [];

  return (
    <section className="space-y-6">
      {/* Filtros */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4">
        <div className="flex flex-col md:flex-row gap-3 md:items-end">
          <div className="flex-1">
            <label className="text-[10px] uppercase tracking-wider text-slate-500">Plataforma</label>
            <select
              value={platform}
              onChange={(e) => {
                setPlatform(e.target.value as PostPlatform);
                setPage(1);
              }}
              className="mt-1 w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm outline-none"
            >
              {platformOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>

          <div className="flex-1">
            <label className="text-[10px] uppercase tracking-wider text-slate-500">Busca</label>
            <input
              value={q}
              onChange={(e) => {
                setQ(e.target.value);
                setPage(1);
              }}
              placeholder="Título, cliente, campanha..."
              className="mt-1 w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm outline-none"
            />
          </div>

          <div className="text-xs text-slate-500">
            {state.loading
              ? "Carregando…"
              : state.error
              ? "Erro"
              : `${state.data?.total ?? 0} resultados`}
          </div>
        </div>
      </div>

      {/* Lista */}
      {state.error && (
        <div className="text-red-400 text-sm">{state.error}</div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5">
        {items.map((a) => (
          <article
            key={a.id}
            className="bg-slate-900/70 border border-slate-800 rounded-2xl overflow-hidden flex flex-col"
          >
            {a.thumbnail_url && (
              <img src={a.thumbnail_url} alt={a.titulo} className="h-40 w-full object-cover" />
            )}
            <div className="p-4 flex-1 flex flex-col gap-2">
              <div className="text-[10px] uppercase tracking-wider text-slate-500">
                {a.plataforma ?? platform}
              </div>
              <h3 className="text-sm text-slate-100 line-clamp-2">{a.titulo}</h3>
              <p className="text-[11px] text-slate-400 line-clamp-2">{a.campanha || a.cliente}</p>
              <div className="mt-auto text-[10px] text-slate-500">
                {a.data_publicacao ? new Date(a.data_publicacao).toLocaleDateString() : "—"}
              </div>
            </div>
            <div className="p-4 pt-0">
              <a
                href={a.url}
                target="_blank"
                rel="noreferrer"
                className="text-[11px] text-emerald-300 hover:underline"
              >
                Abrir post
              </a>
            </div>
          </article>
        ))}
      </div>

      {/* Paginação */}
      {(state.data?.pages ?? 1) > 1 && (
        <div className="flex items-center justify-center gap-2 text-xs">
          <button
            disabled={page <= 1}
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            className="px-3 py-1 rounded-lg border border-slate-800 disabled:opacity-40"
          >
            Anterior
          </button>
          <span className="text-slate-400">
            Página {page} de {state.data?.pages}
          </span>
          <button
            disabled={page >= (state.data?.pages ?? 1)}
            onClick={() => setPage((p) => p + 1)}
            className="px-3 py-1 rounded-lg border border-slate-800 disabled:opacity-40"
          >
            Próxima
          </button>
        </div>
      )}
    </section>
  );
};
