import React, { useState } from "react";
import { NavLink } from "react-router-dom";

const linkBase =
  "px-3 py-2 rounded-lg text-base flex items-center justify-between transition-colors";
const inactive = "text-red-100/80 hover:bg-red-900/40";
const active = "bg-red-900/60 text-white border border-red-800";

const groupHeader =
  "w-full flex items-center justify-between text-sm uppercase tracking-[0.16em] text-red-300/80 px-1 mt-4";

const subBase =
  "mt-1 px-3 py-1.5 rounded-lg text-base flex items-center justify-between transition-colors";
const subInactive = "text-red-100/70 hover:bg-red-900/30";
const subActive = "bg-red-900/70 text-white border border-red-700";

export const Sidebar: React.FC = () => {
  const [openSite, setOpenSite] = useState(true);
  const [openYoutube, setOpenYoutube] = useState(true);
  const [openInstagram, setOpenInstagram] = useState(true);
  const [openTikTok, setOpenTikTok] = useState(true);
  const [openKwai, setOpenKwai] = useState(true);
  const [openFacebook, setOpenFacebook] = useState(true);
  const [openOrg, setOpenOrg] = useState(true);

  return (
    <aside className="w-64 border-r border-red-900 bg-red-950/60 backdrop-blur-sm hidden md:flex flex-col">
      {/* Logo */}
      <div className="px-6 py-6 border-b border-red-900">
        <div className="flex items-center gap-2">
          <div className="h-9 w-9 rounded-xl bg-white flex items-center justify-center text-red-700 font-extrabold text-xl">
            R
          </div>
          <div>
            <h1 className="font-semibold text-base uppercase tracking-[0.16em] text-red-200/80">
              Repositório
            </h1>
            <p className="text-lg font-semibold text-white">
              Comercial
            </p>
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
              <NavLink
                to="/site/todos"
                className={({ isActive }) =>
                  `${subBase} ${isActive ? subActive : subInactive}`
                }
              >
                <span>Todos os conteúdos</span>
              </NavLink>

              <NavLink
                to="/site/publieditorial"
                className={({ isActive }) =>
                  `${subBase} ${isActive ? subActive : subInactive}`
                }
              >
                <span>Publieditorial</span>
              </NavLink>

              <NavLink
                to="/site/publicidade-nativa"
                className={({ isActive }) =>
                  `${subBase} ${isActive ? subActive : subInactive}`
                }
              >
                <span>Publicidade nativa</span>
              </NavLink>

              <NavLink
                to="/site/artigos-opiniao"
                className={({ isActive }) =>
                  `${subBase} ${isActive ? subActive : subInactive}`
                }
              >
                <span>Artigo / opinião digital</span>
              </NavLink>

              <NavLink
                to="/site/manchetes"
                className={({ isActive }) =>
                  `${subBase} ${isActive ? subActive : subInactive}`
                }
              >
                <span>Manchetes</span>
              </NavLink>

              <NavLink
                to="/site/sub-manchetes"
                className={({ isActive }) =>
                  `${subBase} ${isActive ? subActive : subInactive}`
                }
              >
                <span>Sub-manchetes</span>
              </NavLink>
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
              <NavLink
                to="/youtube/lives"
                className={({ isActive }) =>
                  `${subBase} ${isActive ? subActive : subInactive}`
                }
              >
                <span>Lives no YouTube</span>
              </NavLink>

              <NavLink
                to="/youtube/talks"
                className={({ isActive }) =>
                  `${subBase} ${isActive ? subActive : subInactive}`
                }
              >
                <span>YouTube Talks (Big / One / Little)</span>
              </NavLink>

              <NavLink
                to="/youtube/shorts"
                className={({ isActive }) =>
                  `${subBase} ${isActive ? subActive : subInactive}`
                }
              >
                <span>YouTube Shorts</span>
              </NavLink>
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
              <NavLink
                to="/instagram/feed-reels"
                className={({ isActive }) =>
                  `${subBase} ${isActive ? subActive : subInactive}`
                }
              >
                <span>Feed &amp; Reels</span>
              </NavLink>

              <NavLink
                to="/instagram/stories"
                className={({ isActive }) =>
                  `${subBase} ${isActive ? subActive : subInactive}`
                }
              >
                <span>Stories</span>
              </NavLink>
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
              <NavLink
                to="/tiktok/feed"
                className={({ isActive }) =>
                  `${subBase} ${isActive ? subActive : subInactive}`
                }
              >
                <span>Feed / Vídeos curtos</span>
              </NavLink>
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
              <NavLink
                to="/kwai/feed"
                className={({ isActive }) =>
                  `${subBase} ${isActive ? subActive : subInactive}`
                }
              >
                <span>Feed / Vídeos</span>
              </NavLink>
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
              <NavLink
                to="/facebook/feed"
                className={({ isActive }) =>
                  `${subBase} ${isActive ? subActive : subInactive}`
                }
              >
                <span>Feed</span>
              </NavLink>
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
                className={({ isActive }) =>
                  `${subBase} ${isActive ? subActive : subInactive}`
                }
              >
                <span>Coleções</span>
              </NavLink>

              <NavLink
                to="/metricas"
                className={({ isActive }) =>
                  `${subBase} ${isActive ? subActive : subInactive}`
                }
              >
                <span>Métricas</span>
              </NavLink>
            </div>
          )}
        </div>
      </nav>

      {/* Rodapé sidebar */}
      <div className="px-4 py-4 border-t border-red-900 text-sm text-red-200/70">
        v0.1 • ambiente local
      </div>
    </aside>
  );
};
