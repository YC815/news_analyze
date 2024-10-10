import requests
import json
from bs4 import BeautifulSoup


def get(path):
    # 獲取新聞列表信息
    page = 1
    limit = 30
    headers = {
        'Origin': 'https://news.cnyes.com/',
        'Referer': 'https://news.cnyes.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    r = requests.get(f"https://api.cnyes.com/media/api/v1/newslist/category/headline?page={page}&limit={limit}", headers=headers)

    if r.status_code == requests.codes.ok:
        data = r.json()  # 直接將 JSON 數據儲存到變數中

        # 檢查 data 的類型和結構
        if isinstance(data, dict):
            newslist_info = data.get('items', {})  # 確保獲取的數據是字典

            # 確認 newslist_info 是否有正確的鍵
            if isinstance(newslist_info, dict) and 'data' in newslist_info:
                news_data = newslist_info['data']  # 獲取 data 列表
                extracted_news = []

                for news in news_data:
                    name = news['title']
                    url = f"https://news.cnyes.com/news/id/{news['newsId']}"

                    # 獲取內容
                    article_response = requests.get(url, headers=headers)
                    if article_response.status_code == requests.codes.ok:
                        # 解析 HTML
                        soup = BeautifulSoup(article_response.text, 'lxml')
                        main_content = soup.find('main', id='article-container')
                        paragraphs = main_content.find_all('p')
                        text = " ".join([p.get_text() for p in paragraphs])  # 組合所有<p>的文本

                        # 將提取的新聞資料儲存
                        extracted_news.append({'name': name, 'url': url, 'text': text})

                # 將結果儲存為 JSON 檔案
                with open(path, 'w', encoding='utf-8') as json_file:
                    json.dump(extracted_news, json_file, ensure_ascii=False, indent=4)
                print(f"anue: 已成功提取並儲存內容到 {path}")
