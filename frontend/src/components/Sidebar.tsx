import React from "react";
import { NavLink } from "react-router-dom";

const linkBase =
  "px-3 py-2 rounded-lg text-xs flex items-center justify-between transition-colors";
const inactive = "text-red-100/80 hover:bg-red-900/40";
const active =
  "bg-red-900/60 text-white border border-red-800";

export const Sidebar: React.FC = () => {
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

      {/* Nav */}
      <nav className="flex-1 px-4 py-4 space-y-1">
        <NavLink to="/" end className={({ isActive }) => `${linkBase} ${isActive ? active : inactive}`}>
          <span>Dashboard</span>
          <span className="h-1.5 w-1.5 rounded-full bg-white/90" />
        </NavLink>

        <NavLink to="/conteudos-especiais" className={({ isActive }) => `${linkBase} ${isActive ? active : inactive}`}>
          <span>Conteúdos especiais</span>
        </NavLink>

        <NavLink to="/posts-shorts" className={({ isActive }) => `${linkBase} ${isActive ? active : inactive}`}>
          <span>Posts & Shorts</span>
        </NavLink>

        <NavLink to="/colecoes" className={({ isActive }) => `${linkBase} ${isActive ? active : inactive}`}>
          <span>Coleções</span>
        </NavLink>

        <NavLink to="/metricas" className={({ isActive }) => `${linkBase} ${isActive ? active : inactive}`}>
          <span>Métricas</span>
        </NavLink>
      </nav>

      {/* Rodapé sidebar */}
      <div className="px-4 py-4 border-t border-red-900 text-[10px] text-red-200/70">
        v0.1 • ambiente local
      </div>
    </aside>
  );
};
