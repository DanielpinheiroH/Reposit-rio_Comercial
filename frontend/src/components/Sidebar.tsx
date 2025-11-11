import React from "react";
import { NavLink } from "react-router-dom";

const linkBase =
  "px-3 py-2 rounded-lg text-xs flex items-center justify-between transition-colors";
const inactive =
  "text-slate-500 hover:bg-slate-900/60";
const disabled =
  "cursor-not-allowed opacity-40";
const active =
  "bg-slate-900/80 text-emerald-400";

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-950/60 backdrop-blur-sm hidden md:flex flex-col">
      {/* Logo */}
      <div className="px-6 py-6 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-xl bg-emerald-500/90 flex items-center justify-center text-slate-950 font-extrabold text-lg">
            R
          </div>
          <div>
            <h1 className="font-semibold text-sm uppercase tracking-[0.16em] text-slate-400">
              Repositório
            </h1>
            <p className="text-sm font-medium text-slate-100">Comercial</p>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-4 py-4 space-y-1">
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            `${linkBase} ${isActive ? active : inactive}`
          }
        >
          <span>Dashboard</span>
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
        </NavLink>

        <NavLink
          to="/conteudos-especiais"
          className={({ isActive }) =>
            `${linkBase} ${isActive ? active : inactive}`
          }
        >
          <span>Conteúdos especiais</span>
        </NavLink>

        <NavLink
          to="/posts-shorts"
          className={({ isActive }) =>
            `${linkBase} ${isActive ? active : inactive}`
          }
        >
          <span>Posts & Shorts</span>
        </NavLink>

        <NavLink
          to="/colecoes"
          className={({ isActive }) =>
            `${linkBase} ${isActive ? active : inactive}`
          }
        >
          <span>Coleções</span>
        </NavLink>

        <NavLink
          to="/metricas"
          className={({ isActive }) =>
            `${linkBase} ${isActive ? active : inactive}`
          }
        >
          <span>Métricas</span>
        </NavLink>
      </nav>

      {/* Rodapé sidebar */}
      <div className="px-4 py-4 border-t border-slate-800 text-[10px] text-slate-500">
        v0.1 • ambiente local
      </div>
    </aside>
  );
};
