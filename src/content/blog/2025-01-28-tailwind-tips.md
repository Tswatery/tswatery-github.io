---
title: "Tailwind CSS 实用技巧"
date: 2025-01-28
summary: "分享一些 Tailwind CSS 的实用技巧和最佳实践。"
tags: ["CSS", "Tailwind", "前端", "样式"]
---

## 简介

Tailwind CSS 是一个功能类优先的 CSS 框架，它提供了大量的功能类来快速构建自定义设计。本文分享一些实用的技巧。

## 响应式设计技巧

### 移动优先的断点

```html
<!-- 默认是移动端，md: 以上是桌面端 -->
<div class="w-full md:w-1/2 lg:w-1/3">
  响应式网格
</div>

<!-- 不同尺寸的不同布局 -->
<div class="flex flex-col md:flex-row">
  <div class="w-full md:w-3/4">主内容</div>
  <div class="w-full md:w-1/4">侧边栏</div>
</div>
```

### 条件渲染

```html
<!-- 只在特定断点显示 -->
<div class="hidden md:block">只在桌面显示</div>
<div class="block md:hidden">只在移动端显示</div>
```

## 自定义配置技巧

### 扩展主题

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eff6ff',
          500: '#3b82f6',
          900: '#1e3a8a',
        }
      },
      spacing: {
        '72': '18rem',
        '84': '21rem',
        '96': '24rem',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }
    }
  }
}
```

### 使用 CSS 变量

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary)',
        secondary: 'var(--color-secondary)',
      }
    }
  }
}
```

## 实用功能类技巧

### 容器查询

```html
<div class="@container">
  <div class="@lg:text-xl">
    根据父容器大小而不是视口大小调整
  </div>
</div>
```

### 状态变体

```html
<!-- 组合状态变体 -->
<button class="bg-blue-500 hover:bg-blue-600 focus:ring-2 focus:ring-blue-300 disabled:opacity-50">
  按钮样式
</button>

<!-- 暗色模式 -->
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  深色模式支持
</div>
```

## 性能优化

### JIT 模式

Tailwind CSS v3+ 默认使用 JIT（Just-In-Time）编译：

```javascript
// tailwind.config.js
module.exports = {
  mode: 'jit',
  purge: ['./src/**/*.{js,jsx,ts,tsx,astro}'],
}
```

### 移除未使用的样式

```javascript
// 生产环境自动移除未使用的样式
const production = !process.env.ROLLUP_WATCH;

module.exports = {
  purge: production ? './src/**/*.{js,jsx,ts,tsx,astro}' : false,
}
```

## 常见布局模式

### Holy Grail 布局

```html
<body class="min-h-screen flex flex-col">
  <header class="bg-gray-800 text-white p-4">Header</header>

  <main class="flex-1 flex">
    <nav class="w-64 bg-gray-200 p-4">Sidebar</nav>
    <section class="flex-1 p-4">Main Content</section>
    <aside class="w-64 bg-gray-200 p-4">Extra</aside>
  </main>

  <footer class="bg-gray-800 text-white p-4">Footer</footer>
</body>
```

### 卡片组件

```html
<div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
  <img src="image.jpg" alt="Card image" class="w-full h-48 object-cover">
  <div class="p-6">
    <h3 class="text-xl font-semibold mb-2">卡片标题</h3>
    <p class="text-gray-600">卡片描述内容</p>
    <button class="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
      了解更多
    </button>
  </div>
</div>
```

## 总结

Tailwind CSS 提供了极大的灵活性，让开发者在不写自定义 CSS 的情况下快速构建美观的界面。掌握这些技巧可以让你更高效地使用 Tailwind CSS。