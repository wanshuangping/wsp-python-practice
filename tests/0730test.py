import pandas as pd
import os

# 文件路径
file_path = "/Users/temu/Downloads/订单导出2026730001.xlsx"

# 校验文件是否存在（防止路径写错报错）
if os.path.exists(file_path):
    df = pd.read_excel(file_path, engine="openpyxl")
    print("✅ 文件读取成功！")
    print("数据表前5行：")
    print(df.head())
    print("\n所有列名：")
    print(df.columns.tolist())
else:
    print("❌ 文件找不到，请核对路径！")