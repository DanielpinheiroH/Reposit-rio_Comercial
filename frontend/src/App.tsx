import { useEffect, useState } from "react";
import { api } from "./lib/api";

type HealthStatus = {
  status: string;
};

function App() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    async function checkHealth() {
      try {
        const res = await api.get<HealthStatus>("/health");
        setHealth(res.data);
      } catch (err: any) {
        console.error(err);
        setError("Não consegui falar com o backend. Confere se ele está rodando em http://localhost:8000.");
      } finally {
        setLoading(false);
      }
    }

    checkHealth();
  }, []);

  const isOk = health?.status === "ok" && !error;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex">
      {/* Sidebar */}
      <aside className="w-64 border-r border-slate-800 bg-slate-950/60 backdrop-blur-sm hidden md:flex flex-col">
        <div className="px-6 py-6 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-xl bg-emerald-500/90 flex items-center justify-center text-slate-950 font-extrabold text-lg">
              R
            </div>
            <div>
              <h1 className="font-semibold text-sm uppercase tracking-[0.16em] text-slate-400">
                Repositório
              </h1>
              <p className="text-sm font-medium text-slate-100">Comercial</p>
            </div>
          </div>
        </div>

        <nav className="flex-1 px-4 py-4 text-xs text-slate-400 space-y-1">
          <div className="px-3 py-2 rounded-lg bg-slate-900/80 text-emerald-400 font-medium flex items-center justify-between">
            <span>Dashboard</span>
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
          </div>
          <div className="px-3 py-2 rounded-lg hover:bg-slate-900/60 cursor-not-allowed opacity-40">
            Conteúdos especiais
          </div>
          <div className="px-3 py-2 rounded-lg hover:bg-slate-900/60 cursor-not-allowed opacity-40">
            Posts & Shorts
          </div>
          <div className="px-3 py-2 rounded-lg hover:bg-slate-900/60 cursor-not-allowed opacity-40">
            Coleções
          </div>
          <div className="px-3 py-2 rounded-lg hover:bg-slate-900/60 cursor-not-allowed opacity-40">
            Métricas
          </div>
        </nav>

        <div className="px-4 py-4 border-t border-slate-800 text-[10px] text-slate-500">
          v0.1 • ambiente local
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 flex flex-col">
        {/* Top bar (mobile title) */}
        <div className="md:hidden px-4 py-3 border-b border-slate-800 flex items-center gap-2 bg-slate-950/80 backdrop-blur">
          <div className="h-7 w-7 rounded-xl bg-emerald-500/90 flex items-center justify-center text-slate-950 text-sm font-bold">
            R
          </div>
          <div>
            <div className="text-[10px] uppercase text-slate-500 tracking-[0.16em]">
              Repositório Comercial
            </div>
            <div className="text-xs text-slate-300">
              Dashboard
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 px-6 py-6 md:px-10 md:py-8 space-y-6">
          {/* Header */}
          <header className="flex flex-col md:flex-row md:items-end md:justify-between gap-3">
            <div>
              <h2 className="text-xl md:text-2xl font-semibold text-slate-50">
                Central de Conteúdos
              </h2>
              <p className="text-xs md:text-sm text-slate-400 mt-1 max-w-lg">
                Visualize, organize e monitore os conteúdos comerciais da equipe em um só lugar.
              </p>
            </div>

            <div className="flex items-center gap-2 text-[10px] md:text-xs">
              <span
                className={`h-2 w-2 rounded-full ${
                  isOk ? "bg-emerald-400" : "bg-red-500"
                }`}
              />
              <span className="text-slate-400">
                API:&nbsp;
                {loading
                  ? "checando..."
                  : isOk
                  ? "online e respondendo"
                  : "indisponível"}
              </span>
            </div>
          </header>

          {/* Grid cards */}
          <section className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-5">
            {/* Status card */}
            <div className="col-span-1 md:col-span-1 bg-slate-900/70 border border-slate-800 rounded-2xl p-4 flex flex-col gap-2">
              <div className="text-[10px] uppercase tracking-[0.16em] text-slate-500">
                Status do backend
              </div>
              <div className="flex items-baseline gap-2">
                <span
                  className={`font-semibold text-sm ${
                    isOk ? "text-emerald-400" : "text-red-400"
                  }`}
                >
                  {loading
                    ? "Checando..."
                    : isOk
                    ? "OK"
                    : "Offline / erro"}
                </span>
                {!loading && health && (
                  <span className="text-[10px] text-slate-500">
                    ({health.status})
                  </span>
                )}
              </div>
              {error && (
                <p className="text-[10px] text-red-400 mt-1 leading-relaxed">
                  {error}
                </p>
              )}
              {!error && !loading && (
                <p className="text-[10px] text-slate-500 mt-1 leading-relaxed">
                  Conexão estabelecida com <code className="text-emerald-300">/api/health</code>.
                  Pronto para listar conteúdos reais.
                </p>
              )}
            </div>

            {/* Placeholder cards pra próximos recursos */}
            <div className="bg-slate-900/40 border border-slate-800/60 rounded-2xl p-4 flex flex-col justify-between">
              <div>
                <div className="text-[10px] uppercase tracking-[0.16em] text-slate-500">
                  Próximo passo
                </div>
                <div className="mt-1 text-xs font-medium text-slate-200">
                  Listagem de Conteúdos
                </div>
                <p className="mt-1 text-[10px] text-slate-500">
                  Aqui vamos puxar da API os cards dos assets (tipo, plataforma, cliente, tags).
                </p>
              </div>
              <div className="mt-3 text-[9px] text-emerald-300/80">
                assim que quiser, eu monto esse endpoint + tela 👇
              </div>
            </div>

            <div className="bg-slate-900/40 border border-slate-800/60 rounded-2xl p-4 flex flex-col justify-between">
              <div>
                <div className="text-[10px] uppercase tracking-[0.16em] text-slate-500">
                  Organização inteligente
                </div>
                <div className="mt-1 text-xs font-medium text-slate-200">
                  Coleções e filtros
                </div>
                <p className="mt-1 text-[10px] text-slate-500">
                  Depois conectamos com <code>collections</code> para criar pastas temáticas de
                  conteúdos, campanhas e segmentos.
                </p>
              </div>
              <div className="mt-3 text-[9px] text-slate-500">
                UI já preparada para escalar sem ficar uma bagunça visual.
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}

export default App;
