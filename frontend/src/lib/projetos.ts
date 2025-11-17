// frontend/src/lib/projetos.ts
import { api } from "./api";

export type ProjetoInput = {
  nome: string;
  metaValor?: number | null;
  dataInicio?: string | null; // yyyy-mm-dd
  dataFim?: string | null; // yyyy-mm-dd
  descricao?: string | null;
};

export type ProjetoOut = ProjetoInput & {
  id: number;
  created_at?: string;
};

// Tenta salvar na API /projetos; se não existir, salva em localStorage (dev)
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
    const fake: ProjetoOut = {
      id: Date.now(),
      ...payload,
      created_at: new Date().toISOString(),
    };
    const key = "rc_projetos_dev";
    const arr: ProjetoOut[] = JSON.parse(
      localStorage.getItem(key) || "[]",
    );
    arr.push(fake);
    localStorage.setItem(key, JSON.stringify(arr));
    return fake;
  }
}

// Utilitários opcionais para listar/limpar no dev
export function listProjetosLocal(): ProjetoOut[] {
  const key = "rc_projetos_dev";
  return JSON.parse(localStorage.getItem(key) || "[]");
}

export function clearProjetosLocal() {
  localStorage.removeItem("rc_projetos_dev");
}
