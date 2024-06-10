pipeline {
    agent any

    environment {
        VUE_DIR = 'vue'
        VENV = "${env.WORKSPACE}/venv"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/kev405/desarrollo.git'
            }
        }
        
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
