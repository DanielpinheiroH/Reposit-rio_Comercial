import React from "react";
import { Card } from "../components/ui/Card";

export const Dashboard: React.FC = () => {
  return (
    <section className="space-y-6">
      {/* Bloco 1: boas-vindas */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-5">
        <Card className="bg-red-900/30 border-red-900/60 text-red-50">
          <div className="text-[10px] uppercase tracking-[0.16em] text-red-200/80">
            Visão geral
          </div>
          <div className="text-sm text-white mt-1">
            Bem-vindo ao Repositório Comercial.
          </div>
          <p className="text-[10px] text-red-200/80 mt-1">
            Acompanhe conteúdos especiais, posts, coleções e métricas em um painel único.
          </p>
        </Card>

        <Card className="bg-red-900/20 border-red-900/40 text-red-50">
          <div className="text-[10px] uppercase tracking-[0.16em] text-red-200/80">
            Conteúdos
          </div>
          <div className="mt-1 text-xs font-medium text-white">
            Base estruturada
          </div>
          <p className="mt-1 text-[10px] text-red-200/80">
            Cadastre e consulte ativos por tipo, cliente, campanha, plataforma e tags.
          </p>
        </Card>

        <Card className="bg-white text-red-950 border-red-200">
          <div className="text-[10px] uppercase tracking-[0.16em] text-red-700/80">
            Métricas
          </div>
          <div className="mt-1 text-xs font-medium text-red-900">
            Performance integrada
          </div>
          <p className="mt-1 text-[10px] text-red-700/80">
            Em breve: consolidação de resultados por plataforma.
          </p>
        </Card>
      </div>

      {/* Bloco 2: atalho pra áreas */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 md:gap-5">
        {[
          { title: "Conteúdos especiais", desc: "Matérias, vídeos e páginas especiais." },
          { title: "Posts & Shorts", desc: "Instagram, TikTok, Kwai e YouTube Shorts." },
          { title: "Coleções", desc: "Organização por campanha/tema/segmento." },
          { title: "Métricas", desc: "Visão de performance e evolução." },
        ].map((box) => (
          <Card key={box.title} className="bg-red-900/20 border-red-900/40 text-red-50 hover:bg-red-900/30 transition">
            <div className="text-xs font-medium text-white">{box.title}</div>
            <p className="text-[10px] text-red-200/80 mt-1">{box.desc}</p>
          </Card>
        ))}
      </div>
    </section>
  );
};
