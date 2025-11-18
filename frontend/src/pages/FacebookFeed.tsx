import React from "react";

const FacebookFeed: React.FC = () => {
  return (
    <div className="flex flex-col h-full gap-4">
      <header>
        <h2 className="text-2xl font-semibold text-white">
          Facebook · Feed
        </h2>
        <p className="text-sm text-red-200/70">
          Publicações de feed do Facebook cadastradas no repositório.
        </p>
      </header>

      <div className="text-red-100/80 text-sm">
        (Em construção) — depois ligamos com o endpoint de post_facebook.
      </div>
    </div>
  );
};

export default FacebookFeed;
