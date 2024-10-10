from scripts.get_data import collect_all_news, load_json, update_read_and_remove_duplicates
from scripts import analyze_news
import os
from dotenv import load_dotenv
from scripts.GetNewsData import nytc, anue, tnl

# Path
read_json_filepath = "main_system/data/read.json"
news_data_filepath = "main_system/data/news_data.json"

original_paths = [
    "main_system/data/original_data/nytc_business.json",
    "main_system/data/original_data/nytc_china.json",
    "main_system/data/original_data/nytc_technology.json",
    "main_system/data/original_data/nytc_world.json",
    "main_system/data/original_data/anue.json",
    "main_system/data/original_data/tnl.json"
]

# GetNews
nytc.business.get(original_paths[0])
nytc.china.get(original_paths[1])
nytc.technology.get(original_paths[2])
nytc.world.get(original_paths[3])
anue.get(original_paths[4])
tnl.get(original_paths[5])

analyze_data_path = "main_system/data/analyze_data.json"

news_path = "main_system/data/news_data.json"
# GetData
collect_all_news(original_paths, news_data_filepath)

news_data = load_json(news_data_filepath)
update_read_and_remove_duplicates(news_data, read_json_filepath, news_data_filepath)

# AnalyzeNews
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
analyze_news.run(openai_api_key, news_path, analyze_data_path)
