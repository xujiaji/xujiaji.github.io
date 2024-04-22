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
                script {
                    path = sh(returnStdout: true, script: 'pwd').trim()
                }
                trySh "ls ${path} | grep -v Jenkinsfile | grep -v .gitignore | grep -v blog | grep -v node_modules | grep -v .git | grep -v package.json | grep -v package-lock.json | xargs -i cp -r ${path}/{} ${path}/blog/source/"
                sh "cp -rf _config.inside.yml blog"
                sh "cp -rf _config.yml blog"
                sh "cp -rf fabfile.py blog"
                dir('./blog') {
                    sh "npm install hexo-theme-inside"
                    sh "npm install babel-core babel-preset-env html-minifier terser cheerio jasmine --save"
                }
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
