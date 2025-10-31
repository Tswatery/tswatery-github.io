# 📝 写作指南

## 创建新文章

### 1. 在 `src/content/blog/` 目录下创建新文件

文件名格式：**`YYYY-MM-DD-slug.md`**

例如：`2025-11-01-my-first-post.md`

### 2. 文件格式

```markdown
---
title: "文章标题"
date: 2025-11-01
summary: "文章摘要（会在列表页显示）"
tags: ["标签1", "标签2"]
draft: false  # false 表示发布，true 表示草稿
---

# 文章标题

这里是文章正文...

## 二级标题

正文内容...

### 代码示例

```javascript
console.log('Hello, World!');
```

### 数学公式

行内公式：$E = mc^2$

块级公式：
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

### 3. 推送更改

```bash
git add .
git commit -m "feat: add new article: 文章标题"
git push origin main
```

### 4. GitHub Actions 自动部署

推送后，GitHub Actions 会自动：
1. 构建网站
2. 部署到 https://tswatery.github.io
3. 生成 RSS 和 Sitemap

等待 2-3 分钟即可看到新文章！

## 目录结构

```
src/content/blog/
├── 2025-11-01-my-first-post.md  ← 您的第一篇文章
├── 2025-11-02-another-post.md   ← 第二篇文章
└── config.ts                     ← 配置文件（不要删除）
```

## 文章排序

文章按 `date` 字段排序，**最新的在前**。

## 标签使用

在 `tags` 数组中指定标签：
- `tags: ["技术"]`
- `tags: ["前端", "Astro"]`
- `tags: ["教程", "CSS"]`

标签会自动生成标签页，例如：`/tags/技术/`

## 草稿功能

设置 `draft: true` 的文章：
- 不会发布到网站
- 不会生成页面
- 本地开发时可以看到（如果设置可见）

## 支持的功能

✅ Markdown 语法
✅ 代码高亮
✅ 数学公式（LaTeX）
✅ 表格
✅ 任务列表
✅ 引用块
✅ 图片
✅ 自定义组件（MDX）

## 快速开始

现在就可以创建您的第一篇文章了！

在 `src/content/blog/` 目录创建 `2025-11-01-welcome.md`，写入您的内容，然后推送即可。
