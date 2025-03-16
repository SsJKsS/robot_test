*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}              https://www.google.com
${SEARCH_BOX}       xpath=//textarea[@name="q"]
${SEARCH_BUTTON}    xpath=(//input[@name="btnK"])[1]

*** Keywords ***
打開谷哥
    Open Browser    ${URL}    chrome
    Maximize Browser Window
    Wait Until Element Is Visible    ${SEARCH_BOX}    5s

輸入關鍵字
    [Arguments]    ${keyword}
    Input Text    ${SEARCH_BOX}    ${keyword}

關閉瀏覽器
    Close Browser
