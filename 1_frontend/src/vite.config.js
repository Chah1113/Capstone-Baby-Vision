// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite' // 이 줄이 있어야 합니다!

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
})