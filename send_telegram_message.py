import os
import requests
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def send_telegram_message(message):
    try:
        # 從環境變數中獲取 Telegram Bot Token 和 Chat ID
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')  # 取得環境變數中的 Bot Token
        chat_id = os.getenv('TELEGRAM_CHAT_ID')      # 取得環境變數中的 Chat ID

        if not bot_token or not chat_id:
            raise ValueError("Telegram bot token or chat ID is missing")

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        headers = {"Content-Type": "application/json"}
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        # 確保訊息編碼為 UTF-8
        encoded_message = message.encode('utf-8').decode('utf-8')
        payload["text"] = encoded_message

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("✅ Telegram 訊息發送成功")
        else:
            print(f"❌ 發送訊息失敗: {response.status_code}")
    
    except Exception as e:
        print(f"❌ 發送訊息失敗: {e}")

# 呼叫函數並傳入必要的參數
if __name__ == "__main__":
    message = "✅ Robot Framework 測試成功！"
    send_telegram_message(message)
