# Astro 内容管理脚本

一个通用的内容管理脚本，支持自动处理 blog 和 diary 文件的 front matter，包括中文标题翻译、AI 生成 tags 和 summary 等功能。

## 功能特点

- 🔄 **双模式支持**: 同时支持 `blog` 和 `diary` 两种内容类型
- 🌐 **智能翻译**: 中文标题自动翻译成英文文件名
- 🤖 **AI 生成**: 使用配置的模型自动生成 tags 和 summary
- ⚡ **真实时间**: 使用文件的真实创建时间（解决 GitHub Pages 时间戳问题）
- 📝 **交互模式**: 支持手动输入和自动生成两种模式
- 🎯 **智能限制**: tags 限制在 3 个以内，summary 限制在 30 字以内

## 安装依赖

```bash
# 安装所需的 Python 包
pip install requests pyyaml
```

## 使用方法

### 基本用法

```bash
# 处理 blog 文件（交互模式）
python scripts/content_manager.py --type blog

# 处理 diary 文件（保持原有逻辑）
python scripts/content_manager.py --type diary

# 自动模式（全部自动生成，不询问用户）
python scripts/content_manager.py --type blog --auto
```

### 交互模式流程

处理 blog 文件时，脚本会：

1. **提取标题**: 从文件内容中提取一级标题 (# 标题)
2. **翻译文件名**: 将中文标题翻译成英文，生成新的文件名
3. **获取时间**: 使用文件的真实创建时间
4. **生成 tags**:
   - 询问是否手动输入 tags
   - 如果选择自动生成，会使用 AI 模型生成最多 3 个相关标签
5. **生成 summary**:
   - 询问是否手动输入 summary
   - 如果选择自动生成，会使用 AI 模型生成不超过 30 字的中文摘要

### 文件处理规则

#### Blog 文件处理
- ✅ 自动添加必需的 front matter: `title`, `date`, `summary`, `tags`
- ✅ 中文标题翻译成英文文件名（如：`Verl训练SFT和RL小结.md` → `verl-training-sft-rl-summary.md`）
- ✅ 使用文件真实创建时间作为 date
- ✅ 支持手动或自动生成 tags 和 summary
- ✅ 保留原有文件内容，只添加/更新 front matter

#### Diary 文件处理
- ✅ 保持原有逻辑，只添加 `date` 字段
- ✅ 使用文件真实创建时间
- ✅ 跳过已有 date 字段的文件

## 配置说明

### 模型配置 (models.yaml)

脚本会自动读取项目根目录下的 `models.yaml` 文件：

```yaml
models:
  - name: "deepseek-ai/DeepSeek-V3.2-Exp"
    base_url: "https://api.siliconflow.cn/v1"
    api_key: "your-api-key-here"
```

如果配置了模型，脚本会：
- 使用 AI 进行中文到英文的标题翻译
- 使用 AI 生成相关的 tags
- 使用 AI 生成简洁的 summary

如果没有配置模型，脚本会使用内置的简单规则进行转换和生成。

## 使用示例

### 示例 1: 处理 Blog 文件

```bash
$ python scripts/content_manager.py --type blog

🚀 开始处理 blog 内容...

📁 开始处理 blog 目录...

📝 处理 blog 文件: 我的深度学习实践.md
📄 原标题: 我的深度学习实践
🔤 英文文件名: my-deep-learning-practice.md

🎯 当前内容预览: 在这篇文章中，我将分享深度学习的...
是否手动输入 tags？(y/n，默认n): n
🤖 生成的 tags: 深度学习, 实践, 教程
是否手动输入 summary？(y/n，默认n): n
🤖 生成的 summary: 深度学习实践经验分享

✅ 已创建新文件: my-deep-learning-practice.md

✅ 成功处理了 1 个 blog 文件：
  📝 my-deep-learning-practice.md

🎉 blog 内容处理完成！
```

### 示例 2: 自动模式

```bash
$ python scripts/content_manager.py --type blog --auto

🚀 开始处理 blog 内容...

📁 开始处理 blog 目录...

📝 处理 blog 文件: 强化学习总结.md
📄 原标题: 强化学习总结
🔤 英文文件名: reinforcement-learning-summary.md
🤖 生成的 tags: 强化学习, 总结, 机器学习
🤖 生成的 summary: 强化学习核心概念总结
✅ 已创建新文件: reinforcement-learning-summary.md

✅ 成功处理了 1 个 blog 文件：
  📝 reinforcement-learning-summary.md

🎉 blog 内容处理完成！
```

### 示例 3: 处理 Diary 文件

```bash
$ python scripts/content_manager.py --type diary

🚀 开始处理 diary 内容...

📁 开始处理 diary 目录...

📔 处理 diary 文件: 今天的工作总结.md
✅ 已添加时间戳: 2025-11-11 14:30:22

📔 处理 diary 文件: 周末计划.md
✅ 文件已有 date 字段，跳过: 周末计划.md

✅ 成功处理了 1 个 diary 文件：
  📝 今天的工作总结.md

🎉 diary 内容处理完成！
```

## 注意事项

1. **文件备份**: 建议先备份重要文件，特别是 blog 文件会被重命名
2. **模型 API**: 确保 API key 有效，网络连接正常
3. **文件编码**: 所有文件必须是 UTF-8 编码
4. **时间戳**: 脚本使用文件系统的真实创建时间，不受 git 提交时间影响
5. **交互模式**: 默认是交互模式，会询问用户输入；使用 `--auto` 参数可以跳过询问

## 错误处理

脚本会处理以下常见错误：
- ❌ 找不到指定目录
- ❌ 文件编码问题
- ❌ API 调用失败（自动降级到简单规则）
- ❌ 文件重名冲突
- ❌ front matter 格式错误

## 更新日志

- v1.0.0: 初始版本，支持 blog 和 diary 双模式
- 功能: 中文标题翻译、AI 生成、交互模式、自动模式