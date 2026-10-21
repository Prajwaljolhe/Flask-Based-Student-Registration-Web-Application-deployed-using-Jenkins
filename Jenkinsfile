pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    ./venv/bin/python -m py_compile app.py
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    sudo systemctl restart student-app
                    sudo systemctl is-active --quiet student-app
                '''
            }
        }
    }

    post {

        success {
            echo 'Student Registration Application deployed successfully!'
        }

        failure {
            echo 'Deployment failed!'
        }
    }
}
