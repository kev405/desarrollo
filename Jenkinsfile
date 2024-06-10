pipeline {
    agent any

    environment {
        VUE_DIR = 'vue'
        VENV = "${env.WORKSPACE}/venv"
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials-id') // Reemplaza 'dockerhub-credentials-id' con el ID de las credenciales de DockerHub en Jenkins
        DOCKER_IMAGE_VUE = "kev405/my-vue-app" // Reemplaza con tu usuario e imagen de DockerHub para Vue
        DOCKER_IMAGE_DJANGO = "kev405/my-django-app" // Reemplaza con tu usuario e imagen de DockerHub para Django
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/kev405/desarrollo.git'
            }
        }

        // Construcción de la aplicación Vue.js
        stage('Build Vue.js') {
            steps {
                dir("${VUE_DIR}") {
                    script {
                        echo "Building Vue.js application"
                    }
                    sh 'npm install'
                    sh 'npm run build'
                }
            }
        }

        // Construcción de la imagen Docker para la aplicación Vue.js
        stage('Build Vue.js Docker Image') {
            steps {
                dir("${VUE_DIR}") {
                    script {
                        echo "Building Docker image for Vue.js application"
                    }
                    sh 'sudo docker build -t ${DOCKER_IMAGE_VUE}:latest .'
                }
            }
        }

        // Construcción de la aplicación Django
        stage('Setup Virtualenv for Django') {
            steps {
                script {
                    echo "Setting up virtual environment for Django"
                }
                sh 'python3 -m venv ${VENV}'
            }
        }

        stage('Install Dependencies for Django') {
            steps {
                script {
                    echo "Installing dependencies for Django"
                }
                sh '. ${VENV}/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests for Django') {
            steps {
                script {
                    echo "Running tests for Django"
                }
                sh '. ${VENV}/bin/activate && python manage.py test'
            }
        }

        // Construcción de la imagen Docker para la aplicación Django
        stage('Build Django Docker Image') {
            steps {
                script {
                    echo "Building Docker image for Django application"
                }
                sh 'sudo docker build -t ${DOCKER_IMAGE_DJANGO}:latest .'
            }
        }

        // Iniciar sesión en DockerHub
        stage('Login to DockerHub') {
            steps {
                script {
                    echo "Logging into DockerHub"
                }
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }

        // Subir la imagen Docker de Vue.js a DockerHub
        stage('Push Vue.js Docker Image') {
            steps {
                script {
                    echo "Pushing Docker image for Vue.js application to DockerHub"
                }
                sh 'sudo docker push ${DOCKER_IMAGE_VUE}:latest'
            }
        }

        // Subir la imagen Docker de Django a DockerHub
        stage('Push Django Docker Image') {
            steps {
                script {
                    echo "Pushing Docker image for Django application to DockerHub"
                }
                sh 'sudo docker push ${DOCKER_IMAGE_DJANGO}:latest'
            }
        }

        // Desplegar la aplicación Vue.js
        // stage('Deploy Vue.js') {
        //     steps {
        //         dir("${VUE_DIR}") {
        //             script {
        //                 echo "Deploying Vue.js application"
        //             }
        //             sh 'scp -r dist/ user@server:/path/to/deploy'
        //         }
        //     }
        // }

        // // Desplegar la aplicación Django
        // stage('Deploy Django') {
        //     steps {
        //         script {
        //             echo "Deploying Django application"
        //         }
        //         sh 'scp -r * user@server:/path/to/deploy'
        //     }
        // }
    }
}
