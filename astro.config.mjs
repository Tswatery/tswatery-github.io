import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// 说明：
// - 开发环境（npm run dev）：使用 base='/'，本地访问 http://localhost:4321/calendar/2025 正常
// - 生产构建（npm run build 部署到 GitHub Pages 项目页）：使用 base='/<repo>'，例如 '/blog'
const isDev = process.env.NODE_ENV !== 'production';

export default defineConfig({
  // GitHub Pages 用户页域名；本地开发不重要
  site: process.env.SITE || 'https://tswatery.github.io',
  base: process.env.BASE ?? (isDev ? '/' : '/blog'),
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
