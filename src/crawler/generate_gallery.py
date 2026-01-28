import os

# 1. 绝对定位：确保 HTML 和 posters 文件夹在同一个地方
current_dir = os.path.dirname(os.path.abspath(__file__))
# 这里的路径根据你的项目结构调整，确保最终指向 data 目录
data_dir = os.path.abspath(os.path.join(current_dir, "../../data"))
img_dir = os.path.join(data_dir, "posters")

if not os.path.exists(img_dir):
    print(f"❌ 找不到图片文件夹: {img_dir}")
    exit()

posters = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.png'))]

# 2. 构建 HTML
html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>🎬 我的私人影库</title>
    <style>
        body { background: #121212; color: white; text-align: center; font-family: sans-serif; padding: 50px; }
        .container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; }
        .card { width: 160px; background: #1e1e1e; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
        img { width: 100%; height: 230px; object-fit: cover; display: block; }
        .title { padding: 12px 5px; font-size: 13px; height: 32px; overflow: hidden; background: #262626; }
    </style>
</head>
<body>
    <h1 style="color: #00b51d;">🎬 我的豆瓣 Top 250 私人影库</h1>
    <div class="container">
"""

for p in sorted(posters):
    name = p.rsplit('.', 1)[0]
    # 使用最简单的相对路径
    html_content += f'''
        <div class="card">
            <img src="posters/{p}" alt="{name}">
            <div class="title">{name}</div>
        </div>'''

html_content += "</div></body></html>"

# 3. 保存
output_file = os.path.join(data_dir, "my_movies.html")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ 网页已生成！请去文件夹里手动打开：\n{output_file}")