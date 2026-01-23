import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def scrape_all_top250():
    all_movies = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'}

    for i in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={i}"
        print(f"🚀 正在爬取第 {i // 25 + 1} 页...")

        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            # 这里的 item 是每部电影的大盒子
            items = soup.select('div.item')

            for item in items:
                # 在 movie_crawler.py 的循环解析部分，替换掉关于 votes 的抓取逻辑
                try:
                    # 更加精准的定位：找到 star 盒子下的所有 span
                    star_div = item.select_one('div.star')
                    all_spans = star_div.find_all('span')

                    # 豆瓣的规律：最后一个 span 通常是 "xxxx人评价"
                    if all_spans:
                        votes_text = all_spans[-1].get_text()
                        # 验证一下是不是真的包含“评价”两个字
                        if "评价" in votes_text:
                            votes = votes_text
                        else:
                            votes = "0人评价"
                    else:
                        votes = "0人评价"
                except Exception:
                    continue  # 如果这一条实在解析不了，跳过看下一条

            time.sleep(1.0)  # 别忘了休息

        except Exception as e:
            print(f"❌ 网络请求异常: {e}")

    return all_movies


if __name__ == "__main__":
    # 执行抓取
    results = scrape_all_top250()

    if results:
        df = pd.DataFrame(results)

        # 1. 计算并打印平均分
        avg_score = df['评分'].mean()
        print(f"\n📊 统计完成！共抓取 {len(df)} 部电影")
        print(f"🌟 Top 250 的平均评分是: {avg_score:.2f}")

        # 2. 保存到 data 文件夹
        # 使用绝对路径确保不会存错位置
        import os

        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output_file = os.path.join(base_path, "data", "douban_top250_full.xlsx")

        df.to_excel(output_file, index=False)
        print(f"✅ 完整数据已保存至: {output_file}")
    else:
        print("📭 未抓取到任何数据，请检查网络或 User-Agent。")

# 找出评分最高的电影
best_movie = df.loc[df['评分'].idxmax()]
print(f"🏆 评分最高的电影是: {best_movie['电影名称']} ({best_movie['评分']}分)")

# 看看平均分
print(f"📈 250部电影的平均分是: {df['评分'].mean():.2f}")