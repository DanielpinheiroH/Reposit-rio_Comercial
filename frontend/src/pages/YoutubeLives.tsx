// src/pages/YoutubeLives.tsx
import React from "react";

export const YoutubeLives: React.FC = () => {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold text-white">
        Lives no YouTube
      </h1>
      <p className="text-red-100/80 text-base">
        Aqui você vai listar só os assets do tipo <strong>live_youtube</strong>.
      </p>
      {/* Depois a gente pluga no backend */}
    </div>
  );
};
