import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import re
import warnings

# 1. 屏蔽烦人的 pkg_resources 警告
warnings.filterwarnings("ignore", category=UserWarning)

# 2. 设置中文字体（Matplotlib 绘图使用）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def generate_movie_wordcloud():
    # 3. 定位数据文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "../../data/douban_top250_full.xlsx")

    if not os.path.exists(file_path):
        print(f"❌ 找不到数据文件: {file_path}")
        return

    df = pd.read_excel(file_path)

    # 4. 数据清洗：提取电影类型
    df['类型'] = df['类型'].fillna('').astype(str)
    all_genres = []

    for genres_str in df['类型']:
        # 移除括号内容并按斜杠或空格拆分
        clean_text = re.sub(r'\(.*?\)', '', genres_str)
        # 豆瓣格式通常是 "剧情 / 爱情"，拆分并去空格
        genres_list = [g.strip() for g in re.split(r'[/\s,、]', clean_text) if g.strip()]
        all_genres.extend(genres_list)

    if not all_genres:
        print("⚠️ 没有提取到任何类型数据，请检查 Excel 中的 '类型' 列。")
        return

    # 将列表转为词云需要的长文本
    text_for_cloud = " ".join(all_genres)

    # 5. 生成词云（针对 Mac 路径优化）
    # Mac 路径通常为 /System/Library/Fonts/Supplemental/Arial Unicode.ttf
    # 或者 /System/Library/Fonts/STHeiti Light.ttc
    mac_font = '/System/Library/Fonts/STHeiti Light.ttc'

    try:
        wc = WordCloud(
            font_path=mac_font,
            background_color="white",
            width=1000,
            height=700,
            max_words=100,
            collocations=False,
            colormap='viridis'  # 给词云换个好看的颜色
        ).generate(text_for_cloud)

        # 6. 绘图与展示
        plt.figure(figsize=(12, 8))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.title('豆瓣电影 Top 250：类型分布词云', fontsize=20, pad=20)

        # 自动保存一份图片到 data 文件夹
        output_img = os.path.join(current_dir, "../../data/movie_wordcloud.png")
        plt.savefig(output_img)
        print(f"✅ 词云图已生成并保存至: {output_img}")

        plt.show()

    except Exception as e:
        print(f"❌ 词云渲染失败: {e}")
        print("💡 请检查 Mac 字体路径是否正确，或尝试在终端执行: pip install --upgrade wordcloud")


if __name__ == "__main__":
    generate_movie_wordcloud()