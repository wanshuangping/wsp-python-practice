import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


def scrape_douban_css():
    all_movies = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://movie.douban.com/top250'
    }

    for i in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={i}"
        print(f"🎨 CSS 选择器正在点名第 {i // 25 + 1} 页...")

        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')

            # 1. 直接选取所有电影容器 (类名为 item 的 div)
            items = soup.select('div.item')

            for item in items:
                # 2. 精准点名：.class_name 提取内容
                # select_one 确保只取第一个匹配项
                title = item.select_one('.hd .title').get_text()
                rating = item.select_one('.rating_num').get_text()

                # 提取评价人数：利用 CSS 的伪类选择器 last-child
                votes = item.select_one('.star span:last-child').get_text()

                # 提取描述信息：第一个 p 标签
                info = item.select_one('.bd p').get_text(strip=True)

                all_movies.append({
                    "电影名称": title,
                    "评分": rating,
                    "评价人数": votes,
                    "描述": info
                })

            time.sleep(1.2)

        except Exception as e:
            print(f"❌ 某处点名出错: {e}")

    return all_movies


if __name__ == "__main__":
    data = scrape_douban_css()
    if data:
        df = pd.DataFrame(data)
        # 结果保存
        output_path = os.path.join(os.path.dirname(__file__), "../../data/douban_css_result.xlsx")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_excel(output_path, index=False)

        print(f"\n✨ CSS 抓取大功告成！总计 {len(df)} 部电影已存入 Excel。")