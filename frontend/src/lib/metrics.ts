import { api } from "./api";

export type Metric = {
  id: number;
  asset_id: number;
  plataforma:
    | "site"
    | "youtube"
    | "instagram"
    | "tiktok"
    | "kwai"
    | "youtube_shorts"
    | "facebook";
  capturado_em: string;
  views?: number | null;
  likes?: number | null;
  comments?: number | null;
  shares?: number | null;
  engagement?: number | null;
  reach?: number | null;
  raw_json?: Record<string, unknown> | null;
};

export async function listMetrics(limit = 25): Promise<Metric[]> {
  const { data } = await api.get<Metric[]>("/metrics");
  const ordered = [...data].sort(
    (a, b) =>
      new Date(b.capturado_em).getTime() -
      new Date(a.capturado_em).getTime(),
  );
  return ordered.slice(0, limit);
}
