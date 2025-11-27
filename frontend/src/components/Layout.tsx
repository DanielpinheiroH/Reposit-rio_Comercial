import React, { useEffect, useState } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { Header } from "./Header";
import { Footer } from "./Footer";
import { api } from "../lib/api";
import { Modal } from "./ui/Modal";
import { NewProjectModal } from "./NewProjectModal";
import { createProjeto } from "../lib/projetos";
import { NewProjectButton } from "./NewProjectButton";

type HealthStatus = { status: string };

export const Layout: React.FC = () => {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");

  const [openNew, setOpenNew] = useState(false);

  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    async function checkHealth() {
      try {
        const res = await api.get<HealthStatus>("/health");
        setHealth(res.data);
      } catch (err: any) {
        console.error(err);
        setError(
          "Não consegui falar com o backend. Confere se ele está rodando em http://localhost:8000."
        );
      } finally {
        setLoading(false);
      }
    }
    checkHealth();
  }, []);

  // Abre/fecha modal baseado na URL
  useEffect(() => {
    setOpenNew(location.pathname === "/projeto/novo");
  }, [location.pathname]);

  // Bloqueia scroll do body quando o modal está aberto (UX)
  useEffect(() => {
    if (openNew) document.body.classList.add("overflow-hidden");
    else document.body.classList.remove("overflow-hidden");
    return () => document.body.classList.remove("overflow-hidden");
  }, [openNew]);

  const isOk = health?.status === "ok" && !error;

  const pageLabelMap: Record<string, string> = {
    "/": "Dashboard",

    // Site / Portal
    "/site/todos": "Site / Todos os conteúdos",
    "/site/publieditorial": "Site / Publieditorial",
    "/site/publicidade-nativa": "Site / Publicidade nativa",
    "/site/artigo-opiniao-digital": "Site / Artigo / opinião digital",
    "/site/manchetes": "Site / Manchetes",
    "/site/sub-manchetes": "Site / Sub-manchetes",

    // YouTube
    "/youtube/lives": "YouTube / Lives",
    "/youtube/talks": "YouTube / Talks",
    "/youtube/shorts": "YouTube / Shorts",

    // Instagram
    "/instagram/feed-reels": "Instagram / Feed & Reels",
    "/instagram/stories": "Instagram / Stories",

    // TikTok / Kwai / Facebook
    "/tiktok/feed": "TikTok / Feed",
    "/kwai/feed": "Kwai / Feed",
    "/facebook/feed": "Facebook / Feed",

    // Organização
    "/colecoes": "Organização / Coleções",
    "/metricas": "Organização / Métricas",

    // Consolidadas antigas
    "/conteudos-especiais": "Site / Conteúdos especiais (visão única)",
    "/posts-shorts": "Posts & Shorts (visão única)",
  };

  const currentPageLabel =
    pageLabelMap[location.pathname] || "Repositório Comercial";

  function closeNewProjectModal() {
    setOpenNew(false);
    if (location.pathname === "/projeto/novo") {
      if (window.history.length > 1) navigate(-1);
      else navigate("/", { replace: true });
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex">
      <Sidebar />
      <div className="flex-1 flex flex-col relative">
        <Header
          loading={loading}
          isOk={!!isOk}
          healthStatus={health?.status}
          currentPageLabel={currentPageLabel}
        />

        <main className="flex-1 px-6 py-6 md:px-10 md:py-8">
          <Outlet context={{ isOk, loading, error }} />
        </main>

        <Footer />

        {/* Botão flutuante global */}
        <NewProjectButton onClick={() => navigate("/projeto/novo")} />
      </div>

      {/* Modal Novo Projeto */}
      <Modal open={openNew} onClose={closeNewProjectModal} title="Novo Projeto">
        <NewProjectModal
          onClose={closeNewProjectModal}
          onSubmit={async (payload) => {
            const saved = await createProjeto(payload);
            alert(`Projeto criado: ${saved.nome} (id ${saved.id})`);
            closeNewProjectModal();
          }}
        />
      </Modal>
    </div>
  );
};
