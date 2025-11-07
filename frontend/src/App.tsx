import { useEffect, useState } from "react";
import { api } from "./lib/api";

function App() {
  const [status, setStatus] = useState<string>("checando...");
  const [error, setError] = useState<string>("");

  useEffect(() => {
    async function checkHealth() {
      try {
        const res = await api.get("/health");
        setStatus(JSON.stringify(res.data));
      } catch (err: any) {
        console.error(err);
        setError("Não consegui falar com o backend. Confere se ele está rodando em http://localhost:8000.");
      }
    }
    checkHealth();
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col items-center justify-center gap-3">
      <h1 className="text-2xl font-bold">Repositório Comercial</h1>
      <p className="text-xs text-slate-400">
        Teste de conexão frontend ➜ backend
      </p>

      {error ? (
        <div className="px-4 py-2 rounded-xl bg-red-900/40 text-red-300 text-xs max-w-md text-center">
          {error}
        </div>
      ) : (
        <div className="px-4 py-2 rounded-xl bg-emerald-900/40 text-emerald-300 text-xs">
          Resposta do backend: {status}
        </div>
      )}
    </div>
  );
}

export default App;
