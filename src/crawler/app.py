import streamlit as st
import akshare as ak
import pandas as pd
import mplfinance as mpf

st.title("🚀 个人 AI 股票投资决策仪表盘")

# 侧边栏配置
stock_code = st.sidebar.text_input("输入股票代码", value="600519")
days = st.sidebar.slider("选择查看天数", 30, 365, 100)


# 获取数据
@st.cache_data  # 缓存数据，避免重复请求被封 IP
def get_data(code):
    df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq")
    return df


try:
    df = get_data(stock_code).tail(days)
    df.index = pd.to_datetime(df["日期"])
    df = df.rename(columns={"开盘": "Open", "收盘": "Close", "最高": "High", "最低": "Low", "成交量": "Volume"})

    # 展示 K 线图
    st.subheader(f"{stock_code} 最近 {days} 天走势")
    fig, ax = mpf.plot(df, type='candle', style='charles', volume=True, returnfig=True)
    st.pyplot(fig)

    # 简易策略提示
    ma5 = df['Close'].rolling(5).mean().iloc[-1]
    ma20 = df['Close'].rolling(20).mean().iloc[-1]

    if ma5 > ma20:
        st.success("✅ 策略信号：多头趋势 (金叉)")
    else:
        st.error("⚠️ 策略信号：空头趋势 (死叉)")

except Exception as e:
    st.write("请输入正确的股票代码或检查网络。")

# 在 app.py 的原有逻辑下方添加
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

st.divider() # 加一条分割线
# 在 app.py 底部 st.divider() 之后填充
if st.button("开始 AI 深度预测"):
    with st.spinner('AI 正在全力建模中...'):
        # 1. 数据准备
        data_pred = df['Close'].values.reshape(-1, 1)
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data_pred)

        # 2. 构造训练集 (简易版以提升速度)
        prediction_days = 30
        x_train, y_train = [], []
        for x in range(prediction_days, len(scaled_data)):
            x_train.append(scaled_data[x - prediction_days:x, 0])
            y_train.append(scaled_data[x, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # 3. 快速建立模型
        model = Sequential([
            LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)),
            LSTM(units=50),
            Dense(units=1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(x_train, y_train, epochs=5, batch_size=16, verbose=0)  # epoch减小保证网页不卡死

        # 4. 滚动预测未来 5 天
        current_batch = scaled_data[-prediction_days:].reshape(1, prediction_days, 1)
        future_predictions = []
        for i in range(5):
            next_pred = model.predict(current_batch)[0]
            future_predictions.append(next_pred)
            current_batch = np.append(current_batch[:, 1:, :], next_pred.reshape(1, 1, 1), axis=1)

        future_actual = scaler.inverse_transform(future_predictions)

        # 5. 使用 Streamlit 原生图表展示结果
        st.info("📊 预测完成！红色线条即为未来 5 天预估趋势。")
        pred_df = pd.DataFrame(future_actual, columns=['预测价格'])
        st.line_chart(pred_df)
st.subheader("🤖 AI 未来 5 天趋势预测 (LSTM)")
# 建议的修改片段
st.divider()
st.subheader("🎯 AI 未来 5 天趋势预测 (LSTM)")

# 为按钮增加 unique_key 确保不报错
if st.button("开始 AI 深度预测", key="final_predict_btn"):
    with st.spinner('AI 正在全力计算中...'):
        # ... 这里运行你的 LSTM 计算逻辑 ...

        # 最后的关键：用原生图表显示预测
        st.success("✅ AI 计算完成，这是它对未来的推演：")
        st.line_chart(pd.DataFrame(future_actual, columns=['AI 预估价格']))

# 给按钮加一个独特的 key 避免报错
if st.button("开始 AI 深度预测", key="predict_btn"):
    with st.spinner('AI 正在全力建模中...'):
        # ... 这里是你之前的 LSTM 训练代码 ...

        # 核心：必须把预测结果变成 DataFrame 才能在网页显示
        # 假设你的预测结果是 future_actual
        pred_df = pd.DataFrame(future_actual, columns=['AI 预测价'])

        st.success("✅ 预测完成！")
        # 这一行会自动在网页上画出折线图
        st.line_chart(pred_df)

if st.button("开始 AI 深度预测"):
    with st.spinner('AI 正在全力建模中...'):
        # 1. 提取 Close 数据并预处理
        data = df['Close'].values.reshape(-1, 1)
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data)

        # 2. 简单的快速训练逻辑 (为了演示效率，减少 epoch)
        # 实际生产中建议加载预训练好的模型文件
        # ... (这里放入你之前的 LSTM 训练与滚动预测代码) ...

        # 3. 展示结果
        st.info("预测结果已生成！红色虚线代表 AI 预判走势。")
        # 使用 st.line_chart 或 st.pyplot 画出你的预测图