# GitHub Pages 部署指南

## 部署状态

✅ **已完成**：
- 代码已推送到 GitHub：https://github.com/Tswatery/tswatery-github.io
- GitHub Actions 工作流已配置
- 配置文件已更新为您的用户名

## 下一步操作

### 1. 推送更新后的配置

在您的终端中执行：

```bash
cd /Users/lin/Desktop/blog

# 提交配置更改
git add .
git commit -m "chore: update username to Tswatery"
git push origin main
```

### 2. 启用 GitHub Pages

#### 在 GitHub 上操作：

1. **访问您的仓库**
   - 打开：https://github.com/Tswatery/tswatery-github.io

2. **进入 Settings**
   - 点击顶部的 "Settings" 标签

3. **配置 Pages**
   - 在左侧菜单中找到 "Pages"
   - Source 选择 "GitHub Actions"
   - 点击 "Save"

4. **查看部署状态**
   - 切换到 "Actions" 标签
   - 您会看到一个工作流正在运行
   - 等待 2-3 分钟部署完成

### 3. 访问您的博客

部署成功后，您的博客将可通过以下地址访问：

**主要地址**：
```
https://tswatery.github.io
```

**其他可用地址**：
- https://tswatery.github.io/
- https://tswatery.github.io/index.html

## 项目结构说明

```
Tswatery/blog/
├── .github/workflows/
│   └── gh-pages.yml          # GitHub Actions 自动部署配置
├── src/
│   ├── content/blog/         # 博客文章 (Markdown/MDX)
│   ├── layouts/              # 页面布局
│   ├── pages/                # 路由页面
│   └── styles/               # 样式文件
├── astro.config.mjs          # Astro 配置
└── tailwind.config.mjs       # Tailwind CSS 配置
```

## 添加新文章

1. 在 `src/content/blog/` 目录下创建新的 `.md` 文件
2. 文件命名格式：`YYYY-MM-DD-slug.md`
3. 添加 Front Matter：

```markdown
---
title: "文章标题"
date: 2025-01-31
summary: "文章摘要"
tags: ["标签1", "标签2"]
draft: false
---

# 文章内容

这里是文章正文...
```

4. 推送更改：

```bash
git add .
git commit -m "feat: add new article"
git push origin main
```

GitHub Actions 会自动构建并部署！

## 部署工作原理

1. **代码推送** → 触发 GitHub Actions
2. **自动构建** → 运行 `npm run build`
3. **生成静态文件** → 输出到 `dist` 目录
4. **部署到 Pages** → GitHub 自动发布
5. **网站上线** → 可通过 URL 访问

## 常见问题

### Q: 部署失败怎么办？
**A**: 检查 Actions 标签页中的错误日志，常见问题：
- 构建错误：检查代码语法
- 权限问题：确保仓库是 Public

### Q: 网站无法访问？
**A**: 检查以下几点：
- 确保 Pages 设置为 "GitHub Actions" 源
- 等待 3-5 分钟让部署完成
- 清除浏览器缓存

### Q: 如何自定义域名？
**A**: 在 Pages 设置中：
1. 输入您的自定义域名
2. 添加 DNS CNAME 记录指向 `Tswatery.github.io`

### Q: 文章更新但网站没变化？
**A**: 确保：
- 文件放在正确目录：`src/content/blog/`
- Front Matter 格式正确
- 已推送更改到 main 分支

## 性能优化

### 预构建已启用
- ✅ 代码压缩
- ✅ 资源优化
- ✅ 图片优化
- ✅ CSS/JS 合并

### CDN 加速
GitHub Pages 自动提供全球 CDN 加速，访问速度极快！

## SEO 优化

已内置以下 SEO 特性：
- ✅ 自动生成 sitemap.xml
- ✅ RSS 订阅 (rss.xml)
- ✅ 规范的 URL (canonical)
- ✅ Open Graph 元数据
- ✅ Twitter Card 标签
- ✅ 语义化 HTML

## 技术支持

如有问题，请查看：
- [Astro 文档](https://docs.astro.build)
- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [项目 README](../README.md)

---

## 快速命令参考

```bash
# 本地开发
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview

# 推送更改
git add .
git commit -m "your message"
git push origin main
```

---

**部署完成后，您将拥有一个完全功能的个人博客！** 🎉
