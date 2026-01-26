import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


def scrape_all_top250():
    all_movies = []
    # 更加真实的浏览器请求头，防止被豆瓣拦截
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://movie.douban.com/top250'
    }

    # 外层循环：控制翻页 (从0到225，步长25，共10页)
    for i in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={i}"
        print(f"🚀 正在爬取第 {i // 25 + 1} 页: {url}")

        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code != 200:
                print(f"❌ 第 {i // 25 + 1} 页请求失败，状态码: {res.status_code}")
                continue

            soup = BeautifulSoup(res.text, 'html.parser')
            items = soup.find_all('div', class_='item')

            # 内层循环：解析每一部电影
            for item in items:
                try:
                    # 1. 提取标题
                    title = item.find('span', class_='title').get_text()

                    # 2. 提取评分
                    rating = item.find('span', class_='rating_num').get_text()

                    # 3. 核心修复：精准提取评价人数
                    # 逻辑：遍历 star 区域下的所有 span，找到包含“人评价”的文本
                    star_div = item.find('div', class_='star')
                    votes = "0人评价"  # 默认值
                    if star_div:
                        spans = star_div.find_all('span')
                        for s in spans:
                            content = s.get_text()
                            if "人评价" in content:
                                votes = content
                                break

                    all_movies.append({
                        "电影名称": title,
                        "评分": float(rating),
                        "评价人数": votes
                    })
                except Exception as e:
                    print(f"⚠️ 解析单条电影数据出错，已跳过: {e}")
                    continue

            # 每一页爬完后休息 1.5 秒，避免封 IP
            time.sleep(1.5)

        except Exception as e:
            print(f"❌ 网络请求发生异常: {e}")

    # return 必须在 for 循环完全结束后执行，且缩进与第一个 for 对齐
    return all_movies


if __name__ == "__main__":
    # 1. 执行爬取函数
    data_list = scrape_all_top250()

    # 2. 判断是否有结果返回，修复 NameError
    if data_list and len(data_list) > 0:
        # 定义 df 对象
        df = pd.DataFrame(data_list)

        # 3. 确保 data 目录存在并保存
        output_dir = "../../data"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file = os.path.join(output_dir, "douban_top250_full.xlsx")
        df.to_excel(output_file, index=False)

        print("\n" + "=" * 50)
        print(f"✨ 抓取圆满成功！")
        print(f"📈 总计电影数量: {len(df)} 部")

        # 4. 执行简单统计（确保此时 df 已定义）
        top_movie = df.loc[df['评分'].idxmax()]
        print(f"🏆 评分最高: {top_movie['电影名称']} ({top_movie['评分']}分)")
        print(f"👥 评价规模: {top_movie['评价人数']}")
        print(f"📂 文件保存至: {os.path.abspath(output_file)}")
        print("=" * 50)
    else:
        print("\n😱 抓取结果为空！请检查：")
        print("1. 你的网络是否能正常访问豆瓣 (不用梯子)？")
        print("2. 在浏览器打开豆瓣，看是否出现了滑动验证码？")