import { api } from "./api";

export type Collection = {
  id: number;
  nome: string;
  descricao?: string | null;
  created_at?: string;
  updated_at?: string;
  // se o backend retornar assets, usamos o length
  assets?: Array<{
    id: number;
    titulo: string;
    plataforma?: string | null;
  }>;
};

export async function listCollections(): Promise<Collection[]> {
  const { data } = await api.get<Collection[]>("/collections");
  return data;
}
