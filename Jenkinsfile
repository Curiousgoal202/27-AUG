pipeline {
    agent any
    tools {
        // Remove Maven since no pom.xml in repo
        // maven 'Maven3'
    }
    environment {
        REGISTRY = "docker.io"
        IMAGE_NAME = "server"
        IMAGE_TAG = "latest"
        DOCKERHUB_CREDENTIALS = "creds"
        SERVER_PORT = "8085"
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/Curiousgoal202/27-AUG.git'
            }
        }
        stage('Build') {
            steps {
                echo "Skipping Maven build (no pom.xml). If Python packaging needed, add here."
            }
        }
        stage('Test') {
            steps {
                echo "No Java unit tests found. Add pytest/unittest if Python tests exist."
            }
        }
        stage('Code Quality - Python') {
            steps {
                sh '''
                    pip install flake8 bandit
                    flake8 . || true
                    bandit -r . || true
                '''
            }
        }
        stage('Code Quality - HTML') {
            steps {
                sh '''
                    npm install -g htmlhint
                    htmlhint *.html || true
                '''
            }
        }
        stage('Security Scan') {
            steps {
                sh 'docker run --rm -i hadolint/hadolint < Dockerfile || true'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh "docker build -t $IMAGE_NAME:$IMAGE_TAG ."
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS')]) {
                        sh """
                            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                            docker tag $IMAGE_NAME:$IMAGE_TAG $DOCKER_USER/$IMAGE_NAME:$IMAGE_TAG
                            docker push $DOCKER_USER/$IMAGE_NAME:$IMAGE_TAG
                        """
                    }
                }
            }
        }
        stage('Stop Old Container') {
            steps {
                sh """
                    docker stop webserver || true
                    docker rm webserver || true
                """
            }
        }
        stage('Start New Container') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS')]) {
                        sh """
                            docker run -d --name webserver -p $SERVER_PORT:80 $DOCKER_USER/$IMAGE_NAME:$IMAGE_TAG
                        """
                    }
                }
            }
        }
        stage('Health Check') {
            steps {
                script {
                    sh "sleep 5"
                    sh "curl -f http://localhost:$SERVER_PORT || exit 1"
                }
            }
        }
    } // closes stages
    post {
        success {
            echo "✅ Deployment successful!"
            emailext (
                to: 'santosgoal2024@gmail.com',
                subject: "SUCCESS: Webserver Pipeline",
                body: "Your webserver is up on port $SERVER_PORT"
            )
        }
        failure {
            echo "❌ Deployment failed!"
            emailext (
                to: 'santosgoal2024@gmail.com',
                subject: "FAILED: Webserver Pipeline",
                body: "Please check the Jenkins logs for details."
            )
        }
    }
} // closes pipeline
