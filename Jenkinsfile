pipeline {
    agent {
        docker { image 'docker:dind' }
    }
    environment {
        FLOW_API_KEY    = credentials('FLOW_API_KEY')
        FLOW_PROJECT_ID = 'llIOLZ8b_RqDdOfq'
        ECR_TOKEN_URL   = 'https://homologa.conviso.com.br/auth/sast'
        REGISTRY_URL    = 'docker.convisoappsec.com/sastbox'
    }

    stages {
        stage('SAST') {
            steps {
                sh 'apk add curl'
                sh 'curl -X GET $ECR_TOKEN_URL -H "X-API-Key: $FLOW_API_KEY" -o auth_token.txt'
                sh 'cat auth_token.txt | docker login $REGISTRY_URL -u AWS --password-stdin'
                sh 'docker pull $REGISTRY_URL'
                sh 'docker run -v $CI_PROJECT_DIR:/code -e FLOW_PROJECT_ID -e FLOW_API_KEY -e OLD_COMMIT --rm --entrypoint=./scandiff $REGISTRY_URL:latest'
                sh 'docker logout $REGISTRY_URL'
            }
        }
    }
}