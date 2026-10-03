import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
// `defineConfig` comes from "vitest/config" rather than plain "vite" so
// that the `test` block below is type-checked -- it's a superset of
// Vite's own config type with Vitest's options merged in.
export default defineConfig({
    plugins: [react()],
    server: {
        port: 5173,
    },
    test: {
        environment: "jsdom",
        setupFiles: ["./src/test/setup.ts"],
    },
});
