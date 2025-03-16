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
                git 'https://github.com/SsJKsS/robot_test.git'
            }
        }

        stage('Setup Python and Dependencies') {
            steps {
                script {
                    bat 'python -m venv ${PYTHON_ENV}'
                    bat 'call ${PYTHON_ENV}\\Scripts\\activate && pip install --upgrade pip'
                    bat 'call ${PYTHON_ENV}\\Scripts\\activate && pip install robotframework robotframework-seleniumlibrary selenium webdriver-manager'
                }
            }
        }

        stage('Run Robot Tests') {
            steps {
                script {
                    bat 'call ${PYTHON_ENV}\\Scripts\\activate && robot -d results tests/'
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
                bat "curl -s -X POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage -d chat_id=${TELEGRAM_CHAT_ID} -d text='${message}'"
            }
        }
        failure {
            script {
                def message = "❌ Robot Framework 測試失敗！\n📌 Jenkins 報告: ${env.BUILD_URL}"
                bat "curl -s -X POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage -d chat_id=${TELEGRAM_CHAT_ID} -d text='${message}'"
            }
        }
    }
}
