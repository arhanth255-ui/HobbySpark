
const { defineConfig } = require("vite");
const path = require("path");

module.exports = defineConfig({
    root: path.join(__dirname, "renderer"),
    base: "./",
    server: {
        host: "127.0.0.1",
        port: 5173,
        strictPort: true
    },
    build: {
        outDir: path.join(__dirname, "dist"),
        emptyOutDir: true
    }
});
