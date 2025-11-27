// frontend/src/lib/projetos.ts
import { api } from "./api";

export type ProjetoOut = {
  id: number;
  nome: string;

  // campos que vêm do backend (schemas.projetos.ProjetoOut)
  paginaDestino?: string | null;
  tipoConteudo?: string | null;
  segmento?: string | null;
  cliente?: string | null;
  campanha?: string | null;
  link?: string | null;
  dataPublicacao?: string | null; // vem como string ISO do backend
  visualizacoes?: number | null;
  descricao?: string | null;

  created_at?: string;
};

export type ProjetoInput = Omit<ProjetoOut, "id" | "created_at">;

// Cria projeto via API /projetos (com fallback em localStorage)
export async function createProjeto(
  payload: ProjetoInput,
): Promise<ProjetoOut> {
  try {
    const { data } = await api.post<ProjetoOut>("/projetos", payload);
    return data;
  } catch (err) {
    console.warn(
      "[projetos] /projetos indisponível na API. Usando fallback em localStorage.",
      err,
    );

    const nowIso = new Date().toISOString();

    const fake: ProjetoOut = {
      id: Date.now(),
      created_at: nowIso,
      ...payload,
    };

    try {
      const raw = window.localStorage.getItem("projetos_fallback");
      const arr: ProjetoOut[] = raw ? JSON.parse(raw) : [];
      arr.push(fake);
      window.localStorage.setItem("projetos_fallback", JSON.stringify(arr));
    } catch (e) {
      console.warn("[projetos] erro ao salvar fallback em localStorage", e);
    }

    return fake;
  }
}

// Lista todos os projetos (GET /projetos) com fallback em localStorage
export async function listProjetos(): Promise<ProjetoOut[]> {
  try {
    const { data } = await api.get<ProjetoOut[]>("/projetos");
    return data;
  } catch (err) {
    console.warn(
      "[projetos] /projetos indisponível na API. Usando fallback em localStorage.",
      err,
    );

    try {
      const raw = window.localStorage.getItem("projetos_fallback");
      if (!raw) return [];
      const arr: ProjetoOut[] = JSON.parse(raw);
      return arr;
    } catch (e) {
      console.warn("[projetos] erro ao ler fallback do localStorage", e);
      return [];
    }
  }
}
