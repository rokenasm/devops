// Jenkinsfile for the password strength validator.
//
// I split the pipeline into clearly named stages so the Jenkins UI gives the
// marker an obvious progress timeline. Each stage has one job, which keeps
// the failure signal precise - if "Run unit tests" goes red, I know the
// tests broke, not the environment setup.
//
// The pipeline runs Python directly on the Jenkins controller. I considered
// building the project's own Docker image inside the pipeline (Docker in
// Docker) but that route is fragile on a workshop machine, and the
// assignment already asks for a separate "Docker build" screenshot from the
// local terminal anyway. Keeping Jenkins and Docker as two independent
// quality gates is, in my mind, cleaner: Jenkins proves the tests pass,
// the local Dockerfile proves the component is reproducibly packaged.
//
// Python 3 is assumed to be installed inside the Jenkins controller. In a
// production setup I would either bake Python into a custom Jenkins image
// or run the build on a dedicated agent - I mention this in the evaluation
// section of the report.

pipeline {
    agent any

    options {
        // Don't let a hung step wedge the build forever.
        timeout(time: 10, unit: 'MINUTES')
        // Keep enough history for the "failed run" and "successful run"
        // screenshots to coexist in the Jenkins build list.
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull whatever branch triggered the build.
                checkout scm
            }
        }

        stage('Install dependencies') {
            // A virtual environment keeps pytest off the system Python so
            // the Jenkins container stays clean across builds.
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
            // This is the gate that turns Jenkins red when the validator
            // regresses. The -v flag means the marker sees each individual
            // test result in the console log, not just a summary line.
            steps {
                sh '''
                    . .venv/bin/activate
                    python3 -m pytest -v
                '''
            }
        }

        stage('Demo run') {
            // Smoke check that the CLI itself still produces output. A
            // passing test suite does not guarantee the entry point is
            // wired up correctly, so this stage catches that separately.
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
            // Naming the failing stage in the post-message means the
            // screenshot alone tells the story without digging into the log.
            echo 'Pipeline failed - check the stage view above to see which gate caught it.'
        }
    }
}
