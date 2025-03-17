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
                        call "%PYTHON_ENV%\\Scripts\\activate.bat"
                        python -m pip install --upgrade pip
                        pip install robotframework robotframework-seleniumlibrary selenium webdriver-manager
                        pip install requests
                    """
                }
            }
        }

        stage('Run Robot Tests') {
            steps {
                script {
                    bat """
                        chcp 65001 > nul
                        call "%PYTHON_ENV%\\Scripts\\activate.bat"
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
                bat """
                    chcp 65001 > nul
                    call "%PYTHON_ENV%\\Scripts\\activate.bat"
                    python send_telegram_message.py "✅Robot Framework tests passed successfully!✅" "C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\selenium\\results\\log.html"
                """
            }
        }

        failure {
            script {
                bat """
                    chcp 65001 > nul
                    call "%PYTHON_ENV%\\Scripts\\activate.bat"
                    python send_telegram_message.py "❌Robot Framework tests failed. Please check the logs.❌" "C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\selenium\\results\\log.html"
                """
            }
        }
    }
}
