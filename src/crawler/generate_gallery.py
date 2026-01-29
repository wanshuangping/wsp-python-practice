import os
import base64

# 1. 路径定位
current_dir = os.path.dirname(os.path.abspath(__file__))
# 定位到你的 data 文件夹
data_dir = os.path.abspath(os.path.join(current_dir, "../../data"))
img_dir = os.path.join(data_dir, "posters")

if not os.path.exists(img_dir):
    print(f"❌ 找不到文件夹: {img_dir}")
    exit()

# 2. 构建 HTML
html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>🎬 我的豆瓣私人影库 (内嵌版)</title>
    <style>
        body { background: #121212; color: #eee; text-align: center; font-family: sans-serif; padding: 30px; }
        .container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; }
        .card { width: 160px; background: #1e1e1e; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
        img { width: 100%; height: 235px; object-fit: cover; display: block; background: #333; }
        .title { padding: 12px 5px; font-size: 13px; font-weight: bold; background: #262626; height: 36px; overflow: hidden; }
    </style>
</head>
<body>
    <h1 style="color: #00b51d;">🎬 我的豆瓣 Top 250 私人影库</h1>
    <div class="container">
"""

# 3. 核心逻辑：将图片转为 Base64 字符串
posters = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.png'))]
print(f"📦 正在编码 {len(posters)} 张海报，请稍候...")

for p in sorted(posters):
    img_path = os.path.join(img_dir, p)
    name = p.rsplit('.', 1)[0]

    try:
        with open(img_path, "rb") as img_file:
            # 读取图片并转码
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
            # 插入到 HTML 中，直接作为 src
            html_content += f'''
                <div class="card">
                    <img src="data:image/jpeg;base64,{encoded_string}" alt="{name}">
                    <div class="title">{name}</div>
                </div>'''
    except Exception as e:
        print(f"⚠️ 跳过图片 {p}: {e}")

html_content += "</div></body></html>"

# 4. 写入文件
output_path = os.path.join(data_dir, "my_movies_embedded.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ 大功告成！文件已生成：{output_path}")
print("💡 现在你直接双击这个文件，哪怕图片文件夹删了，图片也依然能显示！")