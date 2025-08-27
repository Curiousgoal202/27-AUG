pipeline {
    agent any

    environment {
        REGISTRY = "docker.io"
        IMAGE_NAME = "mywebapp"
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

    
    

        stage('Code Quality Check') {
            steps {
                sh '''
                  echo "Running HTML Linter..."
                  if command -v htmlhint > /dev/null; then
                      htmlhint .
                  else
                      echo "No html linter configured"
                  fi
                  echo "Running Python Linter..."
                  pip install flake8 || true
                  flake8 . || true
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                  echo "Running Bandit Security Scan..."
                  pip install bandit || true
                  bandit -r . || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry("https://${REGISTRY}", "${DOCKERHUB_CREDENTIALS}") {
                        dockerImage.push()
                    }
                }
            }
        }

        stage('Stop Old Container') {
            steps {
                sh '''
                  echo "Stopping old container..."
                  docker ps -q --filter "name=${IMAGE_NAME}" | grep -q . && docker stop ${IMAGE_NAME} && docker rm ${IMAGE_NAME} || true
                '''
            }
        }

        stage('Run New Container') {
            steps {
                sh '''
                  echo "Starting new container..."
                  docker run -d --name ${IMAGE_NAME} -p ${SERVER_PORT}:8085 ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                  echo "Checking if server is running..."
                  sleep 5
                  curl -f http://localhost:${SERVER_PORT} || exit 1
                '''
            }
        }
    }

    post {
        success {
            emailext(
                subject: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: "The pipeline finished successfully. Access app at http://<server-ip>:${SERVER_PORT}",
                to: "santosgoal2024@gmail.com"
            )
        }
        failure {
            emailext(
                subject: "FAILURE: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: "The pipeline failed. Please check Jenkins logs.",
                to: "santosgoal2024@gmail.com"
            )
        }
    }
}
