import requests
import json
from bs4 import BeautifulSoup


def get(path):
    # 目標網址
    url = 'https://www.thenewslens.com/latest-article'

    # 使用 requests 取得網頁內容
    response = requests.get(url)

    # 檢查請求是否成功
    if response.status_code == 200:
        html_content = response.text

        # 解析 HTML 內容
        soup = BeautifulSoup(html_content, 'html.parser')

        # 找到所有 application/ld+json 的 <script> 標籤
        ld_json_scripts = soup.find_all('script', type='application/ld+json')

        # 新的清單，僅保留 itemListElement
        extracted_news = []

        # 遍歷每個 ld_json_scripts，提取所需的資料
        for script in ld_json_scripts:
            try:
                # 解析 JSON 數據
                news_data = json.loads(script.string)

                # 檢查是否存在 mainEntity 和 itemListElement
                if 'mainEntity' in news_data and 'itemListElement' in news_data['mainEntity']:
                    # 取得 itemListElement
                    item_list = news_data['mainEntity']['itemListElement']

                    # 過濾，只保留 name, url
                    for item in item_list:
                        # 檢查 author 中是否有 "精選書摘"
                        if 'author' in item and item['author'] and item['author'][0].get('name') == '精選書摘':
                            continue  # 跳過這個 item

                        # 保留所需字段
                        filtered_item = {
                            'name': item.get('name'),
                            'url': item.get('url'),
                            'text': '',  # 預留位置儲存內容
                        }
                        extracted_news.append(filtered_item)
            except json.JSONDecodeError:
                # 忽略無法解析的 JSON 資料
                continue

        # 對每個 URL 進行內部搜索
        for news in extracted_news:
            article_url = news['url']
            article_response = requests.get(article_url)

            if article_response.status_code == 200:
                article_soup = BeautifulSoup(article_response.text, 'html.parser')

                # 找到文章內容
                article_section = article_soup.find_all('section', class_='item article-body default-color mb-6 mt-5')

                # 儲存文章內容
                article_text = ''
                for section in article_section:
                    article_text += section.get_text(strip=True) + '\n'

                # 儲存文章內容到相應的條目
                news['text'] = article_text

        # 將最終的結果儲存到檔案中
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(extracted_news, json_file, ensure_ascii=False, indent=4)

        print(f"tnl: 已成功提取並儲存內容到 {path}")
