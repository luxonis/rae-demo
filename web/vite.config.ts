import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { viteCommonjs } from "@originjs/vite-plugin-commonjs";
import svgr from "vite-plugin-svgr";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), viteCommonjs(), svgr()],

  optimizeDeps: {
    exclude: ["depthai-visualizer"],
    include: [
      "depthai-visualizer > react-dom",
      "depthai-visualizer > react",
      "depthai-visualizer > hydrated-ws",
    ],
  },

  define: {
    __filename: JSON.stringify(""),
    __dirname: JSON.stringify(""),
    global: "typeof window !== 'undefined' ? window : {}",
    ReactNull: null,

    FOXGLOVE_STUDIO_VERSION: JSON.stringify("0.0.1"),
    process: {
      // eslint-disable-next-line @typescript-eslint/ban-types
      nextTick: (fn: Function, ...args: unknown[]): void => {
        queueMicrotask(() => {
          fn(...args);
        });
      },

      title: "browser",
      browser: true,
      env: {},
      argv: [],
    },
  },

  resolve: {
    alias: {
      "@mui/icons-material": "@mui/icons-material/esm",
    },
  },
});
