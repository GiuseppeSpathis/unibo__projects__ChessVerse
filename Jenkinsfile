
pipeline {
    agent any

    stages {
        stage('SCM') {
            steps {
                checkout scm
            }
        }

        stage('Build and Test App') {
			when {
				anyOf {
					branch "main"
					branch "testing"
					branch "dev-app"
				}
			}
            steps {
                dir('code/app') {
                    nodejs(nodeJSInstallationName: 'NodeJS21_1_0') {
                        sh 'npm install'
                        sh 'npm run coverage:prod'
                    }
                }
            }
        }

        stage('Build and Test api backend') {
			when {
				anyOf {
					branch "main"
					branch "testing"
					branch "dev-api"
				}
			}
            steps {
                dir('code/django') {
                    // Add your Python testing commands here
                    sh 'pip install -r requirements.txt'
                    sh 'python3.12 manage.py test backend.test"'
                }
            }
        }

        stage('Build and Test game backend') {
			when {
				anyOf {
					branch "main"
					branch "testing"
					branch "dev-game"
				}
			}
            agent {
                docker {
                    image 'python:3'
                }
            }
            steps {
                dir('code/game/') {
                    // Add your Python testing commands here
                    sh 'pip install -r requirements.txt'
                    sh 'cd test/unit'
                    sh 'python3.12 -m unittest unit_test.TestChessSocketIO'
                }
            }
        }

        stage('SonarQube Analysis') {
			when {
				anyOf {
					branch "main"
					branch "testing"
				}
			}
            steps {
                dir('code/app') {
                    nodejs(nodeJSInstallationName: 'NodeJS21_1_0') {
						script {
							def scannerHome = tool 'SonarScanner4'
							withSonarQubeEnv("sonarqube") {
								sh "${scannerHome}/bin/sonar-scanner"
							}
						}
                    }
                }
            }
        }

    }
}
