import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


def scrape_douban_css_final():
    all_movies = []
    # 1. 准备图片存放目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(current_dir, "../../data/posters")
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://movie.douban.com/top250'
    }

    for i in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={i}"
        print(f"🎨 CSS 选择器正在安全采集第 {i // 25 + 1} 页...")

        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            items = soup.select('div.item')  # 定位电影条目容器

            for item in items:
                # --- 核心修复：安全提取函数 ---
                # 检查元素是否存在，避免 NoneType 报错
                def safe_select(css_selector, attribute='text'):
                    target = item.select_one(css_selector)
                    if target:
                        if attribute == 'text':
                            return target.get_text(strip=True)
                        return target.get(attribute)
                    return "未知"

                # 2. 提取数据
                title = safe_select('.hd .title')  # 提取电影名称
                rating = safe_select('.rating_num')  # 提取评分
                votes = safe_select('.star span:last-child')  # 提取评价人数
                img_url = safe_select('.pic img', attribute='src')  # 提取封面链接

                # 3. 实时下载海报 (可选功能)
                if img_url != "未知":
                    try:
                        img_data = requests.get(img_url).content
                        # 过滤文件名中的非法字符
                        clean_title = title.replace("/", " ").strip()
                        with open(f"{img_dir}/{clean_title}.jpg", "wb") as f:
                            f.write(img_data)
                    except:
                        pass  # 图片下载失败不影响程序运行

                all_movies.append({
                    "电影名称": title,
                    "评分": rating,
                    "评价人数": votes,
                    "海报路径": f"data/posters/{title}.jpg"
                })

            time.sleep(1.2)  # 频率控制，防止被封

        except Exception as e:
            print(f"❌ 页面抓取异常: {e}")

    return all_movies


if __name__ == "__main__":
    data = scrape_douban_css_final()
    if data:
        df = pd.DataFrame(data)
        output_path = os.path.join(os.path.dirname(__file__), "../../data/douban_css_final.xlsx")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_excel(output_path, index=False)

        print("\n" + "✨" * 15)
        print(f"CSS 方案修复成功！已抓取 {len(df)} 部记录。")
        print(f"图片已存至: data/posters/")
        print("✨" * 15)