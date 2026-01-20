import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def scrape_douban_top250():
    # 1. 模拟浏览器请求头 (没有这个会被豆瓣拦截)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    movie_list = []

    # 我们先尝试抓取第一页 (前 25 部)
    url = "https://movie.douban.com/top250"

    try:
        print(f"🚀 正在请求: {url}")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # 2. 解析网页源码
            soup = BeautifulSoup(response.text, 'html.parser')

            # 找到所有的电影条目 (豆瓣的电影条目都在 <div class="item"> 里)
            items = soup.find_all('div', class_='item')

            for item in items:
                # 提取标题
                title = item.find('span', class_='title').get_text()
                # 提取评分
                rating = item.find('span', class_='rating_num').get_text()
                # 提取评价人数
                quote = item.find('span', class_='inq')
                quote_text = quote.get_text() if quote else "暂无评语"

                movie_list.append({
                    "电影名称": title,
                    "评分": rating,
                    "金句": quote_text
                })

            return movie_list
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            return []

    except Exception as e:
        print(f"⚠️ 发生错误: {e}")
        return []


if __name__ == "__main__":
    results = scrape_douban_top250()

    # 3. 展示结果并保存
    if results:
        df = pd.DataFrame(results)
        print("\n✅ 抓取成功！预览前 5 条数据：")
        print(df.head())

        # 保存为 Excel (需要 openpyxl 库)
        output_path = "../../data/douban_movies.xlsx"
        df.to_excel(output_path, index=False)
        print(f"\n文件已保存至: {output_path}")