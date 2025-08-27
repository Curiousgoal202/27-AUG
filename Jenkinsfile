pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "johntech/myapp:latest"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Curiousgoal202/27-AUG.git', branch: 'master'
            }
        }

      
     

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker image..."
                    docker build -t $DOCKER_IMAGE .
                '''
            }
        }

        stage('Push Docker Image') {
            when {
                expression { return env.DOCKERHUB_USER != null && env.DOCKERHUB_PASS != null }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                 usernameVariable: 'DOCKERHUB_USER',
                                                 passwordVariable: 'DOCKERHUB_PASS')]) {
                    sh '''
                        echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        docker push $DOCKER_IMAGE
                    '''
                }
            }
        }

        stage('Stop Old Container') {
            steps {
                sh '''
                    echo "Stopping old container if running..."
                    docker rm -f myapp || true
                '''
            }
        }

        stage('Run New Container') {
            steps {
                sh '''
                    echo "Starting new container..."
                    docker run -d --name myapp -p 8080:80 $DOCKER_IMAGE
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    echo "Running Health Check..."
                    sleep 10
                    curl -f http://localhost:8085 || exit 1
                '''
            }
        }
    }

    post {
        always {
            emailext(
                subject: "Jenkins Pipeline: ${currentBuild.currentResult}",
                body: "Build finished with status: ${currentBuild.currentResult}\nCheck console output at: ${env.BUILD_URL}",
                to: "santosgoal2024@gmail.com"
            )
        }
    }
}
