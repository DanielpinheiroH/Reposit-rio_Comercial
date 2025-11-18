import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Layout } from "./components/Layout";

// Dashboard
import { Dashboard } from "./pages/Dashboard";

// SITE / PORTAL
import { SiteTodos } from "./pages/SiteTodos";
import { SitePublieditorial } from "./pages/SitePublieditorial";
import { SitePublicidadeNativa } from "./pages/SitePublicidadeNativa";
import { SiteArtigoOpiniaoDigital } from "./pages/SiteArtigoOpiniaoDigital";
import { SiteManchetes } from "./pages/SiteManchetes";
import { SiteSubManchetes } from "./pages/SiteSubManchetes";

// YOUTUBE
import { YoutubeLives } from "./pages/YoutubeLives";
import { YoutubeTalks } from "./pages/YoutubeTalks";
import { YoutubeShorts } from "./pages/YoutubeShorts";

// INSTAGRAM
import { InstagramFeedReels } from "./pages/InstagramFeedReels";
import { InstagramStories } from "./pages/InstagramStories";

// TIKTOK
import { TikTokFeed } from "./pages/TikTokFeed";

// KWAI
import { KwaiFeed } from "./pages/KwaiFeed";

// FACEBOOK
import { FacebookFeed } from "./pages/FacebookFeed";

// ORGANIZAÇÃO
import { Colecoes } from "./pages/Colecoes";
import { Metricas } from "./pages/Metricas";

// Telas antigas agregadas (se quiser manter a visão consolidada)
import { ConteudosEspeciais } from "./pages/ConteudosEspeciais";
import { PostsShorts } from "./pages/PostsShorts";

// Placeholder pra rota /projeto/novo (modal é controlado pelo Layout)
import { ProjetoNovo } from "./pages/ProjetoNovo";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          {/* Dashboard */}
          <Route path="/" element={<Dashboard />} />

          {/* SITE / PORTAL */}
          <Route path="/site/todos" element={<SiteTodos />} />
          <Route path="/site/publieditorial" element={<SitePublieditorial />} />
          <Route
            path="/site/publicidade-nativa"
            element={<SitePublicidadeNativa />}
          />
          <Route
            path="/site/artigo-opiniao-digital"
            element={<SiteArtigoOpiniaoDigital />}
          />
          <Route path="/site/manchetes" element={<SiteManchetes />} />
          <Route path="/site/sub-manchetes" element={<SiteSubManchetes />} />

          {/* YOUTUBE */}
          <Route path="/youtube/lives" element={<YoutubeLives />} />
          <Route path="/youtube/talks" element={<YoutubeTalks />} />
          <Route path="/youtube/shorts" element={<YoutubeShorts />} />

          {/* INSTAGRAM */}
          <Route
            path="/instagram/feed-reels"
            element={<InstagramFeedReels />}
          />
          <Route path="/instagram/stories" element={<InstagramStories />} />

          {/* TIKTOK */}
          <Route path="/tiktok/feed" element={<TikTokFeed />} />

          {/* KWAI */}
          <Route path="/kwai/feed" element={<KwaiFeed />} />

          {/* FACEBOOK */}
          <Route path="/facebook/feed" element={<FacebookFeed />} />

          {/* ORGANIZAÇÃO */}
          <Route path="/colecoes" element={<Colecoes />} />
          <Route path="/metricas" element={<Metricas />} />

          {/* TELAS CONSOLIDADAS ANTIGAS (opcional, se quiser manter) */}
          <Route
            path="/conteudos-especiais"
            element={<ConteudosEspeciais />}
          />
          <Route path="/posts-shorts" element={<PostsShorts />} />

          {/* Rota “vazia” pra acionar o modal de novo projeto */}
          <Route path="/projeto/novo" element={<ProjetoNovo />} />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
