pipeline {
    agent any

    environment {
        PYTHON_ENV = "${WORKSPACE}/venv"
        RESULTS_DIR = "${WORKSPACE}/results"
        TELEGRAM_BOT_TOKEN = credentials('TELEGRAM_BOT_TOKEN')  // 從 Jenkins Credentials 設定
        TELEGRAM_CHAT_ID = "7401334685"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    bat '''
                        chcp 65001 > nul  // 設定 cmd 為 UTF-8
                        python --version
                        echo 正在建立虛擬環境...
                        python -m venv "%PYTHON_ENV%"
                    '''
                }
            }
        }

        stage('Upgrade pip and Install Dependencies') {
            steps {
                script {
                    bat """
                        chcp 65001 > nul
                        call "%PYTHON_ENV%\\Scripts\\activate"
                        python -m pip install --upgrade pip
                        pip install robotframework robotframework-seleniumlibrary selenium webdriver-manager
                    """
                }
            }
        }

        stage('Run Robot Tests') {
            steps {
                script {
                    bat """
                        chcp 65001 > nul
                        call "%PYTHON_ENV%\\Scripts\\activate"
                        set PYTHONIOENCODING=utf-8
                        robot --outputdir "%RESULTS_DIR%" --loglevel DEBUG .
                    """
                }
            }
        }

        stage('Publish Results') {
            steps {
                publishHTML(target: [
                    reportDir: 'results', 
                    reportFiles: 'log.html', 
                    reportName: 'Robot Test Report'
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'results/*', fingerprint: true
        }

        success {
            script {
                sendTelegramMessage("✅ Robot Framework 測試成功！\n📌 Jenkins 報告: ${env.BUILD_URL}")
            }
        }

        failure {
            script {
                sendTelegramMessage("❌ Robot Framework 測試失敗！\n📌 Jenkins 報告: ${env.BUILD_URL}")
            }
        }
    }
}

def sendTelegramMessage(String message) {
    try {
        bat """
            chcp 65001 > nul
            curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" ^
            --header "Content-Type: application/json" ^
            --data "{\\"chat_id\\":\\"${TELEGRAM_CHAT_ID}\\", \\"text\\":\\"${message}\\", \\"parse_mode\\":\\"Markdown\\"}"
        """
    } catch (Exception e) {
        echo "❌ 發送 Telegram 訊息失敗: ${e.message}"
    }
}
