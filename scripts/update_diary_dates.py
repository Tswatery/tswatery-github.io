#!/usr/bin/env python3
"""
自动为日记文件添加创建时间到 front matter

使用方式：
1. 在 src/content/diary/ 目录下创建或编辑 .md 文件
2. 运行：python scripts/update_diary_dates.py
3. 脚本会自动为缺少 date 字段的文件添加创建时间
"""

import os
import re
from pathlib import Path
from datetime import datetime
import locale

# 设置中文时间格式
locale.setlocale(locale.LC_TIME, 'zh_CN.UTF-8')


def get_file_creation_time(file_path):
    """获取文件创建时间（优先创建时间，回退到修改时间）"""
    stat = os.stat(file_path)
    # 优先使用创建时间，如果没有则使用修改时间
    creation_time = stat.st_birthtime if hasattr(stat, 'st_birthtime') else stat.st_ctime
    return datetime.fromtimestamp(creation_time)


def format_datetime(dt):
    """格式化日期时间为 'YYYY-MM-DD HH:MM:SS' 格式"""
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def update_file_with_date(file_path, date_str):
    """为文件添加 date 字段到 front matter"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已有 front matter
    if content.startswith('---'):
        # 找到 front matter 的结束位置
        end_match = re.search(r'\n---+\n', content[3:])
        if end_match:
            # front matter 已存在，检查是否已有 date 字段
            front_matter = content[3:end_match.start()]
            if 'date:' in front_matter:
                # 已有 date 字段，跳过
                return False

            # 在 front matter 中插入 date 字段（插在第一行）
            new_content = content[:3] + '\ndate: "' + date_str + '"' + content[3:end_match.start()] + content[end_match.start():]
        else:
            # 格式不正确，跳过
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

    return True


def main():
    """主函数"""
    # 日记目录路径
    diary_dir = Path(__file__).parent.parent / 'src' / 'content' / 'diary'

    if not diary_dir.exists():
        print(f"❌ 错误：找不到日记目录 {diary_dir}")
        return

    # 扫描所有 markdown 文件
    updated_files = []
    for file_path in diary_dir.iterdir():
        if file_path.suffix.lower() in ['.md', '.markdown']:
            # 获取文件的创建时间
            creation_time = get_file_creation_time(file_path)
            date_str = format_datetime(creation_time)

            # 尝试更新文件
            if update_file_with_date(file_path, date_str):
                updated_files.append({
                    'name': file_path.name,
                    'date': date_str,
                    'path': file_path
                })

    # 输出结果
    if updated_files:
        print(f"✅ 成功更新了 {len(updated_files)} 个文件：\n")
        for file_info in updated_files:
            print(f"  📝 {file_info['name']}")
            print(f"     → date: {file_info['date']}\n")
    else:
        print("✅ 所有文件都已经有 date 字段，无需更新")


if __name__ == '__main__':
    main()
