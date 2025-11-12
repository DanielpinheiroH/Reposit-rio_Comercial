/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: "#dc2626",      // vermelho 600
          primaryDark: "#b91c1c",  // vermelho 700
          soft: "#fee2e2",         // vermelho 200 (bg suave)
        },
      },
      boxShadow: {
        card: "0 6px 24px -8px rgba(220,38,38,0.15)",
      },
      borderRadius: {
        xl2: "1rem",
      },
    },
  },
  plugins: [],
};
