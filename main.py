from itertools import count
from kubernetes import client, config
from kubernetes.stream import stream
import socket
import os
try:
    print("- Loading k8s config")
    # Configs can be set in Configuration class directly or using helper utility
    config.load_incluster_config()
    # config.load_kube_config()
    v1 = client.CoreV1Api()
    print("- Searching for mongodb-replica-0")
    busybox_name = socket.gethostname()
    namespace = os.getenv('NAMESPACE')
    print(namespace)
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
except:
    print("Error 1")
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

        resp = v1.read_namespaced_config_map(
                    name="memphis-broker-config", namespace='memphis-staging')
        print(resp.data)
        break
except:
    print("Error 2")
try:
    response = v1.delete_namespaced_pod(busybox_name, namespace)
    print(response)
except v1 as e:
    print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)
print("- Done")