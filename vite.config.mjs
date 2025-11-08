import { defineConfig } from "vite";
import tailwind from "@tailwindcss/vite";
import path from "node:path";

export default defineConfig({
  plugins: [tailwind()],
  root: "static_src",
  base: "/static/",
  build: {
    outDir: path.resolve(__dirname, "static"),
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, "static_src/js/main.js"),
        form: path.resolve(__dirname, "static_src/js/form.js"),
        visualisation_barchart: path.resolve(
          __dirname,
          "static_src/js/visualisation_barchart.js"
        ),
      },
    },
  },

  server: {
    port: 5173,
    host: "localhost",
    origin: "http://localhost:5173",
    strictPort: true,
    watch: {
      usePolling: true,
    },
  },
});
