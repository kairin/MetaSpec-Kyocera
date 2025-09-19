import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import react from '@astrojs/react';
import mdx from '@astrojs/mdx';

// https://astro.build/config
export default defineConfig({
  integrations: [
    tailwind({
      applyBaseStyles: true, // Let TailwindCSS handle base styles
    }),
    react(),
    mdx()
  ],
  site: 'https://kairin.github.io',
  base: '/MetaSpec-Kyocera',
  server: {
    port: 3000,
    host: '0.0.0.0', // Allow external access for development
  },
  build: {
    outDir: 'dist',
    assets: '_astro'
  },
  output: 'static', // Static site generation for zero-cost GitHub Pages hosting
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
      langs: ['javascript', 'typescript', 'python', 'bash', 'sql', 'yaml', 'json'],
      wrap: true
    }
  },
  vite: {
    define: {
      __DATE__: `"${new Date().toISOString()}"`,
    },
  },
});