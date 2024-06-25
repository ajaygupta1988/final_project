import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3001,
  },
  test: {
    globals:true,
    setupFiles:"src/testSetup.js",
    environment:'jsdom',
    environmentOptions: {
      jsdom: {
        resources: 'usable',
      },
    },
    server: {
      deps: {
        inline: ['vitest-canvas-mock'],
      },
    }

  }
});
