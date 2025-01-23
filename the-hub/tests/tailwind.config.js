/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{ts,tsx,js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: '#102403',
        bg2: '#132A04',
        bdr: '#365721',
        hvr: '#4E6A3C',
        fg: '#418C0F'
      }
    },
    fontFamily: {
      ephesis: ["Ephesis"],
      inkfree: ["Ink Free"],
    }
  },
  plugins: [],
}

