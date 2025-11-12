import { api } from "./api";
import type { Asset, PageIn, PageOut } from "../types/api";

/**
 * Lista Conteúdos Especiais.
 * Busca tudo em /conteudo-especial e pagina/filtra no front por enquanto.
 */
export async function listConteudosEspeciais(params: PageIn): Promise<PageOut<Asset>> {
  const query = new URLSearchParams();
  if (params.q) query.set("q", params.q);
  if (params.plataforma) query.set("plataforma", params.plataforma);
  if (params.cliente) query.set("cliente", params.cliente);
  if (params.dt_ini) query.set("dt_ini", params.dt_ini);
  if (params.dt_fim) query.set("dt_fim", params.dt_fim);

  // Endpoint simples: retorna array de Asset
  const { data } = await api.get<Asset[]>(`/conteudo-especial?${query.toString()}`);

  // Paginação/filtragem no front (até criarmos paginação real no backend)
  const page = params.page ?? 1;
  const size = params.size ?? 12;

  let filtered = data;

  if (params.q) {
    const q = params.q.toLowerCase();
    filtered = filtered.filter((a) =>
      [a.titulo, a.cliente, a.campanha, a.segmento]
        .filter(Boolean)
        .some((v) => String(v).toLowerCase().includes(q))
    );
  }

  if (params.plataforma) {
    filtered = filtered.filter((a) => a.plataforma === params.plataforma);
  }

  if (params.cliente) {
    const c = params.cliente.toLowerCase();
    filtered = filtered.filter((a) => (a.cliente || "").toLowerCase().includes(c));
  }

  if (params.dt_ini) {
    const ini = new Date(params.dt_ini).getTime();
    filtered = filtered.filter((a) =>
      a.data_publicacao ? new Date(a.data_publicacao).getTime() >= ini : true
    );
  }

  if (params.dt_fim) {
    const fim = new Date(params.dt_fim).getTime();
    filtered = filtered.filter((a) =>
      a.data_publicacao ? new Date(a.data_publicacao).getTime() <= fim : true
    );
  }

  const total = filtered.length;
  const pages = Math.max(1, Math.ceil(total / size));
  const start = (page - 1) * size;
  const items = filtered.slice(start, start + size);

  return { items, page, size, total, pages };
}
