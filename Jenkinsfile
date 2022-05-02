def imageName = "k8s-busybox"
def containerName = "k8s-busybox"
def gitURL = "git@github.com:Memphis-OS/k8s-busybox.git"
def gitBranch = "master"
def repoUrlPrefix = "memphisos"
unique_Id = UUID.randomUUID().toString()
def namespace = "memphis"

pipeline {
    agent any
    environment {
      DOCKERHUB_CREDENTIALS=credentials('docker-hub')
    }
    stages{
      stage('SCM checkout') {
        steps{
          git credentialsId: 'main-github', url: gitURL, branch: gitBranch
        }
      }

      stage('Docker hub login') {
        steps{
          sh("docker login -u $DOCKERHUB_CREDENTIALS_USR -p $DOCKERHUB_CREDENTIALS_PSW")
        }
      }

      stage('Build docker image') {
        steps{
          sh("docker build -t ${repoUrlPrefix}/${imageName} .")
        }
      }

      stage('Push docker image') {
        steps{
          sh("docker tag ${repoUrlPrefix}/${imageName} ${repoUrlPrefix}/${imageName}:${unique_Id}")
          sh("docker push ${repoUrlPrefix}/${imageName}:${unique_Id}")
          sh("docker push ${repoUrlPrefix}/${imageName}:latest")
          sh("docker image rm ${repoUrlPrefix}/${imageName}:latest")
          sh("docker image rm ${repoUrlPrefix}/${imageName}:${unique_Id}")
        }
      }
      
      stage('Push image to kubernetes') {
        steps{
          sh "kubectl --kubeconfig=\"/var/lib/jenkins/.kube/memphis-staging-kubeconfig.yaml\" set image deployment/${containerName} ${containerName}=${repoUrlPrefix}/${imageName}:${unique_Id} -n ${namespace}"
        }
      }
    }
}