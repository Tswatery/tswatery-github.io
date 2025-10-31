import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://YOUR_USERNAME.github.io',
  base: '/',
  integrations: [mdx(), tailwind(), sitemap()],
  markdown: {
    shikiConfig: {
      theme: 'github-light',
      wrap: true,
      langs: [],
    },
  },
  vite: {
    optimizeDeps: {
      exclude: ['pagefind'],
    },
  },
});