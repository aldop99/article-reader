pipeline {
    agent any
    stages {
        stage ("SCM checkout") {
            steps {
               sshagent(['mykey']) {
                  sh '''
                    ssh azureuser@20.251.50.253
                    ansible-playbook Myplaybook
                    '''
                }
            }
        }
    }
}