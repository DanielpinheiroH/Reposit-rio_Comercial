// src/pages/InstagramStories.tsx
import React from "react";

export const InstagramStories: React.FC = () => {
  return (
    <div className="flex flex-col h-full gap-4">
      <header>
        <h2 className="text-2xl font-semibold text-white">
          Instagram · Stories
        </h2>
        <p className="text-sm text-red-200/70">
          Stories do Instagram associados às campanhas.
        </p>
      </header>

      <div className="text-red-100/80 text-sm">
        (Em construção) — depois filtramos posts de Instagram com formato
        &quot;stories&quot;.
      </div>
    </div>
  );
};
