pipeline {
    agent any

    tools {
        nodejs 'nodejs21.7.3'
    }

    stages {
        stage('准备环境') {
            steps {
                trySh "npm install hexo-cli@4.3.1 -g"
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
                    sh "npm install babel-core babel-preset-env html-minifier terser cheerio jasmine hexo-deployer-git hexo-filter-mathjax-ssr hexo-generator-feed hexo-renderer-markdown-it html-to-text markdown-it markdown-it-container markdown-it-footnote --save"
                }
            }
        }
        stage('构建') {
            steps {
                dir('./blog') {
                    sh "hexo clean && hexo g"
                }
            }
        }
        stage('部署') {
            agent {
                docker {
                    image 'python:3.12.1-alpine3.19'
                    reuseNode true
                }
            }
            steps {
                dir('./blog') {
                    sh "python -V"
                    sh "pip install Fabric3"
                    sh 'ossutil cp -r public/api oss://xujiaji/blog/api/ -f -c "~/.ossutilconfig"'
                    sh 'ossutil cp -r public oss://xujiaji/blog/statics/ -f --include "*.js" --include "*.css" -c "~/.ossutilconfig"'
                    sh "fab deploy"
                }
            }
        }
    }
}

def trySh(shtext) {
    try {
        sh shtext
    } catch(e) {
       throw e
    }
}
