# 个人博客

一个基于 Astro 构建的轻量级个人博客系统。

> 部署时间：2025-10-30 18:40

## 特性

- 🚀 **极速加载** - 静态站点生成，零运行时 JavaScript
- 🎨 **美观设计** - A4 纸效果，简洁优雅
- 📝 **MDX 支持** - 完整的 Markdown 和 React 组件支持
- 🧮 **数学公式** - 完整的 LaTeX 数学环境支持
- 🎯 **代码高亮** - Shiki 提供的语法高亮
- 📱 **响应式** - 完美适配各种设备
- 🔍 **SEO 优化** - 完整的元数据和站点地图
- 📡 **RSS 订阅** - 支持 RSS 订阅

## 技术栈

- **框架**: Astro
- **样式**: Tailwind CSS
- **内容**: MDX
- **数学**: MathJax
- **部署**: GitHub Pages

## 快速开始

### 安装依赖

```bash
npm install
```

### 本地开发

```bash
npm run dev
```

访问 http://localhost:4321 查看博客。

### 构建生产版本

```bash
npm run build
```

构建后的文件将输出到 `dist` 目录。

### 预览构建结果

```bash
npm run preview
```

## 写作指南

### 创建新文章

在 `src/content/blog/` 目录下创建新的 MDX 文件，文件名格式建议为 `yyyy-mm-dd-slug.mdx`。

### Frontmatter

每篇文章需要包含以下 frontmatter：

```yaml
---
title: "文章标题"
date: 2025-01-01
summary: "文章摘要"
tags: ["标签1", "标签2"]
# 可选
updated: 2025-01-02  # 更新日期
draft: false         # 是否为草稿
cover:               # 封面图片
  src: "/images/cover.jpg"
  alt: "封面图片描述"
canonicalUrl: "https://example.com/original-post"  # 原文链接（如有）
---
```

### 数学公式

支持完整的 LaTeX 数学语法：

- 内联公式：`$E = mc^2$`
- 块级公式：
  ```
  $$
  \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
  $$
  ```

### 代码高亮

使用 ````language` 指定代码语言：

````markdown
```javascript
console.log('Hello, World!');
```
````

## 目录结构

```
src/
├── content/blog/     # 博客文章
├── layouts/         # 布局组件
├── pages/           # 页面路由
├── styles/          # 样式文件
└── components/      # 可复用组件
```

## 部署

### GitHub Pages

1. Fork 或创建仓库
2. 修改 `.github/workflows/gh-pages.yml` 中的 `SITE` 和 `BASE` 环境变量
3. 推送到 main 分支，GitHub Actions 会自动部署

### 其他平台

构建后的 `dist` 目录可以部署到任何静态托管平台。

## 自定义

### 修改主题色

编辑 `src/styles/theme.css` 中的 CSS 变量：

```css
:root {
  --primary: #3b82f6;
  --link: #2563eb;
  /* 其他颜色变量 */
}
```

### 修改字体

在 `tailwind.config.mjs` 中修改字体配置。

### 添加功能

项目采用模块化设计，可以轻松添加新功能。

## 许可证

MIT License