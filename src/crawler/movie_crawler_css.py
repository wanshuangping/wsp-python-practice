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
            items = soup.select('div.item')

            for item in items:
                # --- 核心：安全提取函数 ---
                def safe_get(selector, attr='text'):
                    element = item.select_one(selector)
                    if element:
                        return element.get_text(strip=True) if attr == 'text' else element.get(attr)
                    return "未知"

                # 使用安全点名提取
                title = safe_get('.hd .title')
                rating = safe_get('.rating_num')
                # 评价人数通常是最后一个 span
                votes = safe_get('.star span:last-child')
                # 详情描述
                info = safe_get('.bd p')

                all_movies.append({
                    "电影名称": title,
                    "评分": rating,
                    "评价人数": votes,
                    "描述": info
                })

            time.sleep(1.2)

        except Exception as e:
            print(f"❌ 页面抓取失败: {e}")

    return all_movies


if __name__ == "__main__":
    data = scrape_douban_css()
    if data:
        df = pd.DataFrame(data)
        # 自动保存
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(current_dir, "../../data/douban_css_clean.xlsx")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_excel(output_path, index=False)

        print("\n" + "✨" * 15)
        print(f"CSS 方案也完美通关！共记录 {len(df)} 部。")
        print(f"结果已存至: {output_path}")
        print("✨" * 15)