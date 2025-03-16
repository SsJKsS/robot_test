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
                def message = "✅ Robot Framework 測試成功！\n📌 Jenkins 報告: ${env.BUILD_URL}"

                // 使用 Powershell 發送 UTF-8 編碼消息
                def encodedMessage = URLEncoder.encode(message, "UTF-8")
                
                powershell """
                    $message = '${encodedMessage}'
                    $url = 'https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage'
                    $chatId = '${TELEGRAM_CHAT_ID}'
                    Invoke-RestMethod -Uri \$url -Method Post -Body @{
                        chat_id = \$chatId
                        text = \$message
                    }
                """
            }
        }
        failure {
            script {
                def message = "❌ Robot Framework 測試失敗！\n📌 Jenkins 報告: ${env.BUILD_URL}"

                // 使用 Powershell 發送 UTF-8 編碼消息
                def encodedMessage = URLEncoder.encode(message, "UTF-8")
                
                powershell """
                    $message = '${encodedMessage}'
                    $url = 'https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage'
                    $chatId = '${TELEGRAM_CHAT_ID}'
                    Invoke-RestMethod -Uri \$url -Method Post -Body @{
                        chat_id = \$chatId
                        text = \$message
                    }
                """
            }
        }
    }

}
