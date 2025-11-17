import { api } from "./api";
import type { Asset, PageIn, PageOut } from "../types/api";

export type PostPlatform = "instagram" | "tiktok" | "kwai" | "youtube_shorts";

/**
 * Mapeia plataforma -> endpoint do backend
 * Alinhado com os routers:
 *   /posts-instagram
 *   /posts-tiktok
 *   /posts-kwai
 *   /posts-youtube-shorts
 */
const endpointByPlatform: Record<PostPlatform, string> = {
  instagram: "/posts-instagram",
  tiktok: "/posts-tiktok",
  kwai: "/posts-kwai",
  youtube_shorts: "/posts-youtube-shorts",
};

export async function listPosts(
  platform: PostPlatform,
  params: PageIn = {},
): Promise<PageOut<Asset>> {
  const endpoint = endpointByPlatform[platform];

  const query = new URLSearchParams();
  // backend espera "search"
  if (params.q) query.set("search", params.q);
  if (params.cliente) query.set("cliente", params.cliente);
  // dt_ini / dt_fim ainda estamos usando só no front
  const url = query.toString() ? `${endpoint}?${query.toString()}` : endpoint;

  const { data } = await api.get<Asset[]>(url);

  // paginação simples no front por enquanto
  const page = params.page ?? 1;
  const size = params.size ?? 12;

  let filtered = data;

  if (params.q) {
    const q = params.q.toLowerCase();
    filtered = filtered.filter((a) =>
      [a.titulo, a.cliente, a.campanha, a.segmento]
        .filter(Boolean)
        .some((v) => String(v).toLowerCase().includes(q)),
    );
  }

  if (params.cliente) {
    const c = params.cliente.toLowerCase();
    filtered = filtered.filter((a) =>
      (a.cliente || "").toLowerCase().includes(c),
    );
  }

  if (params.dt_ini) {
    const ini = new Date(params.dt_ini).getTime();
    filtered = filtered.filter((a) =>
      a.data_publicacao
        ? new Date(a.data_publicacao).getTime() >= ini
        : true,
    );
  }

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
