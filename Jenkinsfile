pipeline {
    agent any

    stages {
        stage('Deploy') {
            steps {
                script {
                    sh "docker rm -f borcelle_crm"
                    sh "docker compose up --build --detach"
                }
            }
        }
    }
}
