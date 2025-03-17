import requests
import os
import sys

def send_telegram_message(bot_token, chat_id, message, file_path=None):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # 發送文字訊息
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    requests.post(url, data=payload)
    
    # 如果提供了文件，則同時發送文件
    if file_path and os.path.exists(file_path):
        url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
        with open(file_path, 'rb') as file:
            files = {'document': file}
            data = {'chat_id': chat_id}
            requests.post(url, data=data, files=files)

if __name__ == "__main__":
    # 從環境變數中獲取 Telegram Bot Token 和 Chat ID
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # 從環境變數中讀取 Bot Token
    CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')      # 從環境變數中讀取 Chat ID
    
    # 確保環境變數已設置
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: Telegram Bot Token or Chat ID is not set in the environment variables.")
    else:
        # 從命令行讀取訊息
        MESSAGE = sys.argv[1] if len(sys.argv) > 1 else "Test completed."
        
        # 測試報告的路徑（這裡以 Robot Framework 生成的 report.html 為例）
        if len(sys.argv) > 2:
            FILE_PATH = sys.argv[2]
        else:
            FILE_PATH = "tests/output/report.html"  # 預設的報告路徑，請根據實際路徑修改
        
        # 發送訊息和檔案到 Telegram
        send_telegram_message(BOT_TOKEN, CHAT_ID, MESSAGE, FILE_PATH)


# import requests
# import os

# def send_telegram_message(bot_token, chat_id, message, file_path=None):
#     url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
#     # 發送文字訊息
#     payload = {
#         "chat_id": chat_id,
#         "text": message
#     }
#     requests.post(url, data=payload)
    
#     # 如果提供了文件，則同時發送文件
#     if file_path and os.path.exists(file_path):
#         url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
#         files = {'document': open(file_path, 'rb')}
#         data = {'chat_id': chat_id}
#         requests.post(url, data=data, files=files)

# if __name__ == "__main__":
#     # 從環境變數中獲取 Telegram Bot Token 和 Chat ID
#     BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # 從環境變數中讀取 Bot Token
#     CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')      # 從環境變數中讀取 Chat ID
    
#     # 確保環境變數已設置
#     if not BOT_TOKEN or not CHAT_ID:
#         print("Error: Telegram Bot Token or Chat ID is not set in the environment variables.")
#     else:
#         # 自定義訊息
#         MESSAGE = "Here is the Robot Framework test report."
        
#         # 測試報告的路徑（這裡以 Robot Framework 生成的 report.html 為例）
#         FILE_PATH = "tests/output/report.html"  # 請根據實際路徑修改
        
#         # 發送訊息到 Telegram
#         send_telegram_message(BOT_TOKEN, CHAT_ID, MESSAGE, FILE_PATH)

# import os
# import requests
# import json
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# def send_telegram_message(message):
#     try:
#         # 從環境變數中獲取 Telegram Bot Token 和 Chat ID
#         bot_token = os.getenv('TELEGRAM_BOT_TOKEN')  # 取得環境變數中的 Bot Token
#         chat_id = os.getenv('TELEGRAM_CHAT_ID')      # 取得環境變數中的 Chat ID

#         if not bot_token or not chat_id:
#             raise ValueError("Telegram bot token or chat ID is missing")

#         url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
#         headers = {"Content-Type": "application/json"}
#         payload = {
#             "chat_id": chat_id,
#             "text": message,
#             "parse_mode": "Markdown"
#         }

#         # 確保訊息編碼為 UTF-8
#         encoded_message = message.encode('utf-8').decode('utf-8')
#         payload["text"] = encoded_message

#         response = requests.post(url, headers=headers, data=json.dumps(payload))

#         if response.status_code == 200:
#             print("✅ Telegram 訊息發送成功")
#         else:
#             print(f"❌ 發送訊息失敗: {response.status_code}")
    
#     except Exception as e:
#         print(f"❌ 發送訊息失敗: {e}")

# # 呼叫函數並傳入必要的參數
# if __name__ == "__main__":
#     message = "✅ Robot Framework 測試成功！"
#     send_telegram_message(message)
