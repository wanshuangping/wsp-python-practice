import pandas as pd
import plotly.express as px
import os
import webbrowser

# 1. 载入已经修复好的数据
current_dir = os.path.dirname(os.path.abspath(__file__))
# 确保路径指向你刚刚生成的那个充满数据的 Excel
file_path = os.path.join(current_dir, "../../data/douban_top250_full.xlsx")
df = pd.read_excel(file_path)

# 2. 深度清洗（将 "123人评价" 提取为数字 123）
df['评价人数数字'] = df['评价人数'].astype(str).str.extract(r'(\d+)').fillna(0).astype(int)

# 剔除掉极少数可能解析失败的 0 值，确保对数轴正常
df = df[df['评价人数数字'] > 0]

# 3. 炫技：构建 3D 视觉感的交互散点图
fig = px.scatter(df, x="评分", y="评价人数数字",
                 size="评价人数数字", color="评分",
                 hover_name="电影名称",
                 log_y=True,
                 title="豆瓣电影 Top 250：人气与口碑双维度看板",
                 labels={"评价人数数字": "累计评价人数", "评分": "豆瓣评分"},
                 template="plotly_dark", # 科技感暗黑主题
                 color_continuous_scale=px.colors.sequential.Plasma)

# 4. 保存并自动展示
output_html = os.path.join(current_dir, "../../data/douban_final_report.html")
fig.write_html(output_html)

print(f"🔥 华丽谢幕！交互看板已生成：{output_html}")
webbrowser.open(f"file://{os.path.abspath(output_html)}")