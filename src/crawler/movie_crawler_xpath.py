import requests
from lxml import etree
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
        print(f"🕵️ XPath 正在安全定位第 {i // 25 + 1} 页...")

        try:
            res = requests.get(url, headers=headers, timeout=10)
            selector = etree.HTML(res.text)
            items = selector.xpath('//div[@class="item"]')

            for item in items:
                try:
                    # 使用安全提取方法：先取列表，再判断是否为空
                    def get_first(xpath_res):
                        return xpath_res[0].strip() if xpath_res else "未知"

                    # 提取标题
                    title = get_first(item.xpath('.//span[@class="title"][1]/text()'))

                    # 提取评分
                    rating = get_first(item.xpath('.//span[@class="rating_num"]/text()'))

                    # 提取评价人数 (定位包含数字的那个 span)
                    votes_list = item.xpath('.//div[@class="star"]/span[last()]/text()')
                    votes = get_first(votes_list)

                    # 提取详情文本 (年份/国家/类型)
                    # normalize-space 可以一次性清理所有换行和空格
                    info_raw = item.xpath('normalize-space(.//div[@class="bd"]/p[1])')

                    all_movies.append({
                        "电影名称": title,
                        "评分": rating,
                        "评价人数": votes,
                        "详情": info_raw
                    })
                except Exception as e:
                    # 单条电影解析失败，跳过，不影响全局
                    continue

            time.sleep(1.2)

        except Exception as e:
            print(f"❌ 页面请求失败: {e}")

    return all_movies


if __name__ == "__main__":
    data = scrape_douban_xpath()
    if data:
        df = pd.DataFrame(data)
        # 自动保存到 data 文件夹
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(current_dir, "../../data/douban_xpath_result.xlsx")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        df.to_excel(output_path, index=False)

        print("\n" + "✅" * 15)
        print(f"XPath 抓取圆满完成！共 {len(df)} 部记录。")
        print(f"文件已保存至: {output_path}")
        print("✅" * 15)