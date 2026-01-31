import numpy as np
import pandas as pd
import akshare as ak
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# 1. 获取茅台数据并预处理
df = ak.stock_zh_a_hist(symbol="600519", period="daily", start_date="20230101", end_date="20260130", adjust="qfq")
data = df['收盘'].values.reshape(-1, 1)

# 2. 归一化 (LSTM 对数值敏感)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# 3. 制作滑动窗口数据集 (用过去 60 天的数据预测第 61 天)
prediction_days = 60
x_train, y_train = [], []
for x in range(prediction_days, len(scaled_data)):
    x_train.append(scaled_data[x-prediction_days:x, 0])
    y_train.append(scaled_data[x, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# 4. 构建 LSTM 模型
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(units=50))
model.add(Dense(units=1)) # 输出明天的预测股价

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, epochs=25, batch_size=32) # 训练 25 轮

# 5. 预测未来走势
# (此处省略复杂的未来 5 天滚动预测逻辑，重点看模型训练是否跑通)
print("✅ LSTM 模型训练完成！")