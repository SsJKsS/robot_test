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
                git 'https://your-repo-url.git'
            }
        }

        stage('Setup Python and Dependencies') {
            steps {
                script {
                    sh 'python -m venv ${PYTHON_ENV}'
                    sh 'source ${PYTHON_ENV}/bin/activate && pip install --upgrade pip'
                    sh 'source ${PYTHON_ENV}/bin/activate && pip install robotframework robotframework-seleniumlibrary selenium webdriver-manager'
                }
            }
        }

        stage('Run Robot Tests') {
            steps {
                script {
                    sh 'source ${PYTHON_ENV}/bin/activate && robot -d results tests/'
                }
            }
        }

        stage('Publish Results') {
            steps {
                script {
                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: true, keepAll: true,
                                 reportDir: 'results', reportFiles: 'log.html', reportName: 'Robot Test Report'])
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
                sh "curl -s -X POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage -d chat_id=${TELEGRAM_CHAT_ID} -d text='${message}'"
            }
        }
        failure {
            script {
                def message = "❌ Robot Framework 測試失敗！\n📌 Jenkins 報告: ${env.BUILD_URL}"
                sh "curl -s -X POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage -d chat_id=${TELEGRAM_CHAT_ID} -d text='${message}'"
            }
        }
    }
}
