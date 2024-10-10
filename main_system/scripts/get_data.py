import json
import os


def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # 如果檔案是空的，回傳空列表
                return []
    else:
        return []

# 儲存 JSON 檔案


def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 匯集所有新聞資料到一個檔案


def collect_all_news(original_paths, output_path):
    all_news = []
    for path in original_paths:
        news_data = load_json(path)
        all_news.extend(news_data)
    save_json(output_path, all_news)

# 檢查並更新 JSON 的函式


# 檢查並更新 JSON 的函式
def update_read_and_remove_duplicates(news_items, read_filepath, news_filepath):
    read_data = load_json(read_filepath)
    read_names = {item for item in read_data}

    # 更新新聞資料，刪除已存在於 read.json 中的新聞項目
    updated_news_items = []
    for news in news_items:
        if news["name"] in read_names:
            # 如果 name 已存在於 read.json 中，將該條目略過 (不加入更新後的資料)
            continue
        else:
            # 如果 name 不存在於 read.json 中，將條目加入更新的新聞資料
            updated_news_items.append(news)
            read_names.add(news["name"])

    # 儲存更新後的 read.json 檔案
    save_json(read_filepath, list(read_names))
    # 儲存更新後的新聞資料檔案，將已經過濾的新聞資料儲存
    save_json(news_filepath, updated_news_items)


# 主程式
if __name__ == "__main__":
    read_json_filepath = "main_system/data/read.json"
    news_data_filepath = "main_system/data/news_data.json"

    # 原始資料檔案路徑
    original_paths = [
        "main_system/data/original_data/nytc_business.json",
        "main_system/data/original_data/nytc_china.json",
        "main_system/data/original_data/nytc_technology.json",
        "main_system/data/original_data/nytc_world.json",
        "main_system/data/original_data/anue.json",
        "main_system/data/original_data/tnl.json"
    ]

    # 匯集所有新聞資料到 news_data.json
    collect_all_news(original_paths, news_data_filepath)

    # 從匯集的新聞資料中取得新聞並進行更新
    news_data = load_json(news_data_filepath)
    update_read_and_remove_duplicates(news_data, read_json_filepath, news_data_filepath)
