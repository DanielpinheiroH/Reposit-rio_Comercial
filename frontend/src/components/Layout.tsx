import React, { useEffect, useState } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { Header } from "./Header";
import { Footer } from "./Footer";
import { api } from "../lib/api";
import { Modal } from "./ui/Modal";
import { NewProjectModal } from "./NewProjectModal";
import { createProjeto } from "../lib/projetos";

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
        setError("Não consegui falar com o backend. Confere se ele está rodando em http://localhost:8000.");
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
    "/conteudos-especiais": "Conteúdos especiais",
    "/posts-shorts": "Posts & Shorts",
    "/colecoes": "Coleções",
    "/metricas": "Métricas",
  };
  const currentPageLabel = pageLabelMap[location.pathname] || "Dashboard";

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
        <button
          onClick={() => navigate("/projeto/novo")}
          className="
            fixed bottom-6 right-6 z-50
            px-4 py-3 rounded-xl
            border border-red-800
            bg-white text-red-700
            text-xs font-semibold shadow-lg
            hover:bg-red-50 active:scale-[0.98]
          "
          aria-label="Novo Projeto"
          title="Novo Projeto"
        >
          + Novo Projeto
        </button>
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
