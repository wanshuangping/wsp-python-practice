import requests
from lxml import etree  # 使用 lxml 解析 XPath
import pandas as pd
import time
import os


def scrape_douban_xpath():
    all_movies = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://movie.douban.com/top250'
    }

    for i in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={i}"
        print(f"🕵️ XPath 正在定位第 {i // 25 + 1} 页...")

        try:
            res = requests.get(url, headers=headers, timeout=10)
            # 将 HTML 文本转化为 XPath 可识别的树结构
            selector = etree.HTML(res.text)

            # 1. 定位所有的电影条目容器
            items = selector.xpath('//div[@class="item"]')

            for item in items:
                # 2. 在当前 item 下使用相对路径 (.) 提取数据
                # XPath 返回的是列表，所以通常取 [0]
                title = item.xpath('.//span[@class="title"][1]/text()')[0]
                rating = item.xpath('.//span[@class="rating_num"]/text()')[0]

                # 提取评价人数（定位包含“人评价”的 span）
                votes_text = item.xpath('.//div[@class="star"]/span[last()]/text()')[0]

                # 提取描述信息（年份、国家等所在的 p 标签文本）
                # XPath 的 normalize-space 可以清理多余空格
                info = item.xpath('.//div[@class="bd"]/p[1]/text()')
                # 豆瓣的 info 通常分成两部分：导演/主演 和 年份/国家/类型
                # 我们取第二部分（通常是 info[1]）
                full_info = "".join([i.strip() for i in info])

                all_movies.append({
                    "电影名称": title,
                    "评分": rating,
                    "评价人数": votes_text,
                    "详情": full_info
                })

            time.sleep(1.2)

        except Exception as e:
            print(f"❌ 解析失败: {e}")

    return all_movies


if __name__ == "__main__":
    # 运行前请确保安装了 lxml: pip install lxml
    data = scrape_douban_xpath()
    if data:
        df = pd.DataFrame(data)
        print("\n" + "X" * 30)
        print(f"✅ XPath 抓取完成，共 {len(df)} 部！")
        print(df.head(3))
        print("X" * 30)