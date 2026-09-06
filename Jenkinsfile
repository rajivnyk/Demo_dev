pipeline {

    triggers {
        githubPush()
    }

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
                sh './venv/bin/pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t rajiv69/demo-flask-app:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-cred',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push rajiv69/demo-flask-app:latest
                    '''
                }
            }
        }
    }

    post {

        success {
            emailext(
                subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    Jenkins Build Successful!

                    Job: ${env.JOB_NAME}
                    Build Number: ${env.BUILD_NUMBER}
                    Status: SUCCESS

                    Docker image:
                    rajiv69/demo-flask-app:latest

                    Build URL:
                    ${env.BUILD_URL}
                """,
                to: "your-email@gmail.com"
            )
        }

        failure {
            emailext(
                subject: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    Jenkins Build Failed!

                    Job: ${env.JOB_NAME}
                    Build Number: ${env.BUILD_NUMBER}
                    Status: FAILURE

                    Please check the Jenkins console output.

                    Build URL:
                    ${env.BUILD_URL}
                """,
                to: "your-email@gmail.com"
            )
        }
    }
}