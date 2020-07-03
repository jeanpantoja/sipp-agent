pipeline {
    agent {
        docker { 
            image 'convisoappsec/flowcli' 
            args '-u root -v /var/run/docker.sock:/var/run/docker.sock'
        }
        
    }
    environment {
        FLOW_API_KEY    = credentials('FLOW_API_KEY')
        FLOW_API_URL    = 'https://homologa.conviso.com.br'
        FLOW_PROJECT_CODE = '8qE3Q2w9C6qHGtGt'
    }
    stages {
        stage('Help') {
            steps {
                sh 'printenv'
                sh 'ls -ltrah $WORKSPACE'
                sh 'echo $USER'
                sh 'flow sast run'
            }
        }
    }
}
