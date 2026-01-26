import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


def scrape_all_top250():
    all_movies = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # 外层循环：控制翻页
    for i in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={i}"
        print(f"🚀 正在爬取第 {i // 25 + 1} 页...")

        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            items = soup.select('div.item')

            # 内层循环：解析电影数据
            for item in items:
                try:
                    title = item.select_one('span.title').get_text()
                    rating = item.select_one('span.rating_num').get_text()

                    # 关键修复：精准定位评价人数
                    star_div = item.select_one('div.star')
                    # 找到 star 下所有 span，评价人数通常是最后一个
                    spans = star_div.find_all('span')
                    votes = "0人评价"
                    for s in spans:
                        text = s.get_text()
                        if "人评价" in text:
                            votes = text
                            break

                    all_movies.append({
                        "电影名称": title,
                        "评分": float(rating),
                        "评价人数": votes
                    })
                except Exception:
                    continue

                    # 礼貌翻页
            time.sleep(1.0)

        except Exception as e:
            print(f"❌ 分页请求失败: {e}")

    return all_movies


if __name__ == "__main__":
    # 1. 运行爬虫
    data_list = scrape_all_top250()

    if data_list:
        # 2. 创建 DataFrame (确保在这里定义 df)
        df = pd.DataFrame(data_list)

        # 3. 确保目录存在并保存
        output_dir = "../../data"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file = os.path.join(output_dir, "douban_top250_full.xlsx")
        df.to_excel(output_file, index=False)
        print(f"\n✅ 成功！数据已保存至: {output_file}")

        # 4. 打印统计信息
        print("-" * 30)
        top_movie = df.loc[df['评分'].idxmax()]
        print(f"🏆 评分最高的电影是: {top_movie['电影名称']}")
        print(f"⭐ 评分: {top_movie['评分']}")
        print(f"👥 {top_movie['评价人数']}")
        print("-" * 30)
    else:
        print("📭 未能获取任何数据，请检查网络。")