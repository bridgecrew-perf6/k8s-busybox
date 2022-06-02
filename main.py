# Copyright 2021-2022 The Memphis Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

    ## Mongo Section ##
    print("- Searching for mongodb-0")
    busybox_name = socket.gethostname()
    namespace = os.getenv('NAMESPACE')
    mongo_primary_pod_name = "mongodb-0"
    mongo_secondary_pod_name = "mongodb-1"
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
