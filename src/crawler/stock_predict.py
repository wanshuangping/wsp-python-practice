import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import akshare as ak
import os

# 1. 沿用你之前获取的茅台数据
# 这里假设你的 df 已经包含了最新的 Close 数据
print("🚀 正在获取茅台最新数据进行预测...")
df = ak.stock_zh_a_hist(symbol="600519", period="daily", start_date="20250101", end_date="20260130", adjust="qfq")
df['日期'] = pd.to_datetime(df["日期"])
df = df.rename(columns={"开盘": "Open", "收盘": "Close", "最高": "High", "最低": "Low", "成交量": "Volume"})

# 2. 然后再执行你的预测逻辑
df['Day_Index'] = np.arange(len(df))
df['Day_Index'] = np.arange(len(df)) # 用数字序号作为自变量

# 2. 选取最近 30 天作为训练集
train_days = 30
df_recent = df.tail(train_days)

X = df_recent[['Day_Index']].values
y = df_recent['Close'].values

# 3. 训练线性模型
model = LinearRegression()
model.fit(X, y)

# 4. 预测未来 5 天
future_indices = np.arange(len(df), len(df) + 5).reshape(-1, 1)
future_preds = model.predict(future_indices)

# 5. 可视化
plt.figure(figsize=(12, 6))
# 绘制过去 30 天实际走势
plt.plot(df_recent['日期'], df_recent['Close'], label='过去30天实际股价', color='blue', marker='o')

# 绘制未来 5 天预测线
future_dates = pd.date_range(start=df['日期'].iloc[-1], periods=6)[1:] # 生成未来日期
plt.plot(future_dates, future_preds, label='未来5天趋势预测', color='red', linestyle='--', marker='x')

plt.title('贵州茅台 (600519) 未来 5 天趋势预判 (线性回归)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()