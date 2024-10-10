import openai
import json
import re
import time


def run(OPENAI_API_KEY, input_json_path, output_json_path):
    # 從環境變數中獲取 API 金鑰
    openai_api_key = OPENAI_API_KEY

    if not openai_api_key:
        raise ValueError("未能加載 API 金鑰。")

    # 設定 OpenAI 客戶端
    client = openai.OpenAI(api_key=openai_api_key)

    # 步驟 1: 建立助理
    assistant = client.beta.assistants.create(
        name="新聞分析工具",
        instructions="從提供的新聞標題、內容和連結中提取詳細資訊。針對新聞文章，執行以下操作：1. **摘要**：提供整篇新聞文章的全面摘要，至少 1000 字，非常詳細，並根據需要引用文章的部分內容，以提供清晰的主要訊息理解。2. **分類**：將新聞文章分類為相關的類別，例如財經、政治、社會、科技等。確保至少有三個分類，如果適用，總是包括'財經'和'科技'。3. **每個分類的詳細摘要**：為每個分類編寫該分類專屬的詳細摘要。每個分類摘要必須至少 300 字，提供深入的細節和背景，明確引用原始新聞內容。所有分析應該寫在一個 text 欄位中，必要時以換行符號分段。 # 輸出格式 輸出應為以下 JSON 結構：{ \"analyze\": \"總概要，使用換行符號進行分段，字數最少為 1000 字，且各部分內容詳細（只要一個）\", \"class\":[{\"name\": \"分類名稱寫這裡，如果資料適用的情況下盡量包含科技以及財經這兩個分類，是情況要加入政治以及社會\", \"text\": \"詳細分類的分析要寫這裡，字數最少500字\"}, ...這裡加入其他分類條目]}，可以類似是這樣：{\"analyze\":\"內容\",\"class\":[{\"name\":\"經濟\",\"text\":\"內容\"},{\"name\":\"科技\",\"text\":\"內容\"},{\"name\":\"社會\",\"text\":\"內容\"}]} # 注意事項 - 確保每個摘要提供足夠的上下文，以便在沒有額外資訊的情況下理解文章的主要訊息。- 分類應該是相關的且不強行添加；只包括那些真正適用的。- 如果適用，總是包括'財經'和'科技'作為分類的一部分。- 使用清晰簡潔的語言撰寫所有摘要，並提供在 JSON 結構中的所有內容。- 請使用台灣繁體中文。- 如果完全沒有新聞的話，請這樣寫:{\"analyze\":\"無最新無閲讀之新聞\",\"class\":[{\"name\":\"無資料\", \"text\":\"無資料\"}]} - 一組分類只要一個name以及一個text，如果想要多段寫文字，請也包在同一個text裡面",
        tools=[{"type": "file_search"}],
        model="gpt-4o-mini"
    )

    # 步驟 2: 建立對話線
    thread = client.beta.threads.create()

    # 步驟 3: 從 JSON 檔案中載入新聞文章
    def load_news_data(json_file_path):
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                news_data = json.load(file)
                return json.dumps(news_data, ensure_ascii=False)
        except FileNotFoundError:
            raise ValueError("未能加載 JSON 檔案：檔案未找到。")
        except json.JSONDecodeError:
            raise ValueError("未能加載 JSON 檔案：無效的 JSON 格式。")

    news_article_content = load_news_data(input_json_path)

    # 步驟 4: 將新聞內容分割成小於 API 最大長度的部分
    def split_text_into_chunks(text, max_length):
        """將過長的字串分割為多個小於指定長度的塊"""
        return [text[i:i + max_length] for i in range(0, len(text), max_length)]

    max_chunk_length = 256000  # API 限制
    chunks = split_text_into_chunks(news_article_content, max_chunk_length)

    # 步驟 5: 逐一發送每個分割後的內容
    results = []
    for chunk in chunks:
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=chunk
        )
        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)

        # 輪迴運行狀態直到完成
        run_id = run.id
        is_completed = False
        max_retries = 60
        retry_count = 0
        retry_delay = 5  # 增加輪迴間隔時間以避免超時

        while not is_completed and retry_count < max_retries:
            run_status = client.beta.threads.runs.retrieve(run_id=run_id, thread_id=thread.id)
            if run_status.status == "completed":
                is_completed = True
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                for msg in messages.data:
                    if msg.role == "assistant":
                        # 檢查 msg.content 是否是列表或字串
                        if isinstance(msg.content, list):
                            for content_piece in msg.content:
                                if isinstance(content_piece, str):
                                    results.append(content_piece)
                                else:
                                    results.append(str(content_piece))
                        elif isinstance(msg.content, str):
                            results.append(msg.content)
                        else:
                            results.append(str(msg.content))
            elif run_status.status == "failed":
                raise RuntimeError("運行失敗：" + run_status.last_error.get("message", "沒有可用的錯誤訊息"))
            else:
                retry_count += 1
                time.sleep(retry_delay)

        if retry_count >= max_retries:
            raise TimeoutError("輪迴超過最大重試次數而未完成。")

    # 步驟 6: 將所有結果整合為完整輸出
    final_output = ''.join(results)

    # 刪除最初的 { 之前的文字，和最後 } 之後的文字
    start_index = final_output.find('{')
    end_index = final_output.rfind('}')
    if start_index == -1 or end_index == -1:
        raise ValueError("無法從輸出資料中找到完整的 JSON 結構。")

    cleaned_data = final_output[start_index:end_index + 1]

    # 清理所有多餘的 \n 和空白
    # cleaned_data = cleaned_data.replace('\n', '')
    cleaned_data = re.sub(r"\s+", "", cleaned_data)
    cleaned_data = cleaned_data.replace('\\n', '')

    # 步驟 7: 將提取出的 JSON 資料保存為檔案
    with open(output_json_path, 'w', encoding='utf-8') as output_file:
        output_file.write(cleaned_data)

    print("新聞分析結果已成功保存到", output_json_path)
