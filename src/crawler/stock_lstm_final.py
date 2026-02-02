import numpy as np
import pandas as pd
import akshare as ak
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# 1. 数据准备 (增加数据量以提升 LSTM 学习效果)
df = ak.stock_zh_a_hist(symbol="600519", period="daily", start_date="20230101", end_date="20260130", adjust="qfq")
data = df['收盘'].values.reshape(-1, 1)

# 2. 归一化
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# 3. 构造训练集 (使用过去 60 天预测第 61 天)
prediction_days = 60
x_train, y_train = [], []
for x in range(prediction_days, len(scaled_data)):
    x_train.append(scaled_data[x-prediction_days:x, 0])
    y_train.append(scaled_data[x, 0])
x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# 4. 构建更加稳健的 LSTM 模型
model = Sequential([
    LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)),
    Dropout(0.2), # 防止过拟合
    LSTM(units=50),
    Dropout(0.2),
    Dense(units=1)
])
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, epochs=20, batch_size=32, verbose=1)

# 5. 核心：滚动预测未来 5 天
current_batch = scaled_data[-prediction_days:].reshape(1, prediction_days, 1)
future_predictions = []

for i in range(5):
    # 预测下一天
    next_pred = model.predict(current_batch)[0]
    future_predictions.append(next_pred)
    # 更新输入：剔除最早的一天，加入最新的预测值
    next_pred_reshaped = next_pred.reshape(1, 1, 1)
    current_batch = np.append(current_batch[:, 1:, :], next_pred_reshaped, axis=1)

# 6. 逆归一化还原股价
future_preds_actual = scaler.inverse_transform(future_predictions)

# 7. 可视化
last_days = 30
actual_prices = data[-last_days:]
plt.figure(figsize=(12, 6))
plt.plot(range(last_days), actual_prices, label='实际历史股价 (最近30天)', color='blue', marker='o')

# 对接未来 5 天的 X 轴坐标
plt.plot(range(last_days, last_days + 5), future_preds_actual, label='LSTM 智能预测', color='red', linestyle='--', marker='x')
plt.title('贵州茅台 (600519) LSTM 深度学习趋势预测')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()