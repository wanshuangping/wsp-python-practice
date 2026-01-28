import os

# 1. 精确定位路径
# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# HTML 文件的目标目录是 project/data
data_dir = os.path.normpath(os.path.join(current_dir, "../../data"))
# 图片文件夹是 project/data/posters
img_dir = os.path.join(data_dir, "posters")

if not os.path.exists(img_dir):
    print(f"❌ 找不到图片文件夹，请检查: {img_dir}")
    exit()

# 获取所有 .jpg 文件
posters = [f for f in os.listdir(img_dir) if f.lower().endswith('.jpg')]

# 2. 构建 HTML 内容
html_header = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>🎬 我的豆瓣 Top 250 私人影库</title>
    <style>
        body { background: #121212; color: #eee; text-align: center; font-family: sans-serif; margin: 0; padding: 30px; }
        h1 { color: #00b51d; margin-bottom: 40px; }
        .container { display: flex; flex-wrap: wrap; justify-content: center; gap: 25px; }
        .movie-card { width: 150px; background: #1e1e1e; border-radius: 10px; overflow: hidden; box-shadow: 0 8px 20px rgba(0,0,0,0.5); transition: 0.3s; }
        .movie-card:hover { transform: translateY(-8px); }
        img { width: 100%; height: 220px; object-fit: cover; display: block; }
        .title { padding: 12px 5px; font-size: 13px; height: 32px; line-height: 1.3; overflow: hidden; display: flex; align-items: center; justify-content: center; }
    </style>
</head>
<body>
    <h1>🎬 我的豆瓣 Top 250 私人影库</h1>
    <div class="container">
"""

movie_items = ""
for p in sorted(posters):
    # 移除后缀作为显示名称
    name = p.rsplit('.', 1)[0]
    # 重要修复：因为 HTML 在 data 目录下，图片在 posters 子目录下
    # 路径引用必须是 posters/文件名.jpg
    movie_items += f'''
        <div class="movie-card">
            <img src="posters/{p}" alt="{name}">
            <div class="title">{name}</div>
        </div>'''

html_footer = """
    </div>
</body>
</html>
"""

# 3. 写入文件
output_path = os.path.join(data_dir, "my_movies.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_header + movie_items + html_footer)

print(f"✅ 修复版网页已生成！路径: {output_path}")
print(f"💡 提示：请直接在文件管理器中双击打开该 HTML 文件，不要只在 PyCharm 预览里看。")