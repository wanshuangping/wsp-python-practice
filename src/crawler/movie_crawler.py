import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


def scrape_all_top250():
    all_movies = []
    # 模拟真实浏览器，增加更多 Header 字段
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://movie.douban.com/'
    }

    for i in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={i}"
        print(f"🚀 正在爬取第 {i // 25 + 1} 页...")

        try:
            # 增加随机延时，模仿人类行为
            res = requests.get(url, headers=headers, timeout=15)

            # 检查是否被封或出现验证码
            if res.status_code != 200:
                print(f"❌ 请求失败，状态码: {res.status_code}。可能是触发了防爬。")
                continue

            soup = BeautifulSoup(res.text, 'html.parser')
            # 豆瓣 Top 250 的核心列表项通常在 ol.grid_view > li
            items = soup.find_all('div', class_='item')

            if not items:
                print(f"⚠️ 第 {i // 25 + 1} 页未解析到电影项，请检查网页结构！")
                continue

            for item in items:
                try:
                    # 1. 标题 (找第一个 title)
                    title = item.find('span', class_='title').get_text()

                    # 2. 评分
                    rating = item.find('span', class_='rating_num').get_text()

                    # 3. 评价人数 (核心修复：遍历所有 span 找到包含“人评价”的)
                    star_div = item.find('div', class_='star')
                    votes = "0人评价"
                    if star_div:
                        spans = star_div.find_all('span')
                        for s in spans:
                            if "人评价" in s.get_text():
                                votes = s.get_text()
                                break

                    all_movies.append({
                        "电影名称": title,
                        "评分": float(rating),
                        "评价人数": votes
                    })
                except Exception as e:
                    continue

            print(f"✅ 第 {i // 25 + 1} 页解析完成，当前已抓取 {len(all_movies)} 条。")
            time.sleep(2.0)  # 稍微慢一点，更安全

        except Exception as e:
            print(f"❌ 分页请求发生严重错误: {e}")

    return all_movies


if __name__ == "__main__":
    results = scrape_all_top250()

    if results:
        df = pd.DataFrame(results)
        # 确保 data 目录存在
        os.makedirs("../../data", exist_ok=True)
        output_path = "../../data/douban_top250_full.xlsx"
        df.to_excel(output_path, index=False)

        print("\n" + "=" * 40)
        print(f"🎉 大功告成！总共抓取了 {len(df)} 部电影")
        top_movie = df.loc[df['评分'].idxmax()]
        print(f"🏆 本榜单评分最高: {top_movie['电影名称']} ({top_movie['评分']}分)")
        print(f"📊 数据已保存: {os.path.abspath(output_path)}")
        print("=" * 40)
    else:
        print("\n😱 依然没有抓到数据！请检查你的网络是否需要梯子，或者在浏览器打开豆瓣看看是否需要登录验证。")