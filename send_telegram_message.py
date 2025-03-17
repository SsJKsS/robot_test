import sys
import requests
import os

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
        
        # 編碼訊息以避免亂碼
        MESSAGE = MESSAGE.encode('utf-8').decode('utf-8')

        # 測試報告的路徑（這裡以 Robot Framework 生成的 report.html 為例）
        if len(sys.argv) > 2:
            FILE_PATH = sys.argv[2]
        else:
            FILE_PATH = "tests/output/report.html"  # 預設的報告路徑，請根據實際路徑修改
        
        # 發送訊息和檔案到 Telegram
        send_telegram_message(BOT_TOKEN, CHAT_ID, MESSAGE, FILE_PATH)
