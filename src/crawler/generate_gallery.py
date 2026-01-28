import os

# 1. 定位海报文件夹 (使用绝对路径避免混乱)
current_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(current_dir, "../../data/posters")

if not os.path.exists(img_dir):
    print(f"❌ 找不到海报文件夹: {img_dir}")
    exit()

# 获取所有 jpg 图片
posters = [f for f in os.listdir(img_dir) if f.endswith('.jpg')]

# 2. 构建 HTML 内容
# 注意开头的 f"""，这能让后面的 {name} 被实际变量替换
html_header = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>🎬 我的豆瓣 Top 250 私人影库</title>
    <style>
        body { background: #121212; color: #eee; text-align: center; font-family: 'PingFang SC', sans-serif; margin: 0; padding: 20px; }
        h1 { color: #00b51d; margin-bottom: 30px; }
        .container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; }
        .movie-card { width: 160px; background: #1e1e1e; border-radius: 12px; overflow: hidden; transition: 0.3s; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
        .movie-card:hover { transform: translateY(-10px); box-shadow: 0 15px 30px rgba(0,181,29,0.3); }
        img { width: 100%; height: 230px; object-fit: cover; }
        .title { padding: 10px; font-size: 13px; height: 36px; line-height: 1.4; display: flex; align-items: center; justify-content: center; }
    </style>
</head>
<body>
    <h1>🎬 我的豆瓣 Top 250 私人影库</h1>
    <div class="container">
"""

html_footer = """
    </div>
</body>
</html>
"""

# 动态生成每部电影的格子
movie_items = ""
for p in sorted(posters):
    name = p.replace(".jpg", "")
    # 使用 f-string 插入图片路径和名称
    item_html = f'''
        <div class="movie-card">
            <img src="./posters/{p}" alt="{name}">
            <div class="title">{name}</div>
        </div>'''
    movie_items += item_html

# 3. 写入文件
output_path = os.path.join(current_dir, "../../data/my_movies.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_header + movie_items + html_footer)

print(f"✅ 修复完成！请重新刷新浏览器打开: {output_path}")