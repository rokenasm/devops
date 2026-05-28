// Four named stages so a build's failure point is obvious from the
// stage view alone. Python runs directly on the controller; the
// project's own Docker image is built locally and screenshotted
// separately, which keeps Jenkins and Docker as two independent gates.

pipeline {
    agent any

    options {
        timeout(time: 10, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            // venv keeps pytest off the system Python.
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --quiet --upgrade pip
                    pip install --quiet -r requirements.txt
                '''
            }
        }

        stage('Run unit tests') {
            // The gate that turns the build red on regression. -v means
            // the console log shows each test, not just a summary.
            steps {
                sh '''
                    . .venv/bin/activate
                    python3 -m pytest -v
                '''
            }
        }

        stage('Demo run') {
            // A passing test suite does not prove the entry point is
            // wired up, so this stage runs the CLI as a smoke check.
            steps {
                sh '''
                    . .venv/bin/activate
                    python3 -m src.app
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline finished green - dependencies installed, tests passed, demo CLI ran.'
        }
        failure {
            echo 'Pipeline failed - check the stage view above to see which gate caught it.'
        }
    }
}
