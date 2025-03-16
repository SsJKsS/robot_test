pipeline {
    agent any

    environment {
        PYTHON_VENV = "${WORKSPACE}/venv"
        TELEGRAM_BOT_TOKEN = credentials('TELEGRAM_BOT_TOKEN')
        TELEGRAM_CHAT_ID = credentials('TELEGRAM_CHAT_ID')
        REPO_URL = 'https://github.com/SsJKsS/robot_test.git'
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    checkout scm: [
                        $class: 'GitSCM',
                        branches: [[name: 'refs/heads/main']],
                        userRemoteConfigs: [[url: REPO_URL]]
                    ]
                }
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                script {
                    bat """
                        python --version
                        python -m venv ${PYTHON_VENV}
                    """
                }
            }
        }

        stage('Upgrade pip') {
            steps {
                script {
                    bat """
                        call ${PYTHON_VENV}\\Scripts\\activate
                        python -m pip install --upgrade pip
                    """
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    bat """
                        call ${PYTHON_VENV}\\Scripts\\activate
                        pip install -r requirements.txt
                    """
                }
            }
        }

        stage('Run Robot Tests') {
            steps {
                script {
                    bat """
                        call ${PYTHON_VENV}\\Scripts\\activate
                        robot -d results .
                    """
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
                sendTelegramNotification("✅ 測試通過！", "SUCCESS")
            }
        }

        failure {
            script {
                sendTelegramNotification("❌ 測試失敗", "FAILURE")
            }
        }
    }
}

def sendTelegramNotification(String statusMessage, String status) {
    def buildNumber = env.BUILD_NUMBER
    def reportUrl = "${env.BUILD_URL}artifact/results/report.html"
    def message = "${statusMessage}\n📌 建置編號: ${buildNumber}\n📜 狀態: ${status}\n🔗 [測試報告](${reportUrl})"

    bat """
        chcp 65001 > NUL
        set PYTHONIOENCODING=utf-8
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" ^
        -d chat_id="${TELEGRAM_CHAT_ID}" ^
        -d parse_mode="Markdown" ^
        -d text="${message}" > curl_output.txt
        type curl_output.txt || echo "無法發送 Telegram 訊息"
    """
}
