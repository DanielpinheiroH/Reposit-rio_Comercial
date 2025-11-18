// src/pages/InstagramFeedReels.tsx
import React from "react";

export const InstagramFeedReels: React.FC = () => {
  return (
    <div className="flex flex-col h-full gap-4">
      <header>
        <h2 className="text-2xl font-semibold text-white">
          Instagram · Feed &amp; Reels
        </h2>
        <p className="text-sm text-red-200/70">
          Publicações de feed e reels do Instagram.
        </p>
      </header>

      <div className="text-red-100/80 text-sm">
        (Em construção) — aqui vamos filtrar os posts de Instagram por formato
        (feed / reels).
      </div>
    </div>
  );
};
