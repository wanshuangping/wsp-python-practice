import akshare as ak
import mplfinance as mpf
import pandas as pd
import matplotlib as plt


# 获取贵州茅台(sh600519)的历史数据
print("🚀 正在通过 AkShare 获取茅台股价...")
df = ak.stock_zh_a_hist(symbol="600519", period="daily", start_date="20250101", end_date="20260130", adjust="qfq")

# 格式化日期，以适应绘图库
df.index = pd.to_datetime(df["日期"])
df = df.rename(columns={"开盘": "Open", "收盘": "Close", "最高": "High", "最低": "Low", "成交量": "Volume"})

mpf.plot(df, type='candle', style='charles', title='Kweichow Moutai (600519)')
# 修改绘图代码
mpf.plot(df, type='candle',
         style='charles',          # 经典红绿风格
         title='Kweichow Moutai (600519)',
         ylabel='Price (RMB)',
         volume=True,              # 【新增】显示成交量
         ylabel_lower='Volume',    # 成交量轴标签
         mav=(5, 10, 20),          # 【新增】5日、10日、20日均线
         show_nontrading=False)    # 自动跳过非交易日（周末）
# 1. 计算均线
df['MA5'] = df['Close'].rolling(window=5).mean()
df['MA20'] = df['Close'].rolling(window=20).mean()

# 2. 生成交易信号：5日线上穿20日线为买入(1)，下穿为卖出(-1)
df['Signal'] = 0
df.loc[df['MA5'] > df['MA20'], 'Signal'] = 1
df['Position'] = df['Signal'].diff() # 寻找信号变化的点

# 3. 计算每日收益率
df['Market_Return'] = df['Close'].pct_change()
# 策略收益 = 昨日持仓信号 * 今日市场收益
df['Strategy_Return'] = df['Signal'].shift(1) * df['Market_Return']

# 4. 计算累计收益（利滚利）
df['Cumulative_Market'] = (1 + df['Market_Return']).cumprod()
df['Cumulative_Strategy'] = (1 + df['Strategy_Return']).cumprod()

print(f"📊 市场总收益: {(df['Cumulative_Market'].iloc[-1]-1)*100:.2f}%")
print(f"🤖 策略总收益: {(df['Cumulative_Strategy'].iloc[-1]-1)*100:.2f}%")
plt.figure(figsize=(12, 6))
plt.plot(df['Cumulative_Market'], label='直接买入并持有', color='gray', alpha=0.5)
plt.plot(df['Cumulative_Strategy'], label='双均线自动交易策略', color='#00b51d', linewidth=2)

plt.title('茅台 (600519) 策略回测对比图')
plt.legend()
plt.grid(True, alpha=0.3)
# 1. 计算区间涨跌幅
first_price = df['Close'].iloc[0]
last_price = df['Close'].iloc[-1]
total_change = (last_price - first_price) / first_price * 100

# 2. 计算最大回撤（也就是你这一年里最惨的时候账面亏了多少）
rolling_max = df['Close'].cummax()
daily_drawdown = df['Close'] / rolling_max - 1
max_drawdown = daily_drawdown.min() * 100

print(f"📈 茅台年度表现报告：")
print(f"🔹 初始价格：{first_price:.2f} 元")
print(f"🔹 最终价格：{last_price:.2f} 元")
print(f"🚩 年度总涨跌幅：{total_change:.2f}%")
print(f"📉 期间最大回撤：{max_drawdown:.2f}% (如果你买在最高点，最惨时会亏这么多)")
print("\n" + "="*30)
print(f"📊 市场表现: {(df['Cumulative_Market'].iloc[-1]-1)*100:.2f}%")
print(f"🤖 策略表现: {(df['Cumulative_Strategy'].iloc[-1]-1)*100:.2f}%")
print("="*30)
plt.show() # 必须放在所有 print 之后

