import os
from pathlib import Path
import urllib.parse

# 1. 自动获取你的项目 data/posters 路径
current_dir = Path(__file__).resolve().parent
# 向上跳两级到项目根目录，再进入 data/posters
img_dir = current_dir.parents[1] / "data" / "posters"

if not img_dir.exists():
    print(f"❌ 找不到图片文件夹，请检查路径: {img_dir}")
    exit()

# 2. 构建 HTML
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🎬 最终调试版-私人影库</title>
    <style>
        body { background: #121212; color: white; font-family: sans-serif; text-align: center; padding: 30px; }
        .container { display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; }
        .card { width: 150px; background: #1e1e1e; border-radius: 10px; overflow: hidden; }
        img { width: 100%; height: 220px; object-fit: cover; background: #333; }
        .title { padding: 8px; font-size: 12px; height: 30px; overflow: hidden; }
    </style>
</head>
<body>
    <h1 style="color: #00b51d;">🎬 我的豆瓣 Top 250 (路径修复版)</h1>
    <div class="container">
"""

# 获取所有 jpg 图片并生成绝对链接
for img_file in sorted(img_dir.glob("*.jpg")):
    name = img_file.stem
    # 【核心修复】将 Path 对象转为浏览器可识别的 file:// 链接
    file_url = img_file.as_uri()

    html_content += f'''
        <div class="card">
            <img src="{file_url}" alt="{name}">
            <div class="title">{name}</div>
        </div>'''

html_content += "</div></body></html>"

# 3. 还是保存到桌面，方便你直接双击
output_path = Path.home() / "Desktop" / "check_this_one.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ 脚本已运行完毕！")
print(f"👉 请去桌面找到【check_this_one.html】，右键选择 Chrome 打开。")