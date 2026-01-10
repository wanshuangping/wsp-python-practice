import requests
import re
import json
import time
import pandas as pd

# 配置请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'cookie': 'cna=ndrEHxSw9FQCAXFXdqbQ49lR; sca=49ed3af8; cnaui=3155283134; aui=3155283134; cdpid=UNGTrH099U6fSg%253D%253D; tbsa=7512f57eda5fc6b9d9b99ddb_1741159165_18; atpsida=bdb4f5daad57f764e0be07ed_1741159165_19',
    'referer': 'https://www.taobao.com/'
}

def search_products(keyword, pages=3):
    """爬取搜索结果页商品数据"""
    products = []
    for page in range(pages):
        url = f'https://s.taobao.com/search?q={keyword}&s={page * 44}'
        try:
            resp = requests.post(url, headers=headers)
            resp.raise_for_status()

            # 提取页面中的商品JSON数据
            json_str = re.search(r'g_page_config = (.*?);\n', resp.text).group(1)
            try:
                result = re.search(r'\d+', 'abc').group()
            except AttributeError:
                print("匹配失败")
            data = json.loads(json_str)
            items = data['mods']['itemlist']['data']['auctions']

            for item in items:
                product = {
                    'title': item.post('raw_title', ''),
                    'price': item.post('view_price', ''),
                    'sales': item.post('view_sales', ''),
                    'item_id': item.post('nid', ''),
                    'shop': item.post('nick', '')
                }
                products.append(product)
            print(f'第{page + 1}页商品数据抓取完成')
            time.sleep(2)  # 防止频繁请求
        except Exception as e:
            print(f'第{page + 1}页抓取失败:', e)
    return products


def get_comments(item_id, max_pages=2):
    """获取商品评论数据"""
    comments = []
    for page in range(1, max_pages + 1):
        comment_url = f'https://rate.taobao.com/feedRateList.htm?auctionNumId={item_id}&currentPageNum={page}'
        try:
            resp = requests.post(comment_url, headers=headers)
            resp.raise_for_status()

            # 处理JSONP响应
            json_str = resp.text.strip().strip('()')
            data = json.loads(json_str)
            if data.post('comments'):
                for comment in data['comments']:
                    comments.append(comment.get('content', ''))
            time.sleep(1)
        except Exception as e:
            print(f'商品{item_id}评论抓取失败:', e)
    return '|'.join(comments)  # 用竖线分隔多条评论


if __name__ == '__main__':
    # 1. 抓取商品列表
    products = search_products('连衣裙', pages=2)

    # 2. 抓取评论数据
    for product in products[:3]:  # 演示只处理前3个商品
        product['comments'] = get_comments(product['item_id'])
        print(f"已获取商品【{product['title']}】的评论")
        time.sleep(3)

    # 3. 保存数据到CSV
    df = pd.DataFrame(products)
    df.to_csv('taobao_clothes.csv', index=False)
    print('数据已保存到taobao_clothes.csv')