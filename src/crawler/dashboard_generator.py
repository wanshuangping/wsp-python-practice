import pandas as pd
import plotly.express as px
import os
import webbrowser

# 1. 载入数据
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "../../data/douban_top250_full.xlsx")
df = pd.read_excel(file_path)

# --- 🧪 数据清洗：强化版正则 ---
# 豆瓣的格式是 "1673082人评价"，我们要的是前面那一串数字
df['评价人数数字'] = df['评价人数'].astype(str).str.extract(r'(\d+)').fillna(0).astype(int)

# 打印前5条看看，确保这里不是 0！
print("📋 检查清洗后的前5条评价人数：")
print(df[['电影名称', '评价人数数字']].head())

# 过滤掉为 0 的异常值（防止 log 轴崩溃）
df = df[df['评价人数数字'] > 0]

if df.empty:
    print("❌ 错误：所有数据的评价人数都为 0，请检查 Excel 里的 '评价人数' 列格式！")
else:
    # 2. 绘制气泡图
    fig = px.scatter(df, x="评分", y="评价人数数字",
                     size="评价人数数字", color="评分",
                     hover_name="电影名称",
                     log_y=True,
                     title="豆瓣 Top 250 电影洞察 (交互式看板)",
                     labels={"评价人数数字": "评价人数", "评分": "豆瓣评分"},
                     template="plotly_dark",
                     color_continuous_scale="Viridis")

    # 3. 保存并【强行】弹出
    output_html = os.path.join(current_dir, "../../data/douban_interactive_report.html")
    # 确保文件夹存在
    os.makedirs(os.path.dirname(output_html), exist_ok=True)

    fig.write_html(output_html)
    print(f"🔥 报告已生成：{output_html}")

    # 使用绝对路径，强制浏览器打开
    full_path = "file://" + os.path.abspath(output_html)
    webbrowser.open(full_path, new=2)