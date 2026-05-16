/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./App.{js,jsx,ts,tsx}", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#0F172A",
        accent: "#06B6D4",
        critical: "#EF4444",
        warning: "#F59E0B",
        safe: "#22C55E",
      }
    },
  },
  plugins: [],
}
