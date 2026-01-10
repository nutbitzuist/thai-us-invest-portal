import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Primary Colors
        primary: "#FF6B6B",
        secondary: "#4ECDC4",
        
        // Accent Colors
        accent: {
          yellow: "#FFE66D",
          mint: "#95E1D3",
          salmon: "#F38181",
          purple: "#DDA0DD",
        },
        
        // Neutrals
        background: "#FFF8E7",
        surface: "#FFFFFF",
        "text-primary": "#000000",
        border: "#000000",
        
        // Trend Colors
        uptrend: "#00C851",
        downtrend: "#FF4444",
        sideways: "#FFBB33",
      },
      fontFamily: {
        sans: ["IBM Plex Sans Thai", "sans-serif"],
        heading: ["IBM Plex Sans Thai", "sans-serif"],
        thai: ["IBM Plex Sans Thai", "sans-serif"],
      },
      boxShadow: {
        brutal: "4px 4px 0px #000000",
        "brutal-sm": "2px 2px 0px #000000",
        "brutal-lg": "6px 6px 0px #000000",
        "brutal-hover": "6px 6px 0px #000000",
      },
      borderWidth: {
        3: "3px",
      },
    },
  },
  plugins: [],
} satisfies Config;
