pipeline {
    agent any

    environment {
        APP_NAME     = "budget-tracker"
        PORT         = "5000"
        PYTHONPATH   = "."
        // Set Python and Scripts directories on the build agent
        PATH         = "C:\\Users\\RAVI\\AppData\\Local\\Programs\\Python\\Python313;C:\\Users\\RAVI\\AppData\\Local\\Programs\\Python\\Python313\\Scripts;${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Stage 1: Checkout Source Code from GitHub'
                checkout scm
            }
        }

        stage('Environment Check') {
            steps {
                echo 'Stage 2: Checking Python & Tools Environment'
                bat 'python --version'
                bat 'python -m pip --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Stage 3: Installing Application Dependencies'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Automated Tests') {
            steps {
                echo 'Stage 4: Running Automated Pytest Suite'
                bat 'python -m pytest -v'
            }
        }

        stage('Application Verification') {
            steps {
                echo 'Stage 5: Verifying Application Module and Integrity'
                bat 'python -c "import app; print(\'Application module verified successfully\')"'
            }
        }
    }

    post {
        success {
            echo '==================================================='
            echo 'Personal Budget Tracker Pipeline Completed Successfully!'
            echo '==================================================='
        }
        failure {
            echo '==================================================='
            echo 'Pipeline Execution Failed! Check Console Logs for Errors.'
            echo '==================================================='
        }
        always {
            echo 'Jenkins Pipeline Execution Finished.'
        }
    }
}
