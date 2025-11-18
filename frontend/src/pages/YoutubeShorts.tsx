import React from "react";

export const YoutubeShorts: React.FC = () => {
  return (
    <div className="flex flex-col h-full gap-4">
      <header>
        <h2 className="text-2xl font-semibold text-white">
          YouTube · Shorts
        </h2>
        <p className="text-sm text-red-200/70">
          Shorts do YouTube cadastrados como posts no repositório.
        </p>
      </header>

      <div className="text-red-100/80 text-sm">
        (Em construção) — depois ligamos com a listagem de post_youtube_shorts.
      </div>
    </div>
  );
};

export default YoutubeShorts;
