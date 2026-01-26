import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import re


def scrape_all_top250():
    all_movies = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }

    for i in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={i}"
        print(f"🚀 正在爬取第 {i // 25 + 1} 页...")

        try:
            res = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')
            items = soup.find_all('div', class_='item')

            for item in items:
                try:
                    title = item.find('span', class_='title').get_text()
                    rating = item.find('span', class_='rating_num').get_text()

                    # --- ⚡ 暴力解析评价人数 (新逻辑) ---
                    # 直接获取整个 item 的文本，用正则表达式匹配 "数字 + 人评价"
                    item_text = item.get_text(strip=True)
                    # 匹配类似 "123456人评价" 的内容
                    vote_match = re.search(r'(\d+)人评价', item_text)

                    if vote_match:
                        votes = vote_match.group(0)  # 结果如 "1673082人评价"
                    else:
                        # 备选方案：如果正则没抓到，尝试找特定的 div
                        star_info = item.find('div', class_='star')
                        votes = star_info.find_all('span')[-1].get_text() if star_info else "0人评价"

                    all_movies.append({
                        "电影名称": title,
                        "评分": float(rating),
                        "评价人数": votes
                    })
                except Exception:
                    continue

            time.sleep(1.5)

        except Exception as e:
            print(f"❌ 请求异常: {e}")

    return all_movies


if __name__ == "__main__":
    results = scrape_all_top250()
    if results:
        df = pd.DataFrame(results)
        # 确保目录存在
        os.makedirs("../../data", exist_ok=True)
        output_path = "../../data/douban_top250_full.xlsx"
        df.to_excel(output_path, index=False)

        print("\n" + "=" * 50)
        print(f"✅ 数据抓取完成！前 3 条数据如下：")
        print(df[['电影名称', '评价人数']].head(3))
        print("=" * 50)
    else:
        print("😱 依然没抓到数据，请检查网络！")