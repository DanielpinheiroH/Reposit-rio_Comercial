import React, { useEffect, useState } from "react";
import axios from "axios";

interface Projeto {
  id: number;
  nome: string;
  paginaDestino?: string | null;
  tipoConteudo?: string | null;
  segmento?: string | null;
  cliente?: string | null;
  campanha?: string | null;
  link?: string | null;
  dataPublicacao?: string | null;
  visualizacoes?: number | null;
  descricao?: string | null;
  created_at: string;
}

export const SitePublieditorial: React.FC = () => {
  const [projetos, setProjetos] = useState<Projeto[]>([]);
  const API = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

  useEffect(() => {
    axios
      .get<Projeto[]>(`${API}/projetos`)
      .then((res) => {
        // FILTRAR APENAS OS PROJETOS RELACIONADOS A "SitePublieditorial"
        const filtrados = res.data.filter((p) =>
          (p.paginaDestino || "").toLowerCase().includes("sitepubli")
        );

        setProjetos(filtrados);
      })
      .catch((err) => {
        console.error("Erro ao carregar projetos:", err);
      });
  }, []);

  return (
    <div className="flex flex-col h-full gap-4">
      <header>
        <h2 className="text-2xl font-semibold text-white">
          Site / Portal · Publieditorial
        </h2>
        <p className="text-sm text-red-200/70">
          Conteúdos de publieditorial publicados no portal.
        </p>
      </header>

      {projetos.length === 0 ? (
        <div className="text-red-100/80 text-sm">
          Nenhum projeto encontrado...
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-3">
          {projetos.map((p) => (
            <div
              key={p.id}
              className="bg-red-900/40 border border-red-700/30 rounded-xl p-4 text-red-50"
            >
              <h3 className="text-lg font-semibold">{p.nome}</h3>
              {p.link && (
                <a
                  href={p.link}
                  target="_blank"
                  className="text-red-300 underline text-sm"
                >
                  {p.link}
                </a>
              )}
              <div className="text-xs opacity-70 mt-2">
                Publicado em: {p.dataPublicacao || "—"}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SitePublieditorial;
