# 技术文档（初始化）

版本：v0.2
日期：2025-10-30
状态：已冻结技术选型与范围；待搭建脚手架

## 1. 项目概览
- 目标：搭建一个轻量、阅读体验友好的个人博客，支持 Markdown/MDX 与完整 LaTeX 数学环境，部署到 GitHub Pages（项目页），具备良好 SEO 与 RSS 订阅。
- 非目标：不做搜索、评论、统计分析、暗色模式、侧边栏、多语言切换等复杂功能。
- 风格参考：借鉴 jyywiki 的简洁、专注内容的排版（不包含侧边栏导航）。

## 2. 技术选型（确认）
- 框架：Astro（静态预渲染，默认零运行时 JS）。
- 样式：Tailwind CSS + @tailwindcss/typography（不启用暗色模式）。
- Markdown/MDX：启用 MDX 以支持可复用的内容组件（提示框、图注等）。
- 数学：remark-math + rehype-mathjax（CHTML 输出，构建期静态渲染），启用自动编号与 \label/\ref。
- 代码高亮：Shiki（构建期高亮，亮色主题）。
- SEO：@astrojs/sitemap。
- 订阅：@astrojs/rss（开启）。
- 部署：GitHub Pages（方案 A：GitHub Actions 自动构建与发布，项目页）。

## 3. 信息架构与页面
- 主页（/）：最新文章列表（标题、日期、摘要）。
- 文章页（/blog/:slug/）：标题、日期、标签、上一篇/下一篇。无“文内 TOC 块”。
- 标签页（/tags/ 与 /tags/:tag/）：按标签聚合。
- 归档页（/archive/）：按年/月聚合。
- 关于页（/about/）：作者与站点信息、社交链接。
- 404（/404）：友好返回首页。

## 4. 内容模型（Frontmatter）
- 必填：
  - title: string
  - date: ISO 日期（如 2025-01-01）
  - summary: string（简短摘要）
  - tags: string[]
- 可选：
  - updated: ISO 日期
  - draft: boolean（默认 false）
  - cover: { src: string, alt?: string }
  - canonicalUrl: string（如需要规范化链接）
- 文件组织：`src/content/blog/yyyy-mm-dd-slug.md[x]`
- 路由规范：
  - 文章：`/blog/:slug/`
  - 标签：`/tags/:tag/`
  - 归档：`/archive/`

## 5. 数学环境规范
- 语法：
  - 内联：`$ ... $`
  - 块级：`$$ ... $$`
  - AMS 环境：`align`/`gather`/`cases`/`split` 等。
- 编号与引用：
  - MathJax 配置 `tex: { tags: 'all' }`，支持 `\label{}`、`\ref{}`、`\eqref{}`。
  - 支持 `\tag{}` 自定义编号。
- 宏（示例，可扩展）：
  - `\E`，`\Var`，`\argmin`，`\argmax`，`\ind{}` 等在集中配置中声明。
- 容错：启用 `noerrors`/`noundefined`，渲染错误不阻断页面，保留可读提示。
- 性能：构建期渲染为静态 HTML + CSS（CHTML），无客户端 MathJax 运行时脚本。

示例 MathJax（文档示例，实施阶段会写入配置）：
```js
// mathjax.config.js（示例）
export default {
  options: { enableMenu: false },
  chtml: { scale: 1 },
  tex: {
    tags: 'all',
    packages: { '[+]': ['noerrors', 'noundefined'] },
    macros: {
      E: '{\\mathbb{E}}',
      Var: '{\\mathrm{Var}}',
      argmin: '\\mathop{\\mathrm{argmin}}',
      argmax: '\\mathop{\\mathrm{argmax}}',
      ind: ['{\\mathbf{1}_{ #1 }}', 1]
    }
  }
}
```

## 6. 视觉与配置接口（可由你后续替换）
- 设计 Tokens（CSS 变量，集中管理）：
  - `--bg`, `--fg`, `--muted`, `--primary`, `--link`, `--border`, `--code-bg`, `--code-fg`。
  - Tailwind 通过 `theme.extend.colors` 绑定上述变量，Typography 使用同一套色彩。
- 字体占位（建议后续替换为你的字体栈）：
  - `font-sans`: `-apple-system, BlinkMacSystemFont, 'SF Pro SC', 'Noto Sans SC', 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif`
  - `font-mono`: `ui-monospace, SFMono-Regular, Menlo, Consolas, 'JetBrains Mono', monospace`
