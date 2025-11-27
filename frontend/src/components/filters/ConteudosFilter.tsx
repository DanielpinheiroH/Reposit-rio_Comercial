import React, { useMemo } from "react";
import type { Plataforma } from "../../types/api";

type Props = {
  q: string;
  setQ: (v: string) => void;
  plataforma: Plataforma | "";
  setPlataforma: (v: Plataforma | "") => void;
  cliente: string;
  setCliente: (v: string) => void;
  dtIni: string;
  setDtIni: (v: string) => void;
  dtFim: string;
  setDtFim: (v: string) => void;
  onApply?: () => void;
  onClear?: () => void;
};

export const ConteudosFilter: React.FC<Props> = ({
  q,
  setQ,
  plataforma,
  setPlataforma,
  cliente,
  setCliente,
  dtIni,
  setDtIni,
  dtFim,
  setDtFim,
  onApply,
  onClear,
}) => {
  const options = useMemo<Plataforma[]>(
    () => [
      "site",
      "youtube",
      "instagram",
      "tiktok",
      "kwai",
      "youtube_shorts",
      "facebook",
    ],
    []
  );

  return (
    <div className="bg-red-950/60 border border-red-900 rounded-2xl p-3 md:p-4 space-y-3">
      <div className="grid grid-cols-1 md:grid-cols-5 gap-2">
        <input
          className="
            bg-red-950
            border border-red-900/70
            rounded-lg
            px-3 py-2
            text-xs text-red-50
            placeholder-red-300/70
            outline-none
            focus:ring-2 focus:ring-red-500/60 focus:border-red-500
          "
          placeholder="Buscar por título, campanha, segmento..."
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />

        <select
          className="
            bg-red-950
            border border-red-900/70
            rounded-lg
            px-3 py-2
            text-xs text-red-50
            outline-none
            focus:ring-2 focus:ring-red-500/60 focus:border-red-500
          "
          value={plataforma}
          onChange={(e) => setPlataforma(e.target.value as Plataforma | "")}
        >
          <option value="">Plataforma (todas)</option>
          {options.map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>

        <input
          className="
            bg-red-950
            border border-red-900/70
            rounded-lg
            px-3 py-2
            text-xs text-red-50
            placeholder-red-300/70
            outline-none
            focus:ring-2 focus:ring-red-500/60 focus:border-red-500
          "
          placeholder="Cliente"
          value={cliente}
          onChange={(e) => setCliente(e.target.value)}
        />

        <input
          type="date"
          className="
            bg-red-950
            border border-red-900/70
            rounded-lg
            px-3 py-2
            text-xs text-red-50
            outline-none
            focus:ring-2 focus:ring-red-500/60 focus:border-red-500
          "
          value={dtIni}
          onChange={(e) => setDtIni(e.target.value)}
        />

        <input
          type="date"
          className="
            bg-red-950
            border border-red-900/70
            rounded-lg
            px-3 py-2
            text-xs text-red-50
            outline-none
            focus:ring-2 focus:ring-red-500/60 focus:border-red-500
          "
          value={dtFim}
          onChange={(e) => setDtFim(e.target.value)}
        />
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={onApply}
          className="
            px-3 py-1.5 rounded-lg
            bg-red-600
            text-slate-50 text-[10px] font-semibold
            hover:bg-red-500
            transition-colors
          "
        >
          Aplicar
        </button>
        <button
          onClick={onClear}
          className="
            px-3 py-1.5 rounded-lg
            border border-red-900/70
            text-red-100 text-[10px]
            hover:bg-red-900/60
            transition-colors
          "
        >
          Limpar
        </button>
      </div>
    </div>
  );
};
