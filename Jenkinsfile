pipeline {
    agent any

    environment {
        PYTHON_ENV = "${WORKSPACE}/venv"
        TELEGRAM_BOT_TOKEN = "7597395246:AAEwY29V9_Vcdi-I4Odu9pNGRQfkK3yVvQY"
        TELEGRAM_CHAT_ID = "7401334685"   // 你的 Chat ID
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    // 確保檢出的是 'main' 分支
                    checkout scm: [
                        $class: 'GitSCM',
                        branches: [[name: 'refs/heads/main']], // 確保分支名稱為 'main'
                        userRemoteConfigs: [[url: 'https://github.com/SsJKsS/robot_test.git']]
                    ]
                }
            }
        }

        stage('Setup Python and Create Virtual Environment') {
            steps {
                script {
                    // 檢查 Python 是否可用
                    bat 'python --version'

                    // 顯示 PYTHON_ENV 變數
                    bat 'echo %PYTHON_ENV%'

                    // 創建虛擬環境
                    bat 'python -m venv %PYTHON_ENV%'
                }
            }
        }

        stage('Upgrade pip') {
            steps {
                script {
                    // 升級 pip
                    echo "升級 pip..."
                    bat """
                        call %PYTHON_ENV%\\Scripts\\activate
                        python -m pip install --upgrade pip
                    """
                    
                    // 確保 pip 已升級
                    bat 'call %PYTHON_ENV%\\Scripts\\activate && pip --version'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // 安裝所需的 Python 依賴
                    bat """
                        call %PYTHON_ENV%\\Scripts\\activate
                        pip install robotframework robotframework-seleniumlibrary selenium webdriver-manager
                    """
                }
            }
        }

        stage('Run Robot Tests') {
            steps {
                script {
                    // 執行 Robot 測試
                    bat 'call %PYTHON_ENV%\\Scripts\\activate && robot -d results .'
                }
            }
        }

        stage('Publish Results') {
            steps {
                script {
                    // 發佈 HTML 測試報告
                    publishHTML(target: [
                        reportDir: 'results', 
                        reportFiles: 'log.html', 
                        reportName: 'Robot Test Report'
                    ])
                }
            }
        }
    }

    post {
        always {
            // 儲存測試結果
            archiveArtifacts artifacts: 'results/*', fingerprint: true
        }
        success {
            script {
                // 取得當前建構編號和狀態
                def buildNumber = env.BUILD_NUMBER
                def buildStatus = "SUCCESS"
                
                // 生成成功訊息，包含測試報告的 URL、建構編號和建構狀態
                def message = "Test Pass！\nBuild Status: ${buildStatus}\nBuild Number: ${buildNumber}\n📌 Robot Report: ${env.BUILD_URL}artifact/results/report.html"

                // 直接發送訊息到 Telegram，不進行 URL 編碼
                bat """
                    set LANG=en_US.UTF-8
                    curl -s -X POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage ^
                    -d chat_id=${TELEGRAM_CHAT_ID} ^
                    -d text="${message}"
                """
            }
        }
        failure {
            script {
                // 取得當前建構編號和狀態
                def buildNumber = env.BUILD_NUMBER
                def buildStatus = "FAILURE"
                
                // 生成失敗訊息，包含測試報告的 URL、建構編號和建構狀態
                def message = "Test Fail\nBuild Status: ${buildStatus}\nBuild Number: ${buildNumber}\n📌 Report: ${env.BUILD_URL}artifact/results/report.html"

                // 直接發送訊息到 Telegram，不進行 URL 編碼
                bat """
                    set LANG=en_US.UTF-8
                    curl -s -X POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage ^
                    -d chat_id=${TELEGRAM_CHAT_ID} ^
                    -d text="${message}"
                """
            }
        }
    }

}