- 排版约定：
  - 单栏正文，内容宽 ~70–80 字符；行高 1.7–1.8；标题层级与段落间距清晰。
  - 代码块使用 Shiki 亮色主题、显示行号；复制按钮如需再加微交互（可选）。

## 7. 性能与 SEO
- 性能预算：首屏 JS ≈ 0KB；CSS ≤ 35KB；非相册页图片总量 ≤ 300KB。
- 预渲染：全站静态；可按需预取下一篇文章链接（后续再评估）。
- 元数据：Open Graph、Twitter Card、Article JSON‑LD、canonical URL、站点地图。
- 链接健康：CI 可选启用链接检查（非必需）。

## 8. 目录结构（规划）
```
src/
  pages/           # 路由页面（主页、标签、归档、关于、404）
  content/
    blog/          # 文章（md/mdx）
  layouts/         # 页面与文章布局
  components/      # UI 组件（导航、文章卡片、标签、分页等）
  styles/          # theme.css（tokens）、global.css
public/            # 静态资源（图标等）
.github/workflows/ # gh-pages.yml（Actions 工作流）
```

## 9. 依赖清单（规划，不立即安装）
- 核心：`astro`, `@astrojs/mdx`, `@astrojs/tailwind`, `@astrojs/sitemap`
- 数学：`remark-math`, `rehype-mathjax`
- 样式：`tailwindcss`, `@tailwindcss/typography`, `postcss`, `autoprefixer`
- 高亮：`shiki`
- 订阅：`@astrojs/rss`（开启）

## 10. RSS 规范（开启）
- 路由：`/rss.xml`
- 收录：非 draft 的文章，按 `date` 降序，默认最近 30 篇（可调）。
- 字段：`title`, `link`, `pubDate`, `description(summary)`，可扩展 `content:encoded`。

示例（文档示例，实施阶段会落地到 `src/pages/rss.xml.ts`）：
```ts
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = (await getCollection('blog', ({ data }) => !data.draft))
    .sort((a, b) => +new Date(b.data.date) - +new Date(a.data.date))
    .slice(0, 30);
  return rss({
    title: '你的站点标题',
    description: '你的站点描述',
    site: context.site, // 由 astro.config.mjs 的 site 提供
    items: posts.map((p) => ({
      title: p.data.title,
      pubDate: p.data.date,
      description: p.data.summary,
      link: `/blog/${p.slug}/`,
    })),
  });
}
```

## 11. 部署（方案 A：GitHub Actions，项目页）
- 站点类型：项目页（形如 `https://USERNAME.github.io/REPO`）。
- Astro 关键配置：
  - `site`: 必须是 `https://USERNAME.github.io`
  - `base`: 必须是 `/REPO`
  - 可通过环境变量在 CI 注入：`SITE` 与 `BASE`
- Pages 工作流（文档示例，实施阶段会写入 `.github/workflows/gh-pages.yml`）：
```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - name: Build
        env:
          SITE: https://USERNAME.github.io
          BASE: /REPO
        run: |
          npx astro build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```
- 其他：
  - 构建产物应包含 `.nojekyll`（Astro 默认会处理，无需手工添加）。
  - 若使用自定义域名：在发布产物根目录包含 `CNAME` 文件。

## 12. 里程碑与交付
- M1 文档冻结（当前）：选型与范围已确认（无搜索/无暗色/无评论，RSS 开启，无文内 TOC）。
- M2 脚手架与配置：Astro + Tailwind、Shiki、MathJax 渲染管线、页面骨架、设计 tokens 占位。
- M3 内容导入：迁移首批文章、标签/归档生成、RSS/站点地图。
- M4 视觉落地：替换你的配色与字体，微调排版细节。
- M5 部署上线：Actions + GitHub Pages 项目页。

## 13. 待填信息与后续操作
- GitHub：`USERNAME` 与 `REPO`（用于 `site/base` 与工作流示例替换）。
- 设计：主色 `--primary` 与字体栈（若暂不提供，先用占位值，后续可直接改 tokens）。
- RSS：收录数量是否维持 30？如需调整请告知。

确认无误后，将按本文档实施 M2（脚手架与配置）。
