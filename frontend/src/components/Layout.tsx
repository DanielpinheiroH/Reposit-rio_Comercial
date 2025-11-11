import React, { useEffect, useState } from "react";
import { Outlet, useLocation } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { Header } from "./Header";
import { Footer } from "./Footer";
import { api } from "../lib/api";

type HealthStatus = { status: string };

export const Layout: React.FC = () => {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");

  const location = useLocation();

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

  const isOk = health?.status === "ok" && !error;

  const pageLabelMap: Record<string, string> = {
    "/": "Dashboard",
    "/conteudos-especiais": "Conteúdos especiais",
    "/posts-shorts": "Posts & Shorts",
    "/colecoes": "Coleções",
    "/metricas": "Métricas",
  };

  const currentPageLabel =
    pageLabelMap[location.pathname] || "Dashboard";

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex">
      <Sidebar />
      <div className="flex-1 flex flex-col">
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
      </div>
    </div>
  );
};
