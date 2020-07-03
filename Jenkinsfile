pipeline {
    agent {
        docker { image 'convisoappsec/flowcli' }
    }
    environment {
        FLOW_API_KEY    = credentials('FLOW_API_KEY')
        FLOW_API_URL    = 'https://homologa.conviso.com.br'
    }
    stages {
        stage('Help') {
            steps {
                sh 'printenv'
                sh 'ls -ltrah $WORKSPACE'
                sh 'echo $USER'
                sh 'flow analysis sast --no-send-to-flow -r $WORKSPACE'
            }
        }
    }
}
