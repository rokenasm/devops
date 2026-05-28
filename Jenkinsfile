// Jenkinsfile for the password strength validator.
//
// The pipeline is split into four named stages so the Jenkins UI gives the
// marker a clear progress timeline. Each stage has one job, which keeps the
// failure signal precise - if "Run unit tests" goes red, I know the tests
// broke, not the install step.
//
// I chose a Docker-based pipeline because the assignment is graded on
// reproducibility as well as test outcomes. Building the same Docker image
// in CI as the one I run locally means the test environment is identical
// between my laptop, Jenkins, and any future deployment target.
//
// The agent assumes a Jenkins controller that has Docker available. The
// quickest way to get that locally is the Jenkins-in-Docker recipe, which
// is the route I used for the screenshots. Because the controller is a
// Linux container, all shell steps use `sh` rather than `bat` - on a
// Windows agent you would swap those over.

pipeline {
    agent any

    options {
        // Don't let a hung Docker layer wedge the build forever.
        timeout(time: 15, unit: 'MINUTES')
        // Keep enough history for the "failed run" and "successful run"
        // screenshots to coexist in the Jenkins UI.
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull whatever branch triggered the build.
                checkout scm
            }
        }

        stage('Build image') {
            // Building the image is itself a quality gate - if the Dockerfile
            // is broken, the pipeline fails here before any tests run, which
            // is the fastest possible feedback.
            steps {
                sh 'docker build -t password-validator:${BUILD_NUMBER} .'
            }
        }

        stage('Run unit tests') {
            // Tests run inside the just-built image so the test environment
            // matches the deploy environment exactly. This is the stage that
            // turns Jenkins red when the validator regresses.
            steps {
                sh 'docker run --rm password-validator:${BUILD_NUMBER} python -m pytest -v'
            }
        }

        stage('Demo run') {
            // A quick smoke check that the CLI itself still produces output.
            // Useful because a passing test suite does not guarantee that
            // the entry point in the Dockerfile is wired up correctly.
            steps {
                sh 'docker run --rm password-validator:${BUILD_NUMBER}'
            }
        }
    }

    post {
        success {
            echo 'Pipeline finished green - the validator built, tested and ran inside Docker.'
        }
        failure {
            // The point of saying which stage failed is so the screenshot
            // alone tells the story without needing to dig into the log.
            echo 'Pipeline failed - check the stage view above to see which gate caught it.'
        }
        always {
            // Don't leave a graveyard of test images on the Jenkins host.
            sh 'docker image rm password-validator:${BUILD_NUMBER} || true'
        }
    }
}
