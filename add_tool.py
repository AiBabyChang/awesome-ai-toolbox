#!/usr/bin/env python3
"""
add_tool.py — 往 awesome-ai-toolbox 收藏夹添加项目
用法：
  python3 add_tool.py --repo "https://github.com/xxx/yyy" --name "项目名" \
      --desc "中文一句话介绍" --tags "标签1,标签2" --category "AI Agent" \
      --stars "13.8k" --source "https://x.com/..." [--date "2026-08-25"]

流程：追加到 data/tools.json → 重新生成 README（按分类分组）→ git commit
"""
import argparse, json, datetime
from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE / 'data' / 'tools.json'

CATEGORY_ORDER = ['AI Agent', 'AI 视频', 'AI 聊天', '金融数据', '免费资源', '效率工具', '学习资源', '其他']
CATEGORY_EMOJI = {
    'AI Agent': '🤖', 'AI 视频': '🎬', 'AI 聊天': '💬', '金融数据': '📊',
    '免费资源': '🆓', '效率工具': '⚡', '学习资源': '📚', '其他': '📦'
}
CATEGORY_ANCHOR = {
    'AI Agent': '-ai-agent', 'AI 视频': '-ai-视频', 'AI 聊天': '-ai-聊天',
    '金融数据': '-金融数据', '免费资源': '-免费资源', '效率工具': '-效率工具', '学习资源': '-学习资源', '其他': '其他'
}

def load_tools():
    if DATA.exists():
        return json.loads(DATA.read_text(encoding='utf-8'))
    return []

def save_tools(tools):
    DATA.parent.mkdir(exist_ok=True)
    DATA.write_text(json.dumps(tools, ensure_ascii=False, indent=2), encoding='utf-8')

def render_readme(tools):
    today = datetime.date.today().isoformat()
    # 统计
    cats = {}
    for t in tools:
        cats.setdefault(t['category'], []).append(t)
    ordered = [c for c in CATEGORY_ORDER if c in cats] + [c for c in cats if c not in CATEGORY_ORDER]

    lines = []
    lines.append('# 🧰 AI 工具箱 · Awesome AI Toolbox')
    lines.append('')
    lines.append('> 每日从 Twitter 精选的 GitHub AI 项目收藏夹｜中文介绍 · 分类标签 · 持续更新')
    lines.append('>')
    lines.append('> 🔔 同步发布：Twitter [@Thuweni1](https://x.com/Thuweni1) · 小红书 @Ai.BabyChang')
    lines.append('')
    lines.append('## 📚 分类目录')
    lines.append('')
    lines.append('| 分类 | 收录数 |')
    lines.append('|------|--------|')
    for c in ordered:
        lines.append(f"| [{CATEGORY_EMOJI.get(c,'📦')} {c}](#{CATEGORY_ANCHOR.get(c,'其他')}) | {len(cats[c])} |")
    lines.append('')
    lines.append(f'**共收录 {len(tools)} 个项目**（更新至 {today}）')
    lines.append('')
    lines.append('---')
    lines.append('')

    for c in ordered:
        lines.append(f"## {CATEGORY_EMOJI.get(c,'📦')} {c}")
        lines.append('')
        for t in cats[c]:
            stars = f" ⭐{t['stars']}" if t.get('stars') else ''
            lines.append(f"### [{t['name']}]({t['repo']}){stars}")
            lines.append(f"> {t['desc']}")
            lines.append('')
            tags = ' · '.join(f'`{x.strip()}`' for x in t.get('tags', []).split(',') if x.strip())
            src = f" · [原帖]({t['source']})" if t.get('source') else ''
            lines.append(f"- 🏷️ 标签：{tags}")
            lines.append(f"- 📅 收录：{t.get('date', today)}{src}")
            lines.append('')
        lines.append('---')
        lines.append('')

    lines.append('## 📌 收录标准')
    lines.append('')
    lines.append('1. 从 Twitter 精选的 GitHub 项目（AI/编程/效率方向）')
    lines.append('2. 开源、免费或可自部署优先')
    lines.append('3. 中文一句话介绍 + 分类标签 + 原帖溯源')
    lines.append('')
    lines.append('## 🔄 更新方式')
    lines.append('')
    lines.append('每次双平台（Twitter @Thuweni1 + 小红书 @Ai.BabyChang）同步发布后，自动入库更新本仓库。')
    lines.append('')
    lines.append('## 📄 License')
    lines.append('')
    lines.append('CC BY-NC-SA 4.0（转载注明出处）')
    lines.append('')

    (BASE / 'README.md').write_text('\n'.join(lines), encoding='utf-8')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--name', required=True)
    ap.add_argument('--desc', required=True)
    ap.add_argument('--tags', default='')
    ap.add_argument('--category', default='其他')
    ap.add_argument('--stars', default='')
    ap.add_argument('--source', default='')
    ap.add_argument('--date', default=datetime.date.today().isoformat())
    a = ap.parse_args()

    tools = load_tools()
    # 去重
    if any(t['repo'] == a.repo for t in tools):
        print(f'ALREADY_EXISTS: {a.repo}')
        return
    tools.append({
        'repo': a.repo, 'name': a.name, 'desc': a.desc, 'tags': a.tags,
        'category': a.category, 'stars': a.stars, 'source': a.source, 'date': a.date
    })
    save_tools(tools)
    render_readme(tools)
    print(f'ADDED: {a.name} → {a.category}（共 {len(tools)} 项）')
    print('README 已重新生成。记得 git add -A && git commit && git push')

if __name__ == '__main__':
    main()