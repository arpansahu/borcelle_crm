pipeline {
    agent any

    stages {
        stage('Production') {
            steps {
                script {
                    sh "docker rm -f borcelle_crm"
                    sh "docker compose up --build --detach"
                }
            }
        }
    }
}
