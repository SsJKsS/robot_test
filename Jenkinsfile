pipeline {
    agent any

    environment {
        PYTHON_ENV = "${WORKSPACE}/venv"
        RESULTS_DIR = "${WORKSPACE}/results"
        TELEGRAM_BOT_TOKEN = credentials('TELEGRAM_BOT_TOKEN')  // 讀取 Jenkins Credentials
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
                        chcp 65001 > nul
                        python --version
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
            archiveArtifacts artifacts: 'results/*', fingerprint: true  // ✅ 直接使用，不用 `node {}`
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
        powershell """
            \$message = '${message}'
            \$uri = 'https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage'
            \$body = @{
                chat_id = '${TELEGRAM_CHAT_ID}'
                text = \$message
                parse_mode = 'Markdown'
            } | ConvertTo-Json -Compress
            Invoke-RestMethod -Uri \$uri -Method Post -ContentType 'application/json' -Body \$body
        """
    } catch (Exception e) {
        echo "❌ 發送 Telegram 訊息失敗: ${e.message}"
    }
}
