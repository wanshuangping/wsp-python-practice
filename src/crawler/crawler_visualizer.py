import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. 加载数据
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "../../data/douban_top250_full.xlsx")

if not os.path.exists(file_path):
    print("❌ 找不到数据文件！")
else:
    df = pd.read_excel(file_path)

    # --- 数据清洗逻辑 (修复报错的关键) ---
    # 提取数字，如果提取不到则设为 0
    df['评价人数数字'] = df['评价人数'].str.extract('(\d+)').fillna(0).astype(int)

    # 确保评分也是数字格式
    df['评分'] = pd.to_numeric(df['评分'], errors='coerce').fillna(0)

    # 2. 设置中文字体 (针对 Mac 优化)
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
    plt.style.use('ggplot')

    # 创建画布
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # --- 左图：评分分布 ---
    ax1.hist(df['评分'], bins=15, color='skyblue', edgecolor='white')
    ax1.set_title('豆瓣电影 Top 250 评分分布', fontsize=14)
    ax1.set_xlabel('评分')
    ax1.set_ylabel('电影数量')

    # --- 右图：评分与评价人数的关系 ---
    ax2.scatter(df['评分'], df['评价人数数字'], alpha=0.5, color='salmon')
    ax2.set_title('评分 vs 评价人数', fontsize=14)
    ax2.set_xlabel('评分')
    ax2.set_ylabel('评价人数 (人)')

    plt.tight_layout()

    # 保存并展示
    output_img = os.path.join(current_dir, "../../data/douban_analysis.png")
    plt.savefig(output_img)
    print(f"✅ 可视化图表已更新并保存至: {output_img}")
    plt.show()