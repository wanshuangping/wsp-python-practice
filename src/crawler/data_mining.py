import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. 设置中文字体（解决 Mac/Windows 绘图乱码）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS'] # Mac环境
plt.rcParams['axes.unicode_minus'] = False

# 2. 读取数据
current_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_excel(os.path.join(current_dir, "../../data/douban_top250_full.xlsx"))

# 3. 核心：拆分详情列（假设你的爬虫抓取了详情字段）
# 如果你的表格目前只有标题、评分、评价人数，我们需要微调爬虫抓取“年份/国家”
# 暂时我们先根据现有的评价人数进行深挖
df['评价人数数字'] = df['评价人数'].str.extract(r'(\d+)').astype(int)

# --- 挖掘点 A：计算“受众指数” ---
# 公式：评分 * log10(评价人数) —— 既要好评，又要出圈
import numpy as np
df['综合热度'] = df['评分'] * np.log10(df['评价人数数字'])

# 找出综合热度前5名
top_hot = df.nlargest(5, '综合热度')
print("🔥 豆瓣真正的‘全民顶流’电影：")
print(top_hot[['电影名称', '评分', '评价人数']])