from itertools import count
from kubernetes import client, config
from kubernetes.stream import stream
import socket
import os
import time

try:
    print("- Loading k8s config")
    # Configs can be set in Configuration class directly or using helper utility
    config.load_incluster_config()
    # config.load_kube_config()
    v1 = client.CoreV1Api()

    ## Mongo Section ##
    print("- Searching for mongodb-replica-0")
    busybox_name = socket.gethostname()
    namespace = os.getenv('NAMESPACE')
    # mongo_ns="memphis2"
    mongo_primary_pod_name = "mongodb-replica-0"
    mongo_secondary_pod_name = "mongodb-replica-1"
    counter_arr = [0,0]
    while counter_arr[0] != 1 and counter_arr[1] != 1:
        ret2 = v1.list_namespaced_pod(namespace)
        for i in ret2.items:
            if(i.metadata.name == mongo_primary_pod_name and i.status.phase == "Running"):
                counter_arr[0] = 1
            if(i.metadata.name == mongo_secondary_pod_name and i.status.phase == "Running"):
                counter_arr[1] = 1
    print("- Both replicas are up")
    print("- Starting to configure mongodb")
except v1 as e:
    print("Error: %s\n" % e)
try:
    exec_command = [
            '/bin/sh',
            '-c',
            'mongo < /mnt/scripts/mongo-startup-script.sh']
    while True:
        resp = stream(v1.connect_get_namespaced_pod_exec,
                        mongo_primary_pod_name,
                        namespace,
                        command=exec_command,
                        stderr=True, stdin=True,
                        stdout=True, tty=False)
        print("- Response: " + resp)
        break
except v1 as e:
    print("Error: %s\n" % e)

try:
    print("- Done. Sleeping")
except:
    print("Error")
