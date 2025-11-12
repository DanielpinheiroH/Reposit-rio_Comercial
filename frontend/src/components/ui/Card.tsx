import React from "react";

type CardProps = {
  children: React.ReactNode;
  className?: string;
};

export const Card: React.FC<CardProps> = ({ children, className = "" }) => {
  return (
    <div
      className={[
        "rounded-2xl border p-4",
        // base default (vermelho escuro translúcido)
        "bg-red-900/20 border-red-900/40 text-red-50",
        className,
      ].join(" ")}
    >
      {children}
    </div>
  );
};
