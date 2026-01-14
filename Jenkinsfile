pipeline {
    agent any

    environment {
        SHOOL = "datascientest"
        NAME = "Anthony"
    }

    stages {
        stage("Env Variables") {
            environment {
                NAME = "lewis" // overrides pipeline level NAME env variable
                BUILD_ID = "2" // overrides the default BUILD_ID
            }

            steps {
                echo "SHOOL = ${env.SHOOL}" // prints "SHOOL = bar"
                echo "NAME = ${env.NAME}" // prints "NAME = lewis"
                echo "BUILD_ID = ${env.BUILD_ID}" // prints "BUILD_ID = 2"

                script {
                    env.SOMETHING = "1" // creates env.SOMETHING variable
                }
            }
        }

        stage("Override Variables") {
            steps {
                script {
                    env.SHOOL = "I LOVE DATASCIENTEST!" // it can't override env.SHOOL declared at the pipeline (or stage) level
                    env.SOMETHING = "2" // it can override env variable created imperatively
                }

                echo "SHOOL = ${env.SHOOL}" // prints "SHOOL = bar"
                echo "SOMETHING = ${env.SOMETHING}" // prints "SOMETHING = 2"

                withEnv(["SHOOL=DEV UNIVERSITY"]) { // it can override any env variable
                    echo "SHOOL = ${env.SHOOL}" // prints "SHOOL = DEV UNIVERSITY"
                }

                withEnv(["BUILD_ID=1"]) {
                    echo "BUILD_ID = ${env.BUILD_ID}" // prints "BUILD_ID = 1"
                }
            }
        }
    }
}