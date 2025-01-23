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
        bg: "#1A1A1D",
        bg2: '#3B1C32',
        bdr: '#3B1C32',
        hvr: '#6A1E55',
        fg: "#A64D79",
      },
    },
    fontFamily: {
      indieFlower: ["Indie Flower"],
      patrickHand: ["Patrick Hand"],
    },
  },
  plugins: [],
} satisfies Config;
