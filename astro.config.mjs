import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// 说明：
// - 开发环境：使用 base='/'，本地访问 http://localhost:4321/calendar/2025 正常
// - 生产构建：GitHub Pages 用户页使用 base='/'，项目页使用 base='/<repo>'
const isDev = process.env.NODE_ENV !== 'production';

export default defineConfig({
  // GitHub Pages 用户页域名；本地开发不重要
  site: process.env.SITE || 'https://tswatery.github.io',
  // 用户页直接使用 '/'，项目页通过环境变量 BASE 设置
  base: process.env.BASE ?? '/',
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
