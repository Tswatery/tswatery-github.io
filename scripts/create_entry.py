#!/usr/bin/env python3
"""快速为 blog/diary 创建带 frontmatter 的内容文件。"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = PROJECT_ROOT / 'src' / 'content' / 'blog'
DIARY_DIR = PROJECT_ROOT / 'src' / 'content' / 'diary'


def slugify(value: str, fallback_prefix: str) -> str:
    base = re.sub(r'[^a-z0-9]+', '-', value.strip().lower())
    base = re.sub(r'-{2,}', '-', base).strip('-')
    return base or f"{fallback_prefix}-{datetime.now():%Y%m%d%H%M%S}"


def prompt(label: str, *, default: str | None = None, preset: str | None = None, allow_empty: bool = False) -> str:
    if preset not in (None, ''):
        return preset

    suffix = f" [{default}]" if default else ''
    while True:
        value = input(f"{label}{suffix}: ").strip()
        if not value and default is not None:
            return default
        if value or allow_empty:
            return value
        print('请输入内容，可使用 Ctrl+C 退出。')


def to_json_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def parse_tags(raw: str, fallback: list[str]) -> list[str]:
    parts = [part.strip() for part in raw.split(',') if part.strip()]
    return parts or fallback


def ensure_extension(name: str, *, default: str) -> str:
    return name if name.endswith(default) else f"{name}{default}"


def write_blog_entry(args: argparse.Namespace) -> Path:
    title = prompt('文章标题', preset=args.title)
    summary = prompt('摘要 (<=30 字)', default=title[:30], preset=args.summary)
    tags_raw = prompt('标签（逗号分隔）', default='随笔', preset=args.tags or '')
    tags = parse_tags(tags_raw, ['随笔'])
    weather = prompt('天气（支持 emoji 或文字）', default='☀️', preset=args.weather)
    mood = prompt('心情（支持 emoji 或文字）', default='😊', preset=args.mood)
    rating_default = str(args.rating if args.rating else 3)
    rating_input = prompt('心情评分 (1-5)', default=rating_default)
    try:
        rating = max(1, min(5, int(rating_input)))
    except ValueError:
        rating = 3

    filename_seed = args.filename or slugify(title, 'post')
    filename = ensure_extension(filename_seed, default='.md')
    target = BLOG_DIR / filename
    if target.exists():
        raise SystemExit(f"❌ 文件已存在：{target}")

    BLOG_DIR.mkdir(parents=True, exist_ok=True)

    lines = [
        '---',
        f"title: {to_json_scalar(title)}",
        f"date: {datetime.now():%Y-%m-%d}",
        f"summary: {to_json_scalar(summary)}",
        f"tags: {json.dumps(tags, ensure_ascii=False)}",
        f"weather: {to_json_scalar(weather)}",
        f"mood: {to_json_scalar(mood)}",
        f"rating: {rating}",
        f"draft: {'true' if args.draft else 'false'}",
        '---',
        '',
        '在这里写正文…',
    ]
    target.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return target


def write_diary_entry(args: argparse.Namespace) -> Path:
    now = datetime.now()
    title = prompt('小记标题（可留空）', preset=args.title, allow_empty=True)
    weather = prompt('天气（支持 emoji 或文字）', default='☀️', preset=args.weather)
    mood = prompt('心情（支持 emoji 或文字）', default='😊', preset=args.mood)
    rating_default = str(args.rating if args.rating else 3)
    rating_input = prompt('心情评分 (1-5)', default=rating_default)
    try:
        rating = max(1, min(5, int(rating_input)))
    except ValueError:
        rating = 3
    tags_input = prompt('标签（可选，逗号分隔）', preset=args.tags or '', allow_empty=True)
    tags = parse_tags(tags_input, []) if tags_input else []

    filename_seed = args.filename or (title.strip() if title else f"diary-{now:%Y%m%d-%H%M%S}")
    filename = ensure_extension(filename_seed, default='.md')
    target = DIARY_DIR / filename
    if target.exists():
        raise SystemExit(f"❌ 文件已存在：{target}")

    DIARY_DIR.mkdir(parents=True, exist_ok=True)

    lines = [
        '---',
        f"date: {to_json_scalar(now.strftime('%Y-%m-%d %H:%M:%S'))}",
    ]
    if title:
        lines.append(f"title: {to_json_scalar(title)}")
    lines.extend([
        f"mood: {to_json_scalar(mood)}",
        f"rating: {rating}",
        f"weather: {to_json_scalar(weather)}",
    ])
    if tags:
        lines.append('tags:')
        lines.extend([f"  - {tag}" for tag in tags])
    lines.extend(['---', '', '随手记一记…'])
    target.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description='为 blog 或 diary 初始化 frontmatter。')
    parser.add_argument('--type', choices=['blog', 'diary'], required=True, help='内容类型')
    parser.add_argument('--title', help='标题（可选，留空则运行时输入）')
    parser.add_argument('--summary', help='blog 摘要')
    parser.add_argument('--tags', help='逗号分隔的标签列表')
    parser.add_argument('--weather', help='天气，支持 emoji')
    parser.add_argument('--mood', help='心情，支持 emoji')
    parser.add_argument('--rating', type=int, help='心情评分 1-5')
    parser.add_argument('--filename', help='自定义文件名（含扩展名或不含）')
    parser.add_argument('--draft', action='store_true', help='blog 是否标记为草稿')
    args = parser.parse_args()

    if args.type == 'blog':
        target = write_blog_entry(args)
    else:
        target = write_diary_entry(args)

    print(f"✅ 已创建：{target.relative_to(PROJECT_ROOT)}")


if __name__ == '__main__':
    main()
