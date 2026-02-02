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