pipeline {
    agent any

    tools {
        nodejs 'nodejs18.19.0'
    }

    stages {
        stage('准备环境') {
            steps {
                trySh "npm install hexo-cli -g"
                trySh "rm -rf blog"
                trySh "hexo init blog"
                trySh "rm -rf blog/source && mkdir blog/source"
                String path = sh(returnStdout: true, script: 'pwd').trim()
                trySh "find ${path} -type f -not -name 'Jenkinsfile' -not -name '.gitignore' -not -path '${path}/blog/*' -not -path '${path}/node_modules/*' -exec cp -r {} ${path}/blog/source \\;"
            }
        }
        // stage('构建') {
        //     steps {
        //     }
        // }
        // stage('部署') {
        //     steps {
        //     }
        // }
    }
}

def trySh(shtext) {
    try {
        sh shtext
    } catch(e) {
       throw e
    }
}
