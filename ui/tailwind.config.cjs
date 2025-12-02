module.exports = {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#f5f9ff",
          100: "#e6f0ff",
          500: "#2563eb", // primary
          700: "#1e40af"
        }
      }
    }
  },
  plugins: []
};
