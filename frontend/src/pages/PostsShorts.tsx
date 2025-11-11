import React from "react";
import { useOutletContext } from "react-router-dom";
import type { LayoutContext } from "../types/layout";

export const PostsShorts: React.FC = () => {
  const { isOk } = useOutletContext<LayoutContext>();

  return (
    <section className="space-y-4">
      <div className="flex items-baseline justify-between gap-2">
        <div>
          <h2 className="text-lg font-semibold text-slate-50">
            Posts & Shorts
          </h2>
          <p className="text-[10px] text-slate-500">
            Conteúdos de redes (Instagram, TikTok, Kwai, Shorts) em um só lugar.
          </p>
        </div>
        <button
          className="px-3 py-1.5 rounded-lg bg-emerald-500/90 text-slate-950 text-[10px] font-semibold hover:bg-emerald-400 transition-colors"
          disabled
        >
          + Novo post
        </button>
      </div>

      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 text-[10px] text-slate-400">
        {isOk ? (
          <>
            <p>
              Aqui vamos consumir os endpoints:
              <code className="ml-1 text-emerald-300">
                /post-instagram, /post-tiktok, /post-kwai, /post-youtube-shorts
              </code>
              , unificar em uma grade e permitir filtros por plataforma, cliente
              e campanha.
            </p>
          </>
        ) : (
          <p>
            Aguardando API responder para listar posts. Verifique a aba Dashboard
            para o status da conexão.
          </p>
        )}
      </div>
    </section>
  );
};
