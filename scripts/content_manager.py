#!/usr/bin/env python3.10
"""
Astro 内容管理脚本 - 支持 blog 和 diary 目录

功能：
- 自动处理 blog 和 diary 文件的 front matter
- 中文标题自动翻译成英文文件名
- 使用 AI 模型生成 tags 和 summary
- 支持手动输入和自动生成模式

使用方法：
python scripts/content_manager.py --type blog    # 处理 blog 文件
python scripts/content_manager.py --type diary  # 处理 diary 文件
"""

import os
import re
import argparse
from pathlib import Path
from datetime import datetime
import locale
import json
from typing import Optional, List, Dict

# 可选导入，如果失败则使用备用方案
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    print("⚠️  PyYAML 未安装，将使用备用配置模式")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️  requests 未安装，将使用简单规则模式")

# 设置中文时间格式
locale.setlocale(locale.LC_TIME, 'zh_CN.UTF-8')

class ContentManager:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.models_config = self.load_models_config()

    def load_models_config(self) -> Dict:
        """加载模型配置文件"""
        if not YAML_AVAILABLE:
            print("⚠️  PyYAML 不可用，将使用简单规则模式")
            return {}

        models_file = self.project_root / 'models.yaml'
        if models_file.exists():
            try:
                with open(models_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                print(f"⚠️  读取 models.yaml 失败：{e}，将使用简单规则模式")
                return {}
        return {}

    def get_file_creation_time(self, file_path: Path) -> datetime:
        """获取文件创建时间"""
        stat = os.stat(file_path)
        # 优先使用创建时间，如果没有则使用修改时间
        creation_time = stat.st_birthtime if hasattr(stat, 'st_birthtime') else stat.st_ctime
        return datetime.fromtimestamp(creation_time)

    def translate_chinese_to_english(self, chinese_text: str) -> str:
        """简单的中文转英文函数（使用 AI 模型）"""
        if not self.models_config.get('models') or not REQUESTS_AVAILABLE:
            # 如果没有配置模型或 requests 不可用，使用简单的拼音转换
            print("⚠️  使用简单规则进行中文翻译")
            return self.simple_pinyin_convert(chinese_text)

        # 使用配置的模型进行翻译
        model = self.models_config['models'][0]  # 使用第一个模型
        try:
            response = requests.post(
                f"{model['base_url']}/chat/completions",
                headers={
                    'Authorization': f"Bearer {model['api_key']}",
                    'Content-Type': 'application/json'
                },
                json={
                    "model": model['name'],
                    "messages": [
                        {"role": "system", "content": "你是一个专业的翻译助手，请将中文标题翻译成简洁的英文标题，只返回翻译结果，不要有任何解释或标点符号。"},
                        {"role": "user", "content": f"将以下中文标题翻译成英文：{chinese_text}"}
                    ],
                    "max_tokens": 50,
                    "temperature": 0.3
                },
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                translation = result['choices'][0]['message']['content'].strip()
                # 清理翻译结果，只保留字母、数字和连字符
                return re.sub(r'[^a-zA-Z0-9\s-]', '', translation).replace(' ', '-').lower()
            else:
                print(f"⚠️  翻译 API 调用失败，使用简单转换")
                return self.simple_pinyin_convert(chinese_text)

        except Exception as e:
            print(f"⚠️  翻译失败：{e}，使用简单转换")
            return self.simple_pinyin_convert(chinese_text)

    def simple_pinyin_convert(self, chinese_text: str) -> str:
        """简单的拼音转换作为后备方案"""
        # 这里可以集成更复杂的拼音库，现在用简单处理
        # 提取关键词并简单翻译
        text = re.sub(r'[^\u4e00-\u9fff]', '', chinese_text)  # 只保留中文字符

        # 常见词汇的简单映射
        simple_dict = {
            '训练': 'training', '学习': 'learning', '深度': 'deep',
            '强化': 'reinforcement', '小结': 'summary', '总结': 'summary',
            '笔记': 'notes', '思考': 'thoughts', '实践': 'practice',
            '教程': 'tutorial', '指南': 'guide', '入门': 'beginner',
            '高级': 'advanced', '基础': 'basic', '原理': 'principles'
        }

        result = []
        for key, value in simple_dict.items():
            if key in chinese_text:
                result.append(value)

        if result:
            return '-'.join(result)
        else:
            # 如果无法翻译，使用时间戳
            return f"post-{int(datetime.now().timestamp())}"

    def generate_tags_and_summary(self, content: str, title: str) -> tuple[List[str], str]:
        """使用 AI 模型生成 tags 和 summary"""
        if not self.models_config.get('models') or not REQUESTS_AVAILABLE:
            # 如果没有配置模型或 requests 不可用，使用简单规则生成
            print("⚠️  使用简单规则生成 tags 和 summary")
            return self.simple_generate_tags_and_summary(content, title)

        model = self.models_config['models'][0]
        try:
            # 生成 tags
            tags_response = requests.post(
                f"{model['base_url']}/chat/completions",
                headers={
                    'Authorization': f"Bearer {model['api_key']}",
                    'Content-Type': 'application/json'
                },
                json={
                    "model": model['name'],
                    "messages": [
                        {"role": "system", "content": "你是一个专业的内容分析师，请根据文章内容生成最多3个相关的标签。标签应该简洁、专业，用逗号分隔。只返回标签，不要有任何解释。"},
                        {"role": "user", "content": f"标题：{title}\n内容：{content[:500]}..."}
                    ],
                    "max_tokens": 50,
                    "temperature": 0.3
                },
                timeout=10
            )

            # 生成 summary
            summary_response = requests.post(
                f"{model['base_url']}/chat/completions",
                headers={
                    'Authorization': f"Bearer {model['api_key']}",
                    'Content-Type': 'application/json'
                },
                json={
                    "model": model['name'],
                    "messages": [
                        {"role": "system", "content": "请用中文为文章内容生成一个不超过30字的简洁摘要。只返回摘要内容，不要有任何解释。"},
                        {"role": "user", "content": f"标题：{title}\n内容：{content[:500]}..."}
                    ],
                    "max_tokens": 60,
                    "temperature": 0.3
                },
                timeout=10
            )

            tags = []
            summary = ""

            if tags_response.status_code == 200:
                tags_result = tags_response.json()
                tags_text = tags_result['choices'][0]['message']['content'].strip()
                # 解析标签
                tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()][:3]

            if summary_response.status_code == 200:
                summary_result = summary_response.json()
                summary = summary_result['choices'][0]['message']['content'].strip()
                # 确保不超过30字
                if len(summary) > 30:
                    summary = summary[:30] + "..."

            return tags, summary

        except Exception as e:
            print(f"⚠️  AI 生成失败：{e}，使用简单规则")
            return self.simple_generate_tags_and_summary(content, title)

    def simple_generate_tags_and_summary(self, content: str, title: str) -> tuple[List[str], str]:
        """简单的 tags 和 summary 生成规则"""
        # 简单的关键词提取
        keywords = ['教程', '笔记', '总结', '实践', '思考', '学习', '项目', '工具', '技术']
        tags = []

        for keyword in keywords:
            if keyword in title or keyword in content:
                tags.append(keyword)
                if len(tags) >= 3:
                    break

        if not tags:
            tags = ['笔记']  # 默认标签

        # 简单的摘要生成
        summary = title.replace('训练', '').replace('小结', '').replace('总结', '')
        if len(summary) > 30:
            summary = summary[:30]
        if not summary:
            summary = "一篇技术笔记"

        return tags, summary

    def process_blog_file(self, file_path: Path, interactive: bool = True) -> bool:
        """处理 blog 文件"""
        print(f"\n📝 处理 blog 文件: {file_path.name}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否已经有 front matter
        if content.startswith('---'):
            # 找到 front matter 的结束位置
            end_match = re.search(r'\n---+\n', content[3:])
            if end_match:
                print(f"✅ 文件已有 front matter，跳过: {file_path.name}")
                return False

        # 提取标题（从文件名或内容）
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_path.stem

        # 生成英文文件名
        english_name = self.translate_chinese_to_english(title)
        new_file_name = f"{english_name}.md"

        print(f"📄 原标题: {title}")
        print(f"🔤 英文文件名: {new_file_name}")

        # 获取文件创建时间
        creation_time = self.get_file_creation_time(file_path)
        date_str = creation_time.strftime('%Y-%m-%d')

        # 提取正文内容（去掉标题）
        body_content = re.sub(r'^#\s+.+\n*', '', content, flags=re.MULTILINE).strip()

        # 生成或获取 tags 和 summary
        if interactive:
            print(f"\n🎯 当前内容预览: {body_content[:100]}...")

            # 询问是否手动输入 tags
            use_manual_tags = input("是否手动输入 tags？(y/n，默认n): ").strip().lower() == 'y'
            if use_manual_tags:
                tags_input = input("请输入 tags（用逗号分隔，最多3个）: ").strip()
                tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()][:3]
            else:
                tags, _ = self.generate_tags_and_summary(body_content, title)
                print(f"🤖 生成的 tags: {', '.join(tags)}")

            # 询问是否手动输入 summary
            use_manual_summary = input("是否手动输入 summary？(y/n，默认n): ").strip().lower() == 'y'
            if use_manual_summary:
                summary = input("请输入 summary（不超过30字）: ").strip()
                if len(summary) > 30:
                    summary = summary[:30]
            else:
                _, summary = self.generate_tags_and_summary(body_content, title)
                print(f"🤖 生成的 summary: {summary}")

            # 询问是否添加 weather 和 rating
            add_weather_rating = input("是否添加天气和心情评分？(y/n，默认n): ").strip().lower() == 'y'
            weather = None
            rating = None

            if add_weather_rating:
                weather = input("请输入天气（如：晴/雨/阴，或emoji如☀️/🌧️）: ").strip()
                if not weather:
                    weather = "晴"

                rating_input = input("请输入心情评分（1-5分）: ").strip()
                try:
                    rating = int(rating_input)
                    if rating < 1 or rating > 5:
                        rating = 3
                except ValueError:
                    rating = 3

        else:
            # 自动模式
            tags, summary = self.generate_tags_and_summary(body_content, title)
            print(f"🤖 生成的 tags: {', '.join(tags)}")
            print(f"🤖 生成的 summary: {summary}")

            # 自动生成 weather 和 rating
            weather = "晴"  # 默认天气
            rating = 3    # 默认心情
            print(f"🤖 默认天气: {weather}")
            print(f"🤖 默认心情评分: {rating}")

        # 构建新的 front matter
        front_matter_lines = [
            "---",
            f'title: "{title}"',
            f"date: {date_str}",
            f'summary: "{summary}"',
            f"tags: {json.dumps(tags, ensure_ascii=False)}",
            f'weather: "{weather}"' if weather else None,
            f"rating: {rating}" if rating else None,
            "draft: false",
            "---",
            ""
        ]

        # 过滤掉 None 的行
        front_matter_lines = [line for line in front_matter_lines if line is not None]
        front_matter = "\n".join(front_matter_lines) + "\n"

        # 组合新内容
        new_content = front_matter + body_content

        # 如果文件名需要更改，创建新文件
        if new_file_name != file_path.name:
            new_file_path = file_path.parent / new_file_name

            # 检查文件是否已存在
            if new_file_path.exists():
                print(f"⚠️  文件 {new_file_name} 已存在，跳过重命名")
                # 只在原文件更新内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ 已更新文件内容: {file_path.name}")
            else:
                # 创建新文件，删除旧文件
                with open(new_file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                file_path.unlink()  # 删除原文件
                print(f"✅ 已创建新文件: {new_file_name}")
        else:
            # 只更新内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ 已更新文件: {file_path.name}")

        return True

    def process_diary_file(self, file_path: Path) -> bool:
        """处理 diary 文件（保持原有逻辑）"""
        print(f"\n📔 处理 diary 文件: {file_path.name}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 获取文件创建时间
        creation_time = self.get_file_creation_time(file_path)
        date_str = creation_time.strftime('%Y-%m-%d %H:%M:%S')

        # 检查是否已有 front matter
        if content.startswith('---'):
            # 找到 front matter 的结束位置
            end_match = re.search(r'\n---+\n', content[3:])
            if end_match:
                # front matter 已存在，检查是否已有 date 字段
                front_matter = content[3:end_match.start()]
                if 'date:' in front_matter:
                    print(f"✅ 文件已有 date 字段，跳过: {file_path.name}")
                    return False

                # 在 front matter 中插入 date 字段
                new_content = content[:3] + f'\ndate: "{date_str}"' + content[3:end_match.start()] + content[end_match.start():]
            else:
                print(f"⚠️  front matter 格式不正确，跳过: {file_path.name}")
                return False
        else:
            # 没有 front matter，创建新的
            new_content = f"""---
date: "{date_str}"
---

{content}"""

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✅ 已添加时间戳: {date_str}")
        return True

    def process_directory(self, content_type: str, interactive: bool = True):
        """处理指定目录"""
        content_dir = self.project_root / 'src' / 'content' / content_type

        if not content_dir.exists():
            print(f"❌ 错误：找不到 {content_type} 目录 {content_dir}")
            return

        print(f"\n📁 开始处理 {content_type} 目录...")

        updated_files = []

        # 扫描所有 markdown 文件
        for file_path in content_dir.iterdir():
            if file_path.suffix.lower() in ['.md', '.markdown']:
                try:
                    if content_type == 'blog':
                        if self.process_blog_file(file_path, interactive):
                            updated_files.append(file_path.name)
                    elif content_type == 'diary':
                        if self.process_diary_file(file_path):
                            updated_files.append(file_path.name)
                except Exception as e:
                    print(f"❌ 处理文件 {file_path.name} 失败: {e}")

        # 输出结果
        if updated_files:
            print(f"\n✅ 成功处理了 {len(updated_files)} 个 {content_type} 文件：")
            for file_name in updated_files:
                print(f"  📝 {file_name}")
        else:
            print(f"✅ 没有需要处理的 {content_type} 文件")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Astro 内容管理脚本')
    parser.add_argument('--type', choices=['blog', 'diary'], required=True,
                       help='选择要处理的内容类型：blog 或 diary')
    parser.add_argument('--auto', action='store_true',
                       help='自动模式（不询问用户输入，全部自动生成）')

    args = parser.parse_args()

    manager = ContentManager()

    print(f"🚀 开始处理 {args.type} 内容...")
    manager.process_directory(args.type, interactive=not args.auto)
    print(f"\n🎉 {args.type} 内容处理完成！")


if __name__ == '__main__':
    main()