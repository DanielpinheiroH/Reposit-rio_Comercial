import React, { useEffect, useState } from "react";
import { listMetrics, type Metric } from "../lib/metrics";

export const Metricas: React.FC = () => {
  const [state, setState] = useState<{loading: boolean; error: string; data: Metric[]}>({
    loading: true,
    error: "",
    data: [],
  });

  useEffect(() => {
    (async () => {
      setState((s) => ({ ...s, loading: true, error: "" }));
      try {
        const data = await listMetrics(50);
        setState({ loading: false, error: "", data });
      } catch (e: any) {
        setState({ loading: false, error: "Falha ao carregar métricas.", data: [] });
      }
    })();
  }, []);

  return (
    <section className="space-y-6">
      <div className="flex items-end justify-between">
        <div>
          <h3 className="text-lg font-semibold text-slate-100">Métricas recentes</h3>
          <p className="text-xs text-slate-500">
            Últimos registros capturados por plataforma.
          </p>
        </div>
        <div className="text-xs text-slate-500">
          {state.loading ? "Carregando…" : `${state.data.length} registros`}
        </div>
      </div>

      {state.error && <div className="text-red-400 text-sm">{state.error}</div>}

      <div className="overflow-auto border border-slate-800 rounded-2xl">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-900/70 text-slate-300">
            <tr>
              <th className="px-3 py-2 border-b border-slate-800">Quando</th>
              <th className="px-3 py-2 border-b border-slate-800">Plataforma</th>
              <th className="px-3 py-2 border-b border-slate-800">Views</th>
              <th className="px-3 py-2 border-b border-slate-800">Likes</th>
              <th className="px-3 py-2 border-b border-slate-800">Comments</th>
              <th className="px-3 py-2 border-b border-slate-800">Shares</th>
              <th className="px-3 py-2 border-b border-slate-800">Reach</th>
              <th className="px-3 py-2 border-b border-slate-800">Engagement</th>
              <th className="px-3 py-2 border-b border-slate-800">Asset ID</th>
            </tr>
          </thead>
          <tbody>
            {state.data.map((m) => (
              <tr key={m.id} className="even:bg-slate-900/40">
                <td className="px-3 py-2 text-slate-300">
                  {new Date(m.capturado_em).toLocaleString()}
                </td>
                <td className="px-3 py-2 text-slate-400">{m.plataforma}</td>
                <td className="px-3 py-2">{m.views ?? "—"}</td>
                <td className="px-3 py-2">{m.likes ?? "—"}</td>
                <td className="px-3 py-2">{m.comments ?? "—"}</td>
                <td className="px-3 py-2">{m.shares ?? "—"}</td>
                <td className="px-3 py-2">{m.reach ?? "—"}</td>
                <td className="px-3 py-2">{m.engagement ?? "—"}</td>
                <td className="px-3 py-2">{m.asset_id}</td>
              </tr>
            ))}
            {!state.loading && state.data.length === 0 && (
              <tr>
                <td colSpan={9} className="px-3 py-6 text-center text-slate-500">
                  Nenhuma métrica encontrada.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
};
