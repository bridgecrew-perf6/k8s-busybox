def imageName = "k8s-busybox"
def containerName = "k8s-busybox"
def gitURL = "git@github.com:Memphis-OS/k8s-busybox.git"
def gitBranch = "staging"
def repoUrlPrefix = "memphisos"
unique_Id = UUID.randomUUID().toString()
def namespace = "memphis"
def DOCKERHUB_CREDENTIALS=credentials('docker-hub')

node {
  try{
    stage('SCM checkout') {
        git credentialsId: 'main-github', url: gitURL, branch: gitBranch
    }

    stage('Docker hub login') {
      sh 'docker login -u $DOCKERHUB_CREDENTIALS_USR -p $DOCKERHUB_CREDENTIALS_PSW'
    }

    stage('Build docker image') {
        sh "docker build -t ${repoUrlPrefix}/${imageName} ."
    }

    stage('Push docker image') {
        sh "docker push ${repoUrlPrefix}/${imageName}:${unique_Id}"
        sh "docker push ${repoUrlPrefix}/${imageName}:latest"
        sh "docker image rm ${repoUrlPrefix}/${imageName}:latest"
        sh "docker image rm ${repoUrlPrefix}/${imageName}:${unique_Id}"
    }
    
    stage('Push image to kubernetes') {
	    sh "kubectl --kubeconfig=\"/var/lib/jenkins/.kube/memphis-staging-kubeconfig.yaml\" set image deployment/${containerName} ${containerName}=${repoUrlPrefix}/${imageName}:${unique_Id} -n ${namespace}"
    }
    notifySuccessful()

  } catch (e) {
      currentBuild.result = "FAILED"
      notifyFailed()
      throw e
  }
}

def notifySuccessful() {
  emailext (
      subject: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
      body: """<p>SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
        <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""",
      recipientProviders: [[$class: 'DevelopersRecipientProvider']]
    )
}

def notifyFailed() {
  emailext (
      subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
      body: """<p>FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
        <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""",
      recipientProviders: [[$class: 'DevelopersRecipientProvider']]
    )
}
