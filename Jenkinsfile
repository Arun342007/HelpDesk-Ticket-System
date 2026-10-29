pipeline {
    agent any
    parameters {
        choice(name: 'VERSION', choices: ['v1', 'v2', 'v3'],
               description: 'Select Help Desk version')
    }
    environment {
        IMAGE = 'YOUR_DOCKERHUB_USERNAME/help-desk-system'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Test') {
            steps {
                sh 'python -m pip install -r requirements.txt'
                sh 'python -m pytest -v'
            }
        }
        stage('Build Image') {
            steps { sh 'docker build -t $IMAGE:$VERSION .' }
        }
        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN')]) {
                    sh """
                        echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push "$IMAGE:$VERSION"
                        docker logout
                    """
                }
            }
        }
        stage('Deploy') {
            steps {
                sh """
                    kubectl apply -f k8s/${VERSION}-deployment.yaml
                    kubectl apply -f k8s/${VERSION}-service.yaml
                    kubectl rollout status deployment/helpdesk-${VERSION}
                """
            }
        }
    }
}
