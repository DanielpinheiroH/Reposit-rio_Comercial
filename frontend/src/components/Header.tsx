import React from "react";

type HeaderProps = {
  loading: boolean;
  isOk: boolean;
  healthStatus?: string;
  currentPageLabel?: string;
};

export const Header: React.FC<HeaderProps> = ({
  loading,
  isOk,
  healthStatus,
  currentPageLabel = "Dashboard",
}) => {
  const apiLabel = loading
    ? "checando..."
    : isOk
    ? "online e respondendo"
    : "indisponível";

  return (
    <>
      {/* Top bar mobile */}
      <div className="md:hidden px-4 py-3 border-b border-slate-800 flex items-center gap-2 bg-slate-950/80 backdrop-blur">
        <div className="h-7 w-7 rounded-xl bg-emerald-500/90 flex items-center justify-center text-slate-950 text-sm font-bold">
          R
        </div>
        <div>
          <div className="text-[10px] uppercase text-slate-500 tracking-[0.16em]">
            Repositório Comercial
          </div>
          <div className="text-xs text-slate-300">{currentPageLabel}</div>
        </div>
      </div>

      {/* Header principal */}
      <header className="px-6 pt-4 md:px-10 md:pt-6 flex flex-col md:flex-row md:items-end md:justify-between gap-3">
        <div>
          <h2 className="text-xl md:text-2xl font-semibold text-slate-50">
            Central de Conteúdos
          </h2>
          <p className="text-xs md:text-sm text-slate-400 mt-1 max-w-lg">
            Visualize, organize e monitore os conteúdos comerciais da equipe em um só lugar.
          </p>
        </div>

        <div className="flex items-center gap-2 text-[10px] md:text-xs">
          <span
            className={`h-2 w-2 rounded-full ${
              loading ? "bg-slate-500" : isOk ? "bg-emerald-400" : "bg-red-500"
            }`}
          />
          <span className="text-slate-400">
            API:&nbsp;{apiLabel}
            {!loading && healthStatus && (
              <span className="text-slate-500"> ({healthStatus})</span>
            )}
          </span>
        </div>
      </header>
    </>
  );
};
