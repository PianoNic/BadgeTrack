import { defineConfig } from 'vite';
import preact from '@preact/preset-vite';

const backend = 'http://localhost:8000';

export default defineConfig({
  plugins: [preact()],
  // relative asset URLs so the app works behind a reverse proxy sub-path
  base: './',
  server: { proxy: { '/api': backend, '/badge': backend, '/docs': backend, '/openapi.json': backend } },
});
