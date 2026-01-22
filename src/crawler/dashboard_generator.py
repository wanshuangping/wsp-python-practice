import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. 载入并清洗数据
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "../../data/douban_top250_full.xlsx")
df = pd.read_excel(file_path)

# 清洗评价人数：转为纯数字
df['评价人数数字'] = df['评价人数'].str.extract(r'(\d+)').fillna(0).astype(int)

# 2. 炫技图表一：评价人数与评分的 3D 气泡图
# 我们用气泡大小代表评价人数，用颜色代表评分高低
fig = px.scatter(df, x="评分", y="评价人数数字",
                 size="评价人数数字", color="评分",
                 hover_name="电影名称",
                 log_y=True, # 使用对数轴，让数据分布更美观
                 title="豆瓣 Top 250 电影洞察：谁是真正的顶流？",
                 labels={"评价人数数字": "评价人数 (人)", "评分": "豆瓣评分"},
                 color_continuous_scale=px.colors.sequential.Viridis)

# 3. 炫技图表二：评分段的分布情况 (饼图)
# 划分评分等级
bins = [0, 8.5, 9.0, 9.5, 10]
labels = ['普通好片 (8.0-8.5)', '口碑佳作 (8.5-9.0)', '必看神作 (9.0-9.5)', '史诗传奇 (9.5+)']
df['评分等级'] = pd.cut(df['评分'], bins=bins, labels=labels)
rating_pie = px.pie(df, names='评分等级', title='Top 250 评分构成',
                   color_discrete_sequence=px.colors.sequential.RdBu)

# 4. 自动生成一个单页 HTML 报告
# 这样你可以把这个文件发给任何人，他们用浏览器就能打开，不需要安装 Python
output_html = os.path.join(current_dir, "../../data/douban_interactive_report.html")

with open(output_html, 'w', encoding='utf-8') as f:
    f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(rating_pie.to_html(full_html=False, include_plotlyjs='cdn'))

print(f"🔥 炫技成功！交互式仪表盘已生成：{output_html}")
import webbrowser

# 在 print 语句下面增加：
webbrowser.open(f"file://{os.path.abspath(output_html)}")
