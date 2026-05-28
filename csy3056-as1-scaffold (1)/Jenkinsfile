pipeline {
    agent any

    stages {
        stage('Hello Jenkins') {
            steps {
                echo 'Hello from the CSY3056 AS1 Jenkins scaffold.'
                echo 'This Jenkinsfile is only a starting point.'
                echo 'You must adapt it to install dependencies, run pytest, and support your CI/CD evidence.'
            }
        }

        stage('Check Workspace') {
            steps {
                bat 'dir'
            }
        }
    }
}