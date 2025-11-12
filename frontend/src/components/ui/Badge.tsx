import React from "react";

type BadgeProps = {
  children: React.ReactNode;
  variant?: "solid" | "outline" | "subtle";
  className?: string;
};

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = "solid",
  className = "",
}) => {
  const base =
    "inline-flex items-center rounded-full px-2.5 py-0.5 text-[10px] font-medium";

  const variants: Record<NonNullable<BadgeProps["variant"]>, string> = {
    solid: "bg-white text-red-900",
    outline: "border border-red-300 text-red-200",
    subtle: "bg-red-900/40 text-red-100",
  };

  return <span className={[base, variants[variant], className].join(" ")}>{children}</span>;
};
