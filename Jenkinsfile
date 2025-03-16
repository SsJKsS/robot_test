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

        stage('Setup Python and Dependencies') {
            steps {
                script {
                    // 檢查 Python 是否可用
                    bat 'python --version'

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
                
                // 取得 Jenkins CSRF token
                def crumb = bat(script: "curl -s -u ${env.JENKINS_USER}:${env.JENKINS_API_TOKEN} ${env.JENKINS_URL}/crumbIssuer/api/xml", returnStdout: true).trim()
                def csrfToken = crumb.split('<crumb>')[1].split('</crumb>')[0]

                // 發送成功消息到 Telegram
                bat "curl -s -X POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage -d chat_id=${TELEGRAM_CHAT_ID} -d text='${message}' -H 'Jenkins-Crumb:${csrfToken}'"
            }
        }
        failure {
            script {
                def message = "❌ Robot Framework 測試失敗！\n📌 Jenkins 報告: ${env.BUILD_URL}"

                // 取得 Jenkins CSRF token
                def crumb = bat(script: "curl -s -u ${env.JENKINS_USER}:${env.JENKINS_API_TOKEN} ${env.JENKINS_URL}/crumbIssuer/api/xml", returnStdout: true).trim()
                def csrfToken = crumb.split('<crumb>')[1].split('</crumb>')[0]

                // 發送失敗消息到 Telegram
                bat "curl -s -X POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage -d chat_id=${TELEGRAM_CHAT_ID} -d text='${message}' -H 'Jenkins-Crumb:${csrfToken}'"
            }
        }
    }
}
