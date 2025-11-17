import { api } from "./api";
import type { Asset, PageIn, PageOut } from "../types/api";

/**
 * Lista Conteúdos Especiais.
 * Busca tudo em /conteudo-especial e pagina/filtra no front por enquanto.
 */
export async function listConteudosEspeciais(
  params: PageIn,
): Promise<PageOut<Asset>> {
  const query = new URLSearchParams();

  // backend espera "search", não "q"
  if (params.q) query.set("search", params.q);
  // plataforma não faz diferença aqui (sempre "site" no backend), então não envio
  if (params.cliente) query.set("cliente", params.cliente);
  // se quiser filtrar por campanha direto na API, podemos reaproveitar:
  // (se não vier, fica só no filtro em memória)
  if ((params as any).campanha) {
    query.set("campanha", (params as any).campanha);
  }

  const qs = query.toString();
  const url = qs ? `/conteudo-especial?${qs}` : "/conteudo-especial";

  // Endpoint simples: retorna array de Asset
  const { data } = await api.get<Asset[]>(url);

  // Paginação/filtragem no front (até criarmos paginação real no backend)
  const page = params.page ?? 1;
  const size = params.size ?? 12;

  let filtered = data;

  // Filtro de busca livre (q)
  if (params.q) {
    const q = params.q.toLowerCase();
    filtered = filtered.filter((a) =>
      [a.titulo, a.cliente, a.campanha, a.segmento]
        .filter(Boolean)
        .some((v) => String(v).toLowerCase().includes(q)),
    );
  }

  // Filtro de plataforma (apesar de ser sempre "site" aqui, deixo o filtro pro caso de reaproveitar o tipo Asset)
  if (params.plataforma) {
    filtered = filtered.filter((a) => a.plataforma === params.plataforma);
  }

  // Filtro por cliente
  if (params.cliente) {
    const c = params.cliente.toLowerCase();
    filtered = filtered.filter((a) =>
      (a.cliente || "").toLowerCase().includes(c),
    );
  }

  // Filtro por data inicial (apenas no front)
  if (params.dt_ini) {
    const ini = new Date(params.dt_ini).getTime();
    filtered = filtered.filter((a) =>
      a.data_publicacao
        ? new Date(a.data_publicacao).getTime() >= ini
        : true,
    );
  }

  // Filtro por data final (apenas no front)
  if (params.dt_fim) {
    const fim = new Date(params.dt_fim).getTime();
    filtered = filtered.filter((a) =>
      a.data_publicacao
        ? new Date(a.data_publicacao).getTime() <= fim
        : true,
    );
  }

  const total = filtered.length;
  const pages = Math.max(1, Math.ceil(total / size));
  const start = (page - 1) * size;
  const items = filtered.slice(start, start + size);

  return { items, page, size, total, pages };
}
