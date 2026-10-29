pipeline {
    agent any

    parameters {
        choice(name: 'VERSION', choices: ['v1', 'v2', 'v3'], description: 'Select matching source version')
    }

    environment {
        IMAGE = 'YOUR_DOCKERHUB_USERNAME/leave-system'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh 'python -m pip install -r requirements.txt'
                sh 'python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE:$VERSION .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push "$IMAGE:$VERSION"
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f k8s/${VERSION}-deployment.yaml
                    kubectl apply -f k8s/${VERSION}-service.yaml
                    kubectl rollout status deployment/leave-${VERSION}
                '''
            }
        }
    }
}
