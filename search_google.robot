*** Settings ***
Resource    resources/google_page.robot

*** Test Cases ***
Search Dog On Google
    打開谷哥
    Sleep    2s   # 等待頁面載入，模擬真人行為
    輸入關鍵字    狗
    Sleep    2s   # 等待頁面載入，模擬真人行為
    關閉瀏覽器