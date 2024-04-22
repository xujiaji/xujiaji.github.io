pipeline {
    agent any

    tools {
        nodejs 'nodejs21.7.3'
    }

    stages {
        stage('准备环境') {
            steps {
                sh "npm install hexo-cli -g"
                sh "npm install hexo@6.3.0"
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
                sh "cp -rf ../../tools/ssh/id_rsa.xu blog"
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
        stage('部署静态资源') {
            steps {
                dir('./blog') {
                    sh 'ossutil cp -r public/api oss://xujiaji/blog/api/ -f -c "~/.ossutilconfig"'
                    sh 'ossutil cp -r public oss://xujiaji/blog/statics/ -f --include "*.js" --include "*.css" -c "~/.ossutilconfig"'
                }
            }
        }
        stage('部署到服务器') {
            agent {
                docker {
                    image 'python:3.12.1-alpine3.19'
                    args '-u root --privileged'
                    reuseNode true
                }
            }
            steps {
                dir('./blog') {
                    sh "pip install Fabric3"
                    replaceAllInFile("from collections import Mapping", "from collections.abc import Mapping", "/usr/local/lib/python3.12/site-packages/fabric/main.py")
                    replaceAllInFile("from collections import Mapping", "from collections.abc import Mapping", "/usr/local/lib/python3.12/collections/__init__.py")
                    sh "fab deploy"
                    sh "rm -rf __pycache__"
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

// 替换文件中的字符串
def replaceAllInFile(String oldStr, String newStr, String file) {
    sh """
    sed -i "s/${oldStr}/${newStr}/g" ${file}
    """
}
