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
                    checkout scm: [
                        $class: 'GitSCM',
                        branches: [[name: 'refs/heads/main']], 
                        userRemoteConfigs: [[url: 'https://github.com/SsJKsS/robot_test.git']]
                    ]
                }
            }
        }

        stage('Setup Python and Create Virtual Environment') {
            steps {
                script {
                    bat 'python --version'
                    bat 'echo %PYTHON_ENV%'
                    bat 'python -m venv %PYTHON_ENV%'
                }
            }
        }

        stage('Upgrade pip') {
            steps {
                script {
                    echo "升級 pip..."
                    bat """
                        call %PYTHON_ENV%\\Scripts\\activate
                        python -m pip install --upgrade pip
                    """
                    bat 'call %PYTHON_ENV%\\Scripts\\activate && pip --version'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
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
                    bat 'call %PYTHON_ENV%\\Scripts\\activate && robot -d results .'
                }
            }
        }

        stage('Publish Results') {
            steps {
                script {
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
            archiveArtifacts artifacts: 'results/*', fingerprint: true
        }
        success {
            script {
                def message = "✅ Robot Framework 測試成功！\n📌 Jenkins 報告: ${env.BUILD_URL}"
                sendTelegramMessage(message)
            }
        }
        failure {
            script {
                def message = "❌ Robot Framework 測試失敗！\n📌 Jenkins 報告: ${env.BUILD_URL}"
                sendTelegramMessage(message)
            }
        }
    }
}

def sendTelegramMessage(String message) {
    try {
        bat """
            chcp 65001 > nul
            set PYTHONIOENCODING=utf-8
            powershell -Command "& {
                \$message = '${message.replace('\n', '\n')}'
                Invoke-RestMethod -Uri 'https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage' `
                -Method Post -Body (@{ chat_id='${TELEGRAM_CHAT_ID}'; text=\$message; parse_mode='Markdown' } | ConvertTo-Json -Compress) `
                -ContentType 'application/json'
            }"
        """
    } catch (Exception e) {
        echo "❌ 發送 Telegram 訊息失敗: ${e.message}"
    }
}
