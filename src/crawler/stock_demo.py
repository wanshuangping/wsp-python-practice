import akshare as ak
import mplfinance as mpf
import pandas as pd


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