pipeline {
    agent any

    environment {
        PYTHON_ENV = "${WORKSPACE}/venv"
        TELEGRAM_BOT_TOKEN = "7597395246:AAEwY29V9_Vcdi-I4Odu9pNGRQfkK3yVvQY"
        TELEGRAM_CHAT_ID = "7401334685"
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
                    bat """
                        call %PYTHON_ENV%\\Scripts\\activate
                        python -m pip install --upgrade pip
                        pip --version
                    """
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
                def buildNumber = env.BUILD_NUMBER
                def buildStatus = "SUCCESS"
                def reportUrl = "${env.BUILD_URL}artifact/results/report.html"
                def message = "✅ Test Pass!\n📌 Build Number: ${buildNumber}\n📜 Status: ${buildStatus}\n🔗 [Robot Report](${reportUrl})"

                bat """
                    chcp 65001 > NUL
                    set PYTHONIOENCODING=utf-8
                    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" ^
                    -d chat_id="${TELEGRAM_CHAT_ID}" ^
                    -d parse_mode="Markdown" ^
                    -d text="${message}" > curl_output.txt
                    type curl_output.txt || echo "Failed to send Telegram message."
                """
            }
        }
        failure {
            script {
                def buildNumber = env.BUILD_NUMBER
                def buildStatus = "FAILURE"
                def reportUrl = "${env.BUILD_URL}artifact/results/report.html"
                def message = "❌ Test Fail\n📌 Build Number: ${buildNumber}\n📜 Status: ${buildStatus}\n🔗 [Robot Report](${reportUrl})"

                bat """
                    chcp 65001 > NUL
                    set PYTHONIOENCODING=utf-8
                    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" ^
                    -d chat_id="${TELEGRAM_CHAT_ID}" ^
                    -d parse_mode="Markdown" ^
                    -d text="${message}" > curl_output.txt
                    type curl_output.txt || echo "Failed to send Telegram message."
                """
            }
        }
    }
}
