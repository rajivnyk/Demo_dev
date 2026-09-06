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
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                sh 'pytest'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                // I added the missing '.' at the end of the build command
                // I changed the name to 'demo-flask-app' so it doesn't conflict with your old one!
                sh 'docker build -t rajiv69/demo-flask-app:latest .'
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                // Fixed the syntax for usernamePassword and credentialsId
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-cred',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    // Fixed the echo quotation marks syntax
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push rajiv69/demo-flask-app:latest
                    '''
                }
            }
        }
    }
}
