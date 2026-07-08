import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // React core
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],

          // PDF viewing library (largest dependency)
          'pdf-viewer': ['react-pdf', 'pdfjs-dist'],

          // DOCX preview library
          'docx-viewer': ['docx-preview'],

          // HTTP client
          'axios': ['axios'],

          // Rich text editor (if used)
          'editor': ['@tinymce/tinymce-react']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  }
});
