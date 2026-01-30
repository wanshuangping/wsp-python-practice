import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# 1. 读取数据
current_dir = os.path.dirname(os.path.abspath(__file__))
# 这里的路径和你之前成功读取 Excel 的路径保持一致
file_path = os.path.join(current_dir, "../../data/douban_css_final.xlsx")
df = pd.read_excel(file_path)

# 2. 提取电影名称并进行中文分词
titles = "".join(df['电影名称'].astype(str))
words = jieba.lcut(titles)
# 过滤掉单字（如“的”、“了”）和无效词
filtered_words = [w for w in words if len(w) > 1]
text = " ".join(filtered_words)

# 3. 生成词云图
# 注意：你需要指定一个中文字体文件路径，否则中文会显示为方块
# Mac 常用字体路径：/System/Library/Fonts/Supplemental/Arial Unicode.ttf
wc = WordCloud(
    font_path='/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
    width=1000,
    height=700,
    background_color='white',
    colormap='viridis'
).generate(text)

# 4. 显示与保存
plt.figure(figsize=(12, 8))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off') # 隐藏坐标轴
plt.show()

# 保存到 outputs 文件夹
output_path = os.path.join(current_dir, "../../data/outputs/movie_wordcloud.png")
wc.to_file(output_path)
print(f"✅ 词云图已生成并保存至: {output_path}")