import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import re


def scrape_all_top250():
    all_movies = []
    # 模拟真实浏览器请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://movie.douban.com/top250'
    }

    for i in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={i}"
        print(f"🚀 正在爬取第 {i // 25 + 1} 页...")

        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code != 200:
                print(f"❌ 第 {i // 25 + 1} 页请求失败，状态码: {res.status_code}")
                continue

            soup = BeautifulSoup(res.text, 'html.parser')
            items = soup.find_all('div', class_='item')

            for item in items:
                try:
                    # 1. 提取基础信息：标题与评分
                    title = item.find('span', class_='title').get_text()
                    rating = item.find('span', class_='rating_num').get_text()

                    # 2. 深度挖掘维度：年份、国家、类型
                    info_text = item.find('div', class_='bd').p.get_text(strip=True)
                    # 处理 info_text，如 "1994 / 美国 / 剧情"
                    parts = [p.strip() for p in info_text.split('/')]

                    # 提取年份（正则匹配 4 位数字）
                    year_match = re.search(r'(\d{4})', parts[0])
                    movie_year = year_match.group(1) if year_match else "未知"

                    # 提取国家和类型
                    movie_country = parts[1] if len(parts) > 1 else "未知"
                    movie_genre = parts[2] if len(parts) > 2 else "未知"

                    # 3. 评价人数提取 (暴力正则方案，确保非0)
                    item_full_text = item.get_text(strip=True)
                    vote_match = re.search(r'(\d+)人评价', item_full_text)
                    votes = vote_match.group(0) if vote_match else "0人评价"

                    # 4. 存入列表
                    all_movies.append({
                        "电影名称": title,
                        "评分": float(rating),
                        "评价人数": votes,
                        "上映年份": movie_year,
                        "国家": movie_country,
                        "类型": movie_genre
                    })
                except Exception as e:
                    print(f"⚠️ 解析某条数据时跳过: {e}")
                    continue

            # 礼貌延时，防止封禁
            time.sleep(1.5)

        except Exception as e:
            print(f"❌ 分页请求异常: {e}")

    return all_movies


if __name__ == "__main__":
    # 执行函数
    data_list = scrape_all_top250()

    # 逻辑判断：确保 data_list 存在且不为空
    if data_list:
        df = pd.DataFrame(data_list)

        # 确保数据保存目录存在
        output_dir = "../../data"
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "douban_top250_full.xlsx")
        df.to_excel(output_path, index=False)

        print("\n" + "=" * 50)
        print(f"✅ 全链路修复成功！总计抓取: {len(df)} 部电影")

        # 统计验证
        top_movie = df.loc[df['评分'].idxmax()]
        print(f"🏆 评分最高: {top_movie['电影名称']} ({top_movie['评分']}分)")
        print(f"📅 上映年份: {top_movie['上映年份']}")
        print(f"👥 评价规模: {top_movie['评价人数']}")
        print(f"📂 数据已保存至: {os.path.abspath(output_path)}")
        print("=" * 50)
    else:
        print("\n😱 抓取结果为空！请检查网络或是否需要登录豆瓣验证。")