/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Warm dark charcoal, not pure/blue black -- see project-memory/DECISIONS.md
        // for why this palette was chosen over the more generic
        // near-black + acid-green/vermilion combination.
        base: {
          DEFAULT: "#121110",
          panel: "#1a1917",
          hairline: "#2e2c28",
        },
        ink: {
          DEFAULT: "#f2efe9",
          muted: "#9b968c",
        },
        signal: {
          // Primary interactive accent -- a deliberate nod to
          // amber-on-black trading-terminal displays, not a decorative
          // brand color chosen at random.
          amber: "#e3a53d",
          // Functional only: price dropped / good news.
          positive: "#6fae8c",
          // Functional only: price rose / needs attention.
          negative: "#c97664",
        },
      },
      fontFamily: {
        sans: ["'IBM Plex Sans'", "system-ui", "sans-serif"],
        // Reserved specifically for numeric/data values (prices, specs),
        // never for decorative labels -- see project-memory/DECISIONS.md.
        mono: ["'IBM Plex Mono'", "ui-monospace", "monospace"],
      },
      keyframes: {
        "pulse-dot": {
          "0%, 100%": { opacity: 1 },
          "50%": { opacity: 0.35 },
        },
        "insert-row": {
          "0%": { opacity: 0, transform: "translateY(-6px)" },
          "100%": { opacity: 1, transform: "translateY(0)" },
        },
      },
      animation: {
        "pulse-dot": "pulse-dot 2s ease-in-out infinite",
        "insert-row": "insert-row 0.25s ease-out",
      },
    },
  },
  plugins: [],
};
