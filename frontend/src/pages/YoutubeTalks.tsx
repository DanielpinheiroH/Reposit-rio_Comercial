import React from "react";

export const YoutubeTalks: React.FC = () => {
  return (
    <div className="flex flex-col h-full gap-4">
      <header>
        <h2 className="text-2xl font-semibold text-white">
          YouTube · Talks (Big / One / Little)
        </h2>
        <p className="text-sm text-red-200/70">
          Talks, entrevistas e conversas longas cadastradas (tipo_asset = youtube_talk).
        </p>
      </header>

      <div className="text-red-100/80 text-sm">
        (Em construção) — aqui vamos conectar com o endpoint de youtube_talk.
      </div>
    </div>
  );
};

export default YoutubeTalks;
