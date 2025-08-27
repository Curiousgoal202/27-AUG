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
