pipeline {
    agent {
        docker { image 'docker:dind-rootless' }
    }
    environment {
        FLOW_API_KEY    = credentials('FLOW_API_KEY')
        FLOW_PROJECT_ID = 'llIOLZ8b_RqDdOfq'
        ECR_TOKEN_URL   = 'https://homologa.conviso.com.br/auth/sast'
        REGISTRY_URL    = 'docker.convisoappsec.com/sastbox'
        ECR_TOKEN       = get_token()
    }

    stages {
        stage('SAST') {
            steps {
                sh 'echo $ECR_TOKEN | docker login $REGISTRY_URL -u AWS --password-stdin'
                sh 'docker pull $REGISTRY_URL'
                sh 'docker run -v $CI_PROJECT_DIR:/code -e FLOW_PROJECT_ID -e FLOW_API_KEY -e OLD_COMMIT --rm --entrypoint=./scandiff $REGISTRY_URL:latest'
                sh 'docker logout $REGISTRY_URL'
            }
        }
    }
}

def get_token() {
    node('master') {
        TOKEN = sh(
            script: "wget --header=\'X-API-Key: $FLOW_API_KEY\' -O auth_token.txt $ECR_TOKEN_URL -q",
            returnStdout: true
        )
    }
}