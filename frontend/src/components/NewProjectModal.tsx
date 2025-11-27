import React, { useMemo, useState } from "react";

type NewProjectModalProps = {
  onClose: () => void;
  onSubmit?: (payload: {
    nome: string;
    dataPublicacao?: string | null;  // yyyy-mm-dd
    descricao?: string | null;

    canal?: string | null;           // site, youtube, instagram...
    tipo?: string | null;            // publieditorial, talks, feed_reels...
    segmento?: string | null;        // política, saúde, gastronomia...
    visualizacoes?: number | null;   // quantidade de views
    link?: string | null;            // URL do conteúdo / doc / etc
  }) => Promise<void> | void;
};

export const NewProjectModal: React.FC<NewProjectModalProps> = ({
  onClose,
  onSubmit,
}) => {
  const [nome, setNome] = useState("");
  const [descricao, setDescricao] = useState("");
  const [dataPublicacao, setDataPublicacao] = useState<string>("");

  const [canal, setCanal] = useState<string>("");
  const [tipo, setTipo] = useState<string>("");
  const [segmento, setSegmento] = useState<string>("");
  const [visualizacoes, setVisualizacoes] = useState<number | "">("");
  const [link, setLink] = useState<string>("");

  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState<string>("");

  // Opções de canal/página — alinhado com a sidebar
  const canalOptions = useMemo(
    () => [
      { value: "site", label: "Site / Portal" },
      { value: "youtube", label: "YouTube" },
      { value: "instagram", label: "Instagram" },
      { value: "tiktok", label: "TikTok" },
      { value: "kwai", label: "Kwai" },
      { value: "facebook", label: "Facebook" },
    ],
    []
  );

  // Opções de tipo dentro do canal
  const tipoOptions = useMemo(() => {
    switch (canal) {
      case "site":
        return [
          { value: "todos", label: "Todos os conteúdos" },
          { value: "publieditorial", label: "Publieditorial" },
          { value: "publicidade_nativa", label: "Publicidade nativa" },
          {
            value: "expressao_de_opiniao_digital",
            label: "Artigo / opinião digital",
          },
          { value: "manchete", label: "Manchetes" },
          { value: "sub_manchete", label: "Sub-manchetes" },
        ];
      case "youtube":
        return [
          { value: "live", label: "Lives no YouTube" },
          { value: "talks", label: "YouTube Talks (Big / One / Little)" },
          { value: "shorts", label: "YouTube Shorts" },
        ];
      case "instagram":
        return [
          { value: "feed_reels", label: "Feed & Reels" },
          { value: "stories", label: "Stories" },
        ];
      case "tiktok":
        return [{ value: "feed", label: "Feed / Vídeos curtos" }];
      case "kwai":
        return [{ value: "feed", label: "Feed / Vídeos" }];
      case "facebook":
        return [{ value: "feed", label: "Feed" }];
      default:
        return [];
    }
  }, [canal]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErr("");

    if (!nome.trim()) {
      setErr("Informe um nome para o projeto.");
      return;
    }

    if (!canal) {
      setErr("Selecione em qual página/canal esse projeto se encaixa.");
      return;
    }

    try {
      setSaving(true);
      await onSubmit?.({
        nome: nome.trim(),
        descricao: descricao.trim() || null,
        dataPublicacao: dataPublicacao || null,

        canal: canal || null,
        tipo: tipo || null,
        segmento: segmento.trim() || null,
        visualizacoes:
          visualizacoes === "" ? null : Number(visualizacoes),
        link: link.trim() || null,
      });

      // reset
      setNome("");
      setDescricao("");
      setDataPublicacao("");
      setCanal("");
      setTipo("");
      setSegmento("");
      setVisualizacoes("");
      setLink("");

      onClose();
    } catch (e: any) {
      console.error(e);
      setErr("Não foi possível salvar. Tente novamente.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {/* Nome do projeto */}
        <div className="col-span-1 md:col-span-2">
          <label className="block text-[11px] font-medium text-red-200 mb-1">
            Nome do projeto *
          </label>
          <input
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            className="
              w-full rounded-lg
              border border-red-900/70
              bg-red-950/70
              px-3 py-2
              text-sm text-red-50
              placeholder-red-300/60
              outline-none
              focus:ring-2 focus:ring-red-500/60 focus:border-red-500
            "
            placeholder="Ex.: Projeto Especial Black Friday"
          />
        </div>

        {/* Canal / Página */}
        <div>
          <label className="block text-[11px] font-medium text-red-200 mb-1">
            Canal / Página *
          </label>
          <select
            value={canal}
            onChange={(e) => {
              setCanal(e.target.value);
              setTipo("");
            }}
            className="
              w-full rounded-lg
              border border-red-900/70
              bg-red-950/70
              px-3 py-2
              text-sm text-red-50
              outline-none
              focus:ring-2 focus:ring-red-500/60 focus:border-red-500
            "
          >
            <option value="">Selecione…</option>
            {canalOptions.map((c) => (
              <option key={c.value} value={c.value}>
                {c.label}
              </option>
            ))}
          </select>
        </div>

        {/* Tipo dentro do canal */}
        <div>
          <label className="block text-[11px] font-medium text-red-200 mb-1">
            Tipo dentro do canal
          </label>
          <select
            value={tipo}
            onChange={(e) => setTipo(e.target.value)}
            disabled={!canal || tipoOptions.length === 0}
            className="
              w-full rounded-lg
              border border-red-900/70
              bg-red-950/70
              px-3 py-2
              text-sm text-red-50
              outline-none
              disabled:opacity-50 disabled:cursor-not-allowed
              focus:ring-2 focus:ring-red-500/60 focus:border-red-500
            "
          >
            <option value="">
              {canal
                ? "Selecione o tipo (opcional)…"
                : "Selecione um canal primeiro"}
            </option>
            {tipoOptions.map((t) => (
              <option key={t.value} value={t.value}>
                {t.label}
              </option>
            ))}
          </select>
        </div>

        {/* Visualizações */}
        <div>
          <label className="block text-[11px] font-medium text-red-200 mb-1">
            Visualizações
          </label>
          <input
            type="number"
            min="0"
            step="1"
            value={visualizacoes}
            onChange={(e) =>
              setVisualizacoes(
                e.target.value === "" ? "" : Number(e.target.value)
              )
            }
            className="
              w-full rounded-lg
              border border-red-900/70
              bg-red-950/70
              px-3 py-2
              text-sm text-red-50
              placeholder-red-300/60
              outline-none
              focus:ring-2 focus:ring-red-500/60 focus:border-red-500
            "
            placeholder="Ex.: 120000"
          />
        </div>

        {/* Segmento */}
        <div>
          <label className="block text-[11px] font-medium text-red-200 mb-1">
            Segmento
          </label>
          <input
            value={segmento}
            onChange={(e) => setSegmento(e.target.value)}
            className="
              w-full rounded-lg
              border border-red-900/70
              bg-red-950/70
              px-3 py-2
              text-sm text-red-50
              placeholder-red-300/60
              outline-none
              focus:ring-2 focus:ring-red-500/60 focus:border-red-500
            "
            placeholder="Ex.: política, saúde, gastronomia…"
          />
        </div>

        {/* Data da publicação */}
        <div>
          <label className="block text-[11px] font-medium text-red-200 mb-1">
            Data da publicação
          </label>
          <input
            type="date"
            value={dataPublicacao}
            onChange={(e) => setDataPublicacao(e.target.value)}
            className="
              w-full rounded-lg
              border border-red-900/70
              bg-red-950/70
              px-3 py-2
              text-sm text-red-50
              outline-none
              focus:ring-2 focus:ring-red-500/60 focus:border-red-500
            "
          />
        </div>

        {/* Link */}
        <div className="md:col-span-2">
          <label className="block text-[11px] font-medium text-red-200 mb-1">
            Link (URL)
          </label>
          <input
            value={link}
            onChange={(e) => setLink(e.target.value)}
            className="
              w-full rounded-lg
              border border-red-900/70
              bg-red-950/70
              px-3 py-2
              text-sm text-red-50
              placeholder-red-300/60
              outline-none
              focus:ring-2 focus:ring-red-500/60 focus:border-red-500
            "
            placeholder="https://..."
          />
        </div>

        {/* Descrição */}
        <div className="md:col-span-2">
          <label className="block text-[11px] font-medium text-red-200 mb-1">
            Descrição
          </label>
          <textarea
            rows={4}
            value={descricao}
            onChange={(e) => setDescricao(e.target.value)}
            className="
              w-full rounded-lg
              border border-red-900/70
              bg-red-950/70
              px-3 py-2
              text-sm text-red-50
              placeholder-red-300/60
              outline-none
              focus:ring-2 focus:ring-red-500/60 focus:border-red-500
              resize-y
            "
            placeholder="Resumo do projeto, objetivos, observações…"
          />
        </div>
      </div>

      {err && (
        <div className="text-[11px] text-red-100 bg-red-950/80 border border-red-800 rounded-lg px-3 py-2">
          {err}
        </div>
      )}

      <div className="flex items-center justify-end gap-2 pt-1">
        <button
          type="button"
          onClick={onClose}
          className="
            px-3 py-2 rounded-lg
            border border-red-900/70
            bg-red-950/70
            text-red-100 text-xs
            hover:bg-red-900/70
            transition-colors
          "
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={saving}
          className="
            px-3 py-2 rounded-lg
            border border-red-800
            bg-white text-red-700
            text-xs font-semibold
            hover:bg-red-50
            disabled:opacity-50 disabled:cursor-not-allowed
            transition-colors
          "
        >
          {saving ? "Salvando…" : "Salvar projeto"}
        </button>
      </div>
    </form>
  );
};
