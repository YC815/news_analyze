import requests
from bs4 import BeautifulSoup
import json
import urllib3


class business:
    def get(path):
        # 禁用 SSL 警告
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # 1. 第一段：發送GET請求獲取主頁文章
        url = "https://m.cn.nytimes.com/business"
        response = requests.get(url, verify=False)
        response.encoding = 'utf-8'
        html_content = response.text

        # 2. 解析主頁HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        main_list = soup.find('div', class_='row main-list')

        articles = []
        if main_list:
            article_list = main_list.find('div', class_='articles').find('ol', class_='article-list')
            article_items = article_list.find_all('li', class_='regular-item')

            # 提取文章標題和URL
            for item in article_items:
                a_tag = item.find('a')
                if a_tag:
                    title = a_tag['title']
                    href = a_tag['href']
                    articles.append({'name': title, 'url': href})

        # 3. 第二段：提取每個URL中的文章內容
        for article in articles:
            article_url = article['url']
            response = requests.get(article_url, verify=False)
            response.encoding = 'utf-8'
            article_content = response.text

            # 解析文章內容
            article_soup = BeautifulSoup(article_content, 'html.parser')
            paragraphs = article_soup.find_all('div', class_='article-paragraph')

            # 收集段落中的文字
            text_content = []
            for paragraph in paragraphs:
                text_content.append(paragraph.get_text(strip=True))  # 去除多餘空格

            # 將文字組合成一串
            article['text'] = ' '.join(text_content)

        # 4. 將結果存入JSON檔案
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(articles, json_file, ensure_ascii=False, indent=4)

        print("nytc-business: 資料已成功抓取並儲存至 {path}")


class china:
    def get(path):
        # 禁用 SSL 警告
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # 1. 第一段：發送GET請求獲取主頁文章
        url = "https://m.cn.nytimes.com/china"
        response = requests.get(url, verify=False)
        response.encoding = 'utf-8'
        html_content = response.text

        # 2. 解析主頁HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        main_list = soup.find('div', class_='row main-list')

        articles = []
        if main_list:
            article_list = main_list.find('div', class_='articles').find('ol', class_='article-list')
            article_items = article_list.find_all('li', class_='regular-item')

            # 提取文章標題和URL
            for item in article_items:
                a_tag = item.find('a')
                if a_tag:
                    title = a_tag['title']
                    href = a_tag['href']
                    articles.append({'name': title, 'url': href})

        # 3. 第二段：提取每個URL中的文章內容
        for article in articles:
            article_url = article['url']
            response = requests.get(article_url, verify=False)
            response.encoding = 'utf-8'
            article_content = response.text

            # 解析文章內容
            article_soup = BeautifulSoup(article_content, 'html.parser')
            paragraphs = article_soup.find_all('div', class_='article-paragraph')

            # 收集段落中的文字
            text_content = []
            for paragraph in paragraphs:
                text_content.append(paragraph.get_text(strip=True))  # 去除多餘空格

            # 將文字組合成一串
            article['text'] = ' '.join(text_content)

        # 4. 將結果存入JSON檔案
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(articles, json_file, ensure_ascii=False, indent=4)

        print(f"nytc-china: 資料已成功抓取並儲存至 {path}")


class technology:
    def get(path):
        # 禁用 SSL 警告
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # 1. 第一段：發送GET請求獲取主頁文章
        url = "https://m.cn.nytimes.com/technology"
        response = requests.get(url, verify=False)
        response.encoding = 'utf-8'
        html_content = response.text

        # 2. 解析主頁HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        main_list = soup.find('div', class_='row main-list')

        articles = []
        if main_list:
            article_list = main_list.find('div', class_='articles').find('ol', class_='article-list')
            article_items = article_list.find_all('li', class_='regular-item')

            # 提取文章標題和URL
            for item in article_items:
                a_tag = item.find('a')
                if a_tag:
                    title = a_tag['title']
                    href = a_tag['href']
                    articles.append({'name': title, 'url': href})

        # 3. 第二段：提取每個URL中的文章內容
        for article in articles:
            article_url = article['url']
            response = requests.get(article_url, verify=False)
            response.encoding = 'utf-8'
            article_content = response.text

            # 解析文章內容
            article_soup = BeautifulSoup(article_content, 'html.parser')
            paragraphs = article_soup.find_all('div', class_='article-paragraph')

            # 收集段落中的文字
            text_content = []
            for paragraph in paragraphs:
                text_content.append(paragraph.get_text(strip=True))  # 去除多餘空格

            # 將文字組合成一串
            article['text'] = ' '.join(text_content)

        # 4. 將結果存入JSON檔案
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(articles, json_file, ensure_ascii=False, indent=4)

        print(f"nytc-technology: 資料已成功抓取並儲存至 {path}")


class world:
    def get(json_path):
        # 禁用 SSL 警告
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # 1. 第一段：發送GET請求獲取主頁文章
        url = "https://m.cn.nytimes.com/world"
        response = requests.get(url, verify=False)
        response.encoding = 'utf-8'
        html_content = response.text

        # 2. 解析主頁HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        main_list = soup.find('div', class_='row main-list')

        articles = []
        if main_list:
            article_list = main_list.find('div', class_='articles').find('ol', class_='article-list')
            article_items = article_list.find_all('li', class_='regular-item')

            # 提取文章標題和URL
            for item in article_items:
                a_tag = item.find('a')
                if a_tag:
                    title = a_tag['title']
                    href = a_tag['href']
                    articles.append({'name': title, 'url': href})

        # 3. 第二段：提取每個URL中的文章內容
        for article in articles:
            article_url = article['url']
            response = requests.get(article_url, verify=False)
            response.encoding = 'utf-8'
            article_content = response.text

            # 解析文章內容
            article_soup = BeautifulSoup(article_content, 'html.parser')
            paragraphs = article_soup.find_all('div', class_='article-paragraph')

            # 收集段落中的文字
            text_content = []
            for paragraph in paragraphs:
                text_content.append(paragraph.get_text(strip=True))  # 去除多餘空格

            # 將文字組合成一串
            article['text'] = ' '.join(text_content)

        # 4. 將結果存入JSON檔案
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(articles, json_file, ensure_ascii=False, indent=4)

        print(f"nytc-world: 資料已成功抓取並儲存至 {json_path}")
