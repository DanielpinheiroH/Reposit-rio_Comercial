import React from "react";

const TikTokFeed: React.FC = () => {
  return (
    <div className="flex flex-col h-full gap-4">
      <header>
        <h2 className="text-2xl font-semibold text-white">
          TikTok · Feed / Vídeos curtos
        </h2>
        <p className="text-sm text-red-200/70">
          Conteúdos do TikTok vinculados às campanhas do repositório.
        </p>
      </header>

      <div className="text-red-100/80 text-sm">
        (Em construção) — aqui conectamos com post_tiktok.
      </div>
    </div>
  );
};

export default TikTokFeed;
