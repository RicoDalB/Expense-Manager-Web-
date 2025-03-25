import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  publicDir: './public', // ✅ Assicura che `public/` sia la cartella giusta
  server: {
    port: 5173, // ✅ Cambia se necessario
  },
});
