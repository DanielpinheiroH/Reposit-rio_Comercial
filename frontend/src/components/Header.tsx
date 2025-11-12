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
      {/* Top bar (mobile) — mesma paleta translúcida do footer/sidebar */}
      <div className="md:hidden px-4 py-3 border-b border-red-900 bg-red-950/80 text-red-200/90 backdrop-blur">
        <div className="flex items-center gap-2">
          <div className="h-7 w-7 rounded-xl bg-white flex items-center justify-center text-red-700 text-sm font-bold shadow">
            R
          </div>
          <div>
            <div className="text-[10px] uppercase tracking-[0.16em] opacity-90">
              Repositório Comercial
            </div>
            <div className="text-xs">{currentPageLabel}</div>
          </div>
        </div>
      </div>

      {/* Header principal — igual vibe do footer/sidebar (translúcido, borda suave) */}
      <header className="px-6 pt-4 md:px-10 md:pt-6">
        <div className="rounded-2xl border border-red-900 bg-red-950/80 text-red-200/90 backdrop-blur">
          <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-3 px-4 py-4 md:px-6 md:py-5">
            <div>
              <h2 className="text-xl md:text-2xl font-semibold text-red-50/95">
                Central de Conteúdos
              </h2>
              <p className="text-xs md:text-sm text-red-200/80 mt-1 max-w-lg">
                Visualize, organize e monitore os conteúdos comerciais da equipe em um só lugar.
              </p>
            </div>

            <div className="flex items-center gap-2 text-[10px] md:text-xs">
              <span
                className={`h-2 w-2 rounded-full ${
                  loading ? "bg-red-300/80" : isOk ? "bg-emerald-400" : "bg-red-400"
                }`}
                aria-hidden
              />
              <span className="text-red-200/90">
                API:&nbsp;{apiLabel}
                {!loading && healthStatus && (
                  <span className="opacity-70"> ({healthStatus})</span>
                )}
              </span>
            </div>
          </div>

          {/* Etiqueta da página atual */}
          <div className="px-4 md:px-6 pb-4">
            <span className="inline-flex items-center gap-2 rounded-lg border border-red-900 bg-red-950/60 px-2 py-1 text-[10px] text-red-200/90">
              <span className="h-1.5 w-1.5 rounded-full bg-white/70" />
              {currentPageLabel}
            </span>
          </div>
        </div>
      </header>
    </>
  );
};
