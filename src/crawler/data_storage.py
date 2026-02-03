import sqlite3
import pandas as pd
import akshare as ak


def init_db():
    # 连接（或创建）本地数据库文件
    conn = sqlite3.connect('stock_data.db')
    return conn


def update_stock_data(stock_code="600519"):
    conn = init_db()

    # 1. 抓取最新数据
    df_new = ak.stock_zh_a_hist(symbol=stock_code, period="daily", adjust="qfq")

    # 2. 自动化存入数据库 (如果表不存在则创建，存在则替换)
    # 这样你的数据就从内存“落袋为安”到了硬盘
    df_new.to_sql(f'stock_{stock_code}', conn, if_exists='replace', index=False)

    print(f"✅ 股票 {stock_code} 数据已自动同步至本地数据库")
    conn.close()


# 运行一次进行初始化
if __name__ == "__main__":
    update_stock_data()