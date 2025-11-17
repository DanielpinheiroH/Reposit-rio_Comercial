import React, { useState } from "react";
import { NavLink, Link, useLocation } from "react-router-dom";

const linkBase =
  "px-3 py-2 rounded-lg text-xs flex items-center justify-between transition-colors";
const inactive = "text-red-100/80 hover:bg-red-900/40";
const active = "bg-red-900/60 text-white border border-red-800";

const groupHeader =
  "w-full flex items-center justify-between text-[11px] uppercase tracking-[0.16em] text-red-300/80 px-1 mt-4";

const subBase =
  "mt-1 px-3 py-1.5 rounded-lg text-[11px] flex items-center justify-between transition-colors";
const subInactive = "text-red-100/70 hover:bg-red-900/30";
const subActive = "bg-red-900/70 text-white border border-red-700";

export const Sidebar: React.FC = () => {
  const location = useLocation();

  const [openSite, setOpenSite] = useState(true);
  const [openYoutube, setOpenYoutube] = useState(true);
  const [openInstagram, setOpenInstagram] = useState(true);
  const [openTikTok, setOpenTikTok] = useState(true);
  const [openKwai, setOpenKwai] = useState(true);
  const [openFacebook, setOpenFacebook] = useState(true);
  const [openOrg, setOpenOrg] = useState(true);

  const params = new URLSearchParams(location.search);

  const isConteudoAll = () =>
    location.pathname === "/conteudos-especiais" &&
    !params.get("formato");

  const isConteudoFormato = (formato: string) =>
    location.pathname === "/conteudos-especiais" &&
    params.get("formato") === formato;

  const isPosts = (plataforma: string, tipo?: string) => {
    if (location.pathname !== "/posts-shorts") return false;
    const p = params.get("plataforma");
    const t = params.get("tipo");
    if (!tipo) {
      return p === plataforma;
    }
    return p === plataforma && t === tipo;
  };

  const isColecoes = location.pathname === "/colecoes";
  const isMetricas = location.pathname === "/metricas";

  return (
    <aside className="w-64 border-r border-red-900 bg-red-950/60 backdrop-blur-sm hidden md:flex flex-col">
      {/* Logo */}
      <div className="px-6 py-6 border-b border-red-900">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-xl bg-white flex items-center justify-center text-red-700 font-extrabold text-lg">
            R
          </div>
          <div>
            <h1 className="font-semibold text-sm uppercase tracking-[0.16em] text-red-200/80">
              Repositório
            </h1>
            <p className="text-sm font-medium text-white">Comercial</p>
          </div>
        </div>
      </div>

      {/* Navegação com scroll */}
      <nav className="flex-1 px-4 py-4 space-y-2 overflow-y-auto custom-scroll">
        {/* Dashboard */}
        <div className="space-y-1">
          <NavLink
            to="/"
            end
            className={({ isActive }) =>
              `${linkBase} ${isActive ? active : inactive}`
            }
          >
            <span>Dashboard</span>
            <span className="h-1.5 w-1.5 rounded-full bg-white/90" />
          </NavLink>
        </div>

        {/* SITE / PORTAL */}
        <div>
          <button
            type="button"
            onClick={() => setOpenSite((v) => !v)}
            className={groupHeader}
          >
            <span>Site / Portal</span>
            <span
              className={`transition-transform text-red-200 ${
                openSite ? "rotate-90" : "rotate-0"
              }`}
            >
              ▶
            </span>
          </button>

          {openSite && (
            <div className="mt-1 space-y-0.5">
              <Link
                to="/conteudos-especiais"
                className={
                  subBase +
                  " " +
                  (isConteudoAll() ? subActive : subInactive)
                }
              >
                <span>Todos os conteúdos</span>
              </Link>

              <Link
                to="/conteudos-especiais?formato=publieditorial"
                className={
                  subBase +
                  " " +
                  (isConteudoFormato("publieditorial")
                    ? subActive
                    : subInactive)
                }
              >
                <span>Publieditorial</span>
              </Link>

              <Link
                to="/conteudos-especiais?formato=publicidade_nativa"
                className={
                  subBase +
                  " " +
                  (isConteudoFormato("publicidade_nativa")
                    ? subActive
                    : subInactive)
                }
              >
                <span>Publicidade nativa</span>
              </Link>

              <Link
                to="/conteudos-especiais?formato=expressao_de_opiniao_digital"
                className={
                  subBase +
                  " " +
                  (isConteudoFormato("expressao_de_opiniao_digital")
                    ? subActive
                    : subInactive)
                }
              >
                <span>Artigo / opinião digital</span>
              </Link>

              <Link
                to="/conteudos-especiais?formato=manchete"
                className={
                  subBase +
                  " " +
                  (isConteudoFormato("manchete")
                    ? subActive
                    : subInactive)
                }
              >
                <span>Manchetes</span>
              </Link>

              <Link
                to="/conteudos-especiais?formato=sub_manchete"
                className={
                  subBase +
                  " " +
                  (isConteudoFormato("sub_manchete")
                    ? subActive
                    : subInactive)
                }
              >
                <span>Sub-manchetes</span>
              </Link>
            </div>
          )}
        </div>

        {/* YOUTUBE */}
        <div>
          <button
            type="button"
            onClick={() => setOpenYoutube((v) => !v)}
            className={groupHeader}
          >
            <span>YouTube</span>
            <span
              className={`transition-transform text-red-200 ${
                openYoutube ? "rotate-90" : "rotate-0"
              }`}
            >
              ▶
            </span>
          </button>

          {openYoutube && (
            <div className="mt-1 space-y-0.5">
              <Link
                to="/posts-shorts?plataforma=youtube_shorts"
                className={
                  subBase +
                  " " +
                  (isPosts("youtube_shorts") ? subActive : subInactive)
                }
              >
                <span>YouTube Shorts</span>
              </Link>
            </div>
          )}
        </div>

        {/* INSTAGRAM */}
        <div>
          <button
            type="button"
            onClick={() => setOpenInstagram((v) => !v)}
            className={groupHeader}
          >
            <span>Instagram</span>
            <span
              className={`transition-transform text-red-200 ${
                openInstagram ? "rotate-90" : "rotate-0"
              }`}
            >
              ▶
            </span>
          </button>

          {openInstagram && (
            <div className="mt-1 space-y-0.5">
              <Link
                to="/posts-shorts?plataforma=instagram&tipo=feed_reels"
                className={
                  subBase +
                  " " +
                  (isPosts("instagram", "feed_reels")
                    ? subActive
                    : subInactive)
                }
              >
                <span>Feed &amp; Reels</span>
              </Link>

              <Link
                to="/posts-shorts?plataforma=instagram&tipo=stories"
                className={
                  subBase +
                  " " +
                  (isPosts("instagram", "stories")
                    ? subActive
                    : subInactive)
                }
              >
                <span>Stories</span>
              </Link>
            </div>
          )}
        </div>

        {/* TIKTOK */}
        <div>
          <button
            type="button"
            onClick={() => setOpenTikTok((v) => !v)}
            className={groupHeader}
          >
            <span>TikTok</span>
            <span
              className={`transition-transform text-red-200 ${
                openTikTok ? "rotate-90" : "rotate-0"
              }`}
            >
              ▶
            </span>
          </button>

          {openTikTok && (
            <div className="mt-1 space-y-0.5">
              <Link
                to="/posts-shorts?plataforma=tiktok&tipo=feed"
                className={
                  subBase +
                  " " +
                  (isPosts("tiktok", "feed") ? subActive : subInactive)
                }
              >
                <span>Feed / Vídeos curtos</span>
              </Link>
            </div>
          )}
        </div>

        {/* KWAI */}
        <div>
          <button
            type="button"
            onClick={() => setOpenKwai((v) => !v)}
            className={groupHeader}
          >
            <span>Kwai</span>
            <span
              className={`transition-transform text-red-200 ${
                openKwai ? "rotate-90" : "rotate-0"
              }`}
            >
              ▶
            </span>
          </button>

          {openKwai && (
            <div className="mt-1 space-y-0.5">
              <Link
                to="/posts-shorts?plataforma=kwai&tipo=feed"
                className={
                  subBase +
                  " " +
                  (isPosts("kwai", "feed") ? subActive : subInactive)
                }
              >
                <span>Feed / Vídeos</span>
              </Link>
            </div>
          )}
        </div>

        {/* FACEBOOK */}
        <div>
          <button
            type="button"
            onClick={() => setOpenFacebook((v) => !v)}
            className={groupHeader}
          >
            <span>Facebook</span>
            <span
              className={`transition-transform text-red-200 ${
                openFacebook ? "rotate-90" : "rotate-0"
              }`}
            >
              ▶
            </span>
          </button>

          {openFacebook && (
            <div className="mt-1 space-y-0.5">
              <Link
                to="/posts-shorts?plataforma=facebook&tipo=feed"
                className={
                  subBase +
                  " " +
                  (isPosts("facebook", "feed")
                    ? subActive
                    : subInactive)
                }
              >
                <span>Feed</span>
              </Link>
            </div>
          )}
        </div>

        {/* ORGANIZAÇÃO */}
        <div className="pb-4">
          <button
            type="button"
            onClick={() => setOpenOrg((v) => !v)}
            className={groupHeader}
          >
            <span>Organização</span>
            <span
              className={`transition-transform text-red-200 ${
                openOrg ? "rotate-90" : "rotate-0"
              }`}
            >
              ▶
            </span>
          </button>

          {openOrg && (
            <div className="mt-1 space-y-0.5">
              <NavLink
                to="/colecoes"
                className={
                  subBase +
                  " " +
                  (isColecoes ? subActive : subInactive)
                }
              >
                <span>Coleções</span>
              </NavLink>

              <NavLink
                to="/metricas"
                className={
                  subBase +
                  " " +
                  (isMetricas ? subActive : subInactive)
                }
              >
                <span>Métricas</span>
              </NavLink>
            </div>
          )}
        </div>
      </nav>

      {/* Rodapé sidebar */}
      <div className="px-4 py-4 border-t border-red-900 text-[10px] text-red-200/70">
        v0.1 • ambiente local
      </div>
    </aside>
  );
};
