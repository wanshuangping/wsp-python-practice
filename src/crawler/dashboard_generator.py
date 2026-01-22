import pandas as pd
import plotly.express as px
import os
import webbrowser

# 1. 载入并清洗数据
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "../../data/douban_top250_full.xlsx")
df = pd.read_excel(file_path)

# --- 核心修复：正则表达式加上 r，并确保数字大于 0 ---
# 使用 r'(\d+)' 确保准确抓取数字
df['评价人数数字'] = df['评价人数'].str.extract(r'(\d+)').fillna(0).astype(int)

# 过滤掉评价人数为 0 的异常数据，防止 log_y 报错
df = df[df['评价人数数字'] > 0]

# 2. 炫技图表一：评价人数与评分的 3D 气泡图
fig = px.scatter(df, x="评分", y="评价人数数字",
                 size="评价人数数字", color="评分",
                 hover_name="电影名称", # 鼠标悬停显示电影名
                 log_y=True,
                 title="豆瓣 Top 250 电影洞察：谁是真正的顶流？",
                 labels={"评价人数数字": "评价人数 (人)", "评分": "豆瓣评分"},
                 template="plotly_dark", # 使用酷炫的暗黑模式
                 color_continuous_scale=px.colors.sequential.Viridis)

# 3. 炫技图表二：评分段分布饼图
bins = [0, 8.5, 9.0, 9.5, 10]
labels = ['普通好片', '口碑佳作', '必看神作', '史诗传奇']
df['评分等级'] = pd.cut(df['评分'], bins=bins, labels=labels)
rating_pie = px.pie(df, names='评分等级', title='Top 250 评分构成',
                   hole=0.4, # 变成环形图，更高级
                   color_discrete_sequence=px.colors.sequential.RdBu)

# 4. 生成并保存 HTML
output_html = os.path.join(current_dir, "../../data/douban_interactive_report.html")
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(rating_pie.to_html(full_html=False, include_plotlyjs='cdn'))

print(f"🔥 炫技成功！交互式仪表盘已生成：{output_html}")

# --- 核心修复：自动在浏览器打开结果 ---
webbrowser.open(f"file://{os.path.abspath(output_html)}")