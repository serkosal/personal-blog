import { defineConfig } from 'vite'
import path from 'path';

export default defineConfig({
  base: '/static/',

  server: {
    host: 'localhost',
    port: 5173,
    strictPort: true,
    hmr: true,
  },


  build: {
    outDir: path.resolve(__dirname, '../backend/src/static/'),
    emptyOutDir: false,
    manifest: "manifest.json",
    rollupOptions: {
      
      input: {
        main:  'src/main.ts',
        editor: 'src/editor.ts',
      },
      output: {
        entryFileNames: '[name]-[hash].js',
        chunkFileNames: '[name]-[hash].js',
        assetFileNames: '[name]-[hash].[ext]'
      },
    },
  },
})