// Tipos compartilhados da API

export type Plataforma =
  | "site"
  | "youtube"
  | "instagram"
  | "tiktok"
  | "kwai"
  | "youtube_shorts"
  | "facebook"; // novo no backend

export type ClassConteudo =
  | "Publicidade"
  | "Nativa"
  | "Artigo de Opinião"
  | "Conteúdo da casa"
  | null;

export type Asset = {
  id: number;
  titulo: string;
  url: string;
  cliente?: string | null;
  campanha?: string | null;
  segmento?: string | null;
  plataforma: Plataforma;
  data_publicacao?: string | null;
  classificacao_conteudo_especial?: ClassConteudo;
  thumbnail_url?: string | null;

  // extras que o backend agora tem (deixo opcionais pra não quebrar nada)
  tipo_asset?: string;
  formato?: string | null;
};

export type PageIn = {
  page?: number; // 1-based
  size?: number; // itens por página
  q?: string; // busca livre
  plataforma?: Plataforma | "";
  cliente?: string;
  dt_ini?: string; // yyyy-mm-dd
  dt_fim?: string; // yyyy-mm-dd
};

export type PageOut<T> = {
  items: T[];
  page: number;
  size: number;
  total: number;
  pages: number;
};
