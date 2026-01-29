import pandas as pd
import os

# 1. 准确定位项目根目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 向上跳两级回到 pythonProject
project_root = os.path.dirname(os.path.dirname(current_dir))
# 定位到 data 文件夹
data_folder = os.path.join(project_root, "data")

# 2. 拼接正确的文件路径 (根据截图，文件直接在 data 文件夹下)
file_path = os.path.join(data_folder, "douban_css_final.xlsx")

print(f"🔍 正在尝试读取文件: {file_path}")

if not os.path.exists(file_path):
    print("❌ 路径依然不对！请查看下方 data 文件夹里的实际文件列表：")
    print(os.listdir(data_folder))
else:
    df = pd.read_excel(file_path)
    print("✅ 读取成功！")
    print(df.head()) # 显示前5行数据

import matplotlib.pyplot as plt
import seaborn as sns

# 1. 设置中文字体（解决图表乱码的关键）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 2. 创建画布
plt.figure(figsize=(10, 6))

# 3. 绘制直方图和核密度曲线
# 注意：确保你的 Excel 列名确实叫 '评分'
sns.histplot(df['评分'], bins=10, kde=True, color='#00b51d')

# 4. 设置标题和标签
plt.title('豆瓣电影 Top 250 评分分布情况', fontsize=15)
plt.xlabel('电影评分', fontsize=12)
plt.ylabel('电影数量', fontsize=12)

# 5. 保存并展示
output_img = os.path.join(data_folder, "outputs/rating_dist.png")
plt.savefig(output_img)
print(f"🎨 评分分布图已保存至: {output_img}")
plt.show()