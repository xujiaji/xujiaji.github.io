pipeline {
    agent any

    tools {
        nodejs 'nodejs18.19.0'
    }

    stages {
        stage('准备环境') {
            steps {
                trySh "npm install hexo-cli -g"
                trySh "hexo init blog"
                trySh "rm -rf blog/source"
                trySh "find * -type f -not -name '.gitignore' -not -name 'JenkinsFile' -exec cp {} 'blog/source' \\;"
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
