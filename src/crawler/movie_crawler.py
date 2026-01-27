import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import re


def scrape_all_top250():
    all_movies = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://movie.douban.com/top250'
    }

    for i in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={i}"
        print(f"🚀 正在精准爬取第 {i // 25 + 1} 页...")

        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code != 200:
                continue

            soup = BeautifulSoup(res.text, 'html.parser')
            items = soup.find_all('div', class_='item')

            for item in items:
                try:
                    # 1. 基础字段
                    title = item.find('span', class_='title').get_text()
                    rating = item.find('span', class_='rating_num').get_text()

                    # 2. 详情字段解析 (解决林青霞变国家的问题)
                    info_text = item.find('div', class_='bd').p.get_text(strip=True)
                    # 豆瓣格式: "导演: ... / 主演: ... / 1994 / 美国 / 剧情"
                    parts = [p.strip() for p in info_text.split('/')]

                    # --- 核心修复逻辑：从后往前定位 ---
                    # 倒数第一通常是类型，倒数第二通常是国家，倒数第三通常是年份
                    # 但我们要用正则确保年份的准确性
                    movie_genre = parts[-1] if len(parts) > 0 else "未知"
                    movie_country = parts[-2] if len(parts) > 1 else "未知"

                    # 在整段文本中搜寻 4 位数字作为年份
                    year_search = re.search(r'(\d{4})', info_text)
                    movie_year = year_search.group(1) if year_search else "未知"

                    # 二次清洗国家名：如果抓到了人名（通常很长或包含特殊字符）
                    if "..." in movie_country or len(movie_country) > 10:
                        # 尝试从类型前一个位置重新提取
                        movie_country = movie_country.split(' ')[-1]

                    # 3. 评价人数解析 (解决数字虚高问题)
                    item_text = item.get_text(strip=True)
                    # 仅提取“数字+人评价”这一组合
                    vote_match = re.search(r'(\d+)人评价', item_text)
                    votes = vote_match.group(0) if vote_match else "0人评价"

                    all_movies.append({
                        "电影名称": title,
                        "评分": float(rating),
                        "评价人数": votes,
                        "上映年份": movie_year,
                        "国家": movie_country,
                        "类型": movie_genre
                    })
                except Exception:
                    continue

            time.sleep(1.5)  # 频率控制

        except Exception as e:
            print(f"❌ 分页异常: {e}")

    return all_movies


if __name__ == "__main__":
    results = scrape_all_top250()

    if results:
        df = pd.DataFrame(results)
        # 自动定位项目 data 目录
        output_dir = os.path.join(os.path.dirname(__file__), "../../data")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "douban_top250_full.xlsx")
        df.to_excel(output_path, index=False)

        print("\n" + "=" * 50)
        print(f"✅ 数据洗白成功！")
        print(f"📊 样本检查: {df['电影名称'].iloc[0]} -> {df['国家'].iloc[0]} | {df['上映年份'].iloc[0]}")
        print(f"📂 文件位置: {output_path}")
        print("=" * 50)