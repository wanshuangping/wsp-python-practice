import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. 基础设置
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS'] # Mac 字体适配
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid", font='Arial Unicode MS')

# 2. 读取数据
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "../../data/douban_top250_full.xlsx")
df = pd.read_excel(file_path)

# 3. 创建画布（一板两图）
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

# --- 挖掘 A：黄金年代趋势 (折线图) ---
# 清洗年份数据，只保留数字
df['年份数字'] = pd.to_numeric(df['上映年份'], errors='coerce')
year_stats = df['年份数字'].value_counts().sort_index()

sns.lineplot(x=year_stats.index, y=year_stats.values, ax=ax1, color='#e74c3c', linewidth=2, marker='o')
ax1.fill_between(year_stats.index, year_stats.values, color='#e74c3c', alpha=0.1)
ax1.set_title('🎬 豆瓣 Top 250：影史神作产出年份趋势', fontsize=15, pad=15)
ax1.set_xlabel('年份')
ax1.set_ylabel('入榜数量')

# --- 挖掘 B：国家实力分布 (柱状图) ---
# 清洗国家数据，取第一个主产地
df['主产国'] = df['国家'].str.split(' ').str[0]
country_counts = df['主产国'].value_counts().head(10) # 取前 10

sns.barplot(x=country_counts.values, y=country_counts.index, ax=ax2, palette='viridis')
ax2.set_title('🌍 豆瓣 Top 250：全球制片实力 Top 10', fontsize=15, pad=15)
ax2.set_xlabel('入榜电影部数')

# 自动调整布局并展示
plt.tight_layout()
plt.show()

# 4. 打印一个有趣的结论
peak_year = year_stats.idxmax()
print(f"💡 数据洞察：豆瓣影迷心中最伟大的‘黄金年代’是 {int(peak_year)} 年！")