import React, { useState } from "react";

type NewProjectModalProps = {
  open: boolean;
  onClose: () => void;
  onSubmit?: (payload: {
    nome: string;
    metaValor?: number | null;
    dataInicio?: string | null; // yyyy-mm-dd
    dataFim?: string | null;    // yyyy-mm-dd
    descricao?: string | null;
  }) => Promise<void> | void;
};

export const NewProjectModal: React.FC<NewProjectModalProps> = ({
  open,
  onClose,
  onSubmit,
}) => {
  const [nome, setNome] = useState("");
  const [descricao, setDescricao] = useState("");
  const [metaValor, setMetaValor] = useState<number | "">("");
  const [dataInicio, setDataInicio] = useState<string>("");
  const [dataFim, setDataFim] = useState<string>("");
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState<string>("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErr("");

    if (!nome.trim()) {
      setErr("Informe um nome para o projeto.");
      return;
    }

    try {
      setSaving(true);
      await onSubmit?.({
        nome: nome.trim(),
        descricao: descricao.trim() || null,
        metaValor: metaValor === "" ? null : Number(metaValor),
        dataInicio: dataInicio || null,
        dataFim: dataFim || null,
      });
      onClose();
      // reset opcional
      setNome("");
      setDescricao("");
      setMetaValor("");
      setDataInicio("");
      setDataFim("");
    } catch (e: any) {
      console.error(e);
      setErr("Não foi possível salvar. Tente novamente.");
    } finally {
      setSaving(false);
    }
  }

  // Reaproveita estrutura visual do Modal via composition
  return (
    <div className={open ? "" : "hidden"}>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div className="col-span-1 md:col-span-2">
            <label className="block text-[11px] font-medium text-red-200 mb-1">
              Nome do projeto *
            </label>
            <input
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              className="w-full rounded-lg border border-red-900/60 bg-red-900/30 px-3 py-2 text-sm text-red-50 placeholder-red-200/50 outline-none focus:ring-2 focus:ring-red-400/40"
              placeholder="Ex.: Projeto Especial Black Friday"
            />
          </div>

          <div>
            <label className="block text-[11px] font-medium text-red-200 mb-1">
              Meta (R$)
            </label>
            <input
              type="number"
              min="0"
              step="0.01"
              value={metaValor}
              onChange={(e) => setMetaValor(e.target.value === "" ? "" : Number(e.target.value))}
              className="w-full rounded-lg border border-red-900/60 bg-red-900/30 px-3 py-2 text-sm text-red-50 placeholder-red-200/50 outline-none focus:ring-2 focus:ring-red-400/40"
              placeholder="Ex.: 500000"
            />
          </div>

          <div>
            <label className="block text-[11px] font-medium text-red-200 mb-1">
              Início
            </label>
            <input
              type="date"
              value={dataInicio}
              onChange={(e) => setDataInicio(e.target.value)}
              className="w-full rounded-lg border border-red-900/60 bg-red-900/30 px-3 py-2 text-sm text-red-50 outline-none focus:ring-2 focus:ring-red-400/40"
            />
          </div>

          <div>
            <label className="block text-[11px] font-medium text-red-200 mb-1">
              Fim
            </label>
            <input
              type="date"
              value={dataFim}
              onChange={(e) => setDataFim(e.target.value)}
              className="w-full rounded-lg border border-red-900/60 bg-red-900/30 px-3 py-2 text-sm text-red-50 outline-none focus:ring-2 focus:ring-red-400/40"
            />
          </div>

          <div className="md:col-span-2">
            <label className="block text-[11px] font-medium text-red-200 mb-1">
              Descrição
            </label>
            <textarea
              rows={4}
              value={descricao}
              onChange={(e) => setDescricao(e.target.value)}
              className="w-full rounded-lg border border-red-900/60 bg-red-900/30 px-3 py-2 text-sm text-red-50 placeholder-red-200/50 outline-none focus:ring-2 focus:ring-red-400/40 resize-y"
              placeholder="Resumo do projeto, objetivos, observações…"
            />
          </div>
        </div>

        {err && (
          <div className="text-[11px] text-red-200 bg-red-900/50 border border-red-900/60 rounded-lg px-3 py-2">
            {err}
          </div>
        )}

        <div className="flex items-center justify-end gap-2 pt-1">
          <button
            type="button"
            onClick={onClose}
            className="px-3 py-2 rounded-lg border border-red-900/60 bg-red-900/30 text-red-100 text-xs hover:bg-red-900/50"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={saving}
            className="px-3 py-2 rounded-lg border border-red-800 bg-white text-red-700 text-xs font-semibold hover:bg-red-50 disabled:opacity-50"
          >
            {saving ? "Salvando…" : "Salvar projeto"}
          </button>
        </div>
      </form>
    </div>
  );
};
