# K8S相关
## Pod相关

**Pod** 是一组一个或多个容器，它们共享同一个网络命名空间、存储卷以及其他资源。通常，**Pod 中的容器是紧密耦合的**，它们一起工作，共享资源，通常是为了实现一个完整的业务功能。示例：一个nginx和一个python Server（2个容器环境里）组成一个完整业务服务，那么一个Pod就是这2个容器，对应的**Pod配置**可以如下：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app-pod
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
  - name: python-server
    image: python:3.9
    command: ["python", "server.py"]
    ports:
    - containerPort: 5000
```

**这种方式的好处**

1. **网络共享**：nginx 可以通过 `localhost` 或 `127.0.0.1` 直接访问 Python server，无需暴露外部 IP 或端口。
2. **资源共享**：如果你需要存储文件或缓存，你可以将共享的存储卷挂载到这两个容器中。
3. **同生命周期管理**：nginx 和 Python server 容器的生命周期是一起管理的，便于协调启动、停止等操作。



**Pod小知识**

1. 展示所有Pods：kubectl get pods [-n {namespace}]
2. 查看单个pod详细信息：kubectl describe pod {pod-name}
3. 查看日志：kubectl logs {pod-name} [-c {container-name}]
4. 进入单个pods：kubectl exec -it {pod-name} [-c {container-name}] -- /bin/bash



### 健康检查

- livenessProbe
- readinessProbe



# 各类层级相关

**1 Service → 1-n Deployment/Pod**

- 一个 **Service** 可以暴露一个或多个 **Deployment**。
- **Service** 的作用是将流量引导到符合特定标签的 Pod 上，而这些 Pod 是由 **Deployment** 管理的。
- 在实践中，**Service** 经常指向多个 **Deployment**，特别是当你有不同类型的服务（例如 Web 服务、API 服务等）时，Service 会暴露多个应用。

**1 Deployment → 1-n Pod**

- 一个 **Deployment** 负责管理多个 **Pod** 副本。部署时，你可以通过 **Deployment** 定义期望的 Pod 副本数量。
- **Deployment** 会根据需要自动创建、更新、扩展或删除 Pod 副本，确保应用始终以正确的副本数运行。



## Pod相关

🔍 查看 Pod 状态

```bash

kubectl get pods
kubectl get pods -n <namespace>                # 指定命名空间
kubectl get pods -o wide                       # 显示更多信息（如 IP、节点）
```

------

📖 查看 Pod 详细信息

```bash

kubectl describe pod <pod-name>
kubectl describe pod <pod-name> -n <namespace>
```

通过Deployment的label获取pods

```
kubectl get deployment XXX -o yaml |grep -A 10 matchLabels
    matchLabels:
      example1: value1
      example2: value2

kubectl get pods -l example1=value1,example2=value2
```

------

📦 查看 Pod 日志

```bash

kubectl logs <pod-name>
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -c <container-name>     # Pod 中有多个容器时
kubectl logs -f <pod-name>                      # 实时跟踪日志
```

------

🐛 进入 Pod 内部（调试容器）

```bash

kubectl exec -it <pod-name> -- /bin/bash
kubectl exec -it <pod-name> -c <container-name> -- /bin/sh
```

------

🚨 排查 CrashLoopBackOff 或 Pending 的 Pod

```bash

kubectl get events --sort-by='.metadata.creationTimestamp'
kubectl describe pod <pod-name>                # 查看失败原因
```

------

🛠️ 创建 Pod（测试用）

```bash
# 示例1
kubectl run test-pod --image=nginx --restart=Never

# 示例2
kubectl run tmp-demo --image=nginx --restart=Never --port=8080 --command -- sleep 300d
```

------

🧹 删除 Pod

```bash

kubectl delete pod <pod-name>
kubectl delete pod <pod-name> -n <namespace>
```

------

🧪 检查 Pod 就绪状态

```bash

kubectl get pods -w                             # 实时观察 Ready 状态
```

------

🔁 重启 Deployment（间接重启 Pod）

```bash

kubectl rollout restart deployment <deployment-name>
```

端口转发

```bash
# 转发单个pod的端口
kubectl port-forward pod/<pod-name> <local-port>:<pod-port>
i.e. kubectl port-forward pod/myapp-pod 8080:80

# 转发Service的端口
kubectl port-forward service/<service-name> <local-port>:<target-port>
i.e. kubectl port-forward service/myapp-svc 8080:80
```



## depolyment相关

📦 查看 Deployment 列表

```bash

kubectl get deployments
kubectl get deployments -n <namespace>
kubectl get deploy -o wide
```

------

🔍 查看 Deployment 详情

```bash

kubectl describe deployment <deployment-name>
kubectl describe deploy <deployment-name> -n <namespace>
```

------

🔄 更新 Deployment（推荐方式）

例如：更新镜像

```bash

kubectl set image deployment/<deployment-name> <container-name>=<new-image>
# 例：
kubectl set image deployment/nginx-deploy nginx=nginx:1.21
```

------

💥 强制重启 Deployment（通常用于热更新配置）

```bash

kubectl rollout restart deployment <deployment-name>
```

------

🔁 回滚 Deployment

查看历史版本：

```bash

kubectl rollout history deployment <deployment-name>
```

回滚到上一个版本：

```bash

kubectl rollout undo deployment <deployment-name>
```

指定版本回滚：

```bash

kubectl rollout undo deployment <deployment-name> --to-revision=<number>
```

------

👀 查看滚动更新状态

```bash

kubectl rollout status deployment <deployment-name>
```

------

🧹 删除 Deployment

```bash

kubectl delete deployment <deployment-name>
```

------

🛠 创建 Deployment（快速方式）

```bash

kubectl create deployment myapp --image=nginx
```

------

✍️ 使用 YAML 部署/更新 Deployment

```bash

kubectl apply -f deployment.yaml
```

------

🚥 调整副本数（scale）

```bash

kubectl scale deployment <deployment-name> --replicas=3
```



## helem chart 相关/helm相关

前言：helem chart是用来做服务部署的历史记录，让每次的更新都能够被追溯，同时有一个统一的地方维护部署的所有配置，如资源quota、镜像版本、启停和健康检查的定义等。下方通过单个示例，来做部署的演示

**文件结构如下**

```bash
tree ./K8S_config/aws_helem_chart
./K8S_config/aws_helem_chart
├── Chart.yaml
├── templates
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── ingress.yaml
│   └── service.yaml
└── values.yaml

1 directory, 6 files
```

﻿**基础概念**

- release：helm中首先是release的概念，可以认为是某个环境下的一套服务部署，如一套pod-deployment-service-ingress组成的服务



**服务安装**

```bash
$ helm install test-app-1 ./K8S_config/aws_helem_chart -f K8S_config/aws_helem_chart/values.yaml
```

**通过文件生成各类部署yaml**

```bash
helm template test-app-1 ./K8S_config/aws_helem_chart -f K8S_config/aws_helem_chart/values.yaml > test-app-5.yaml
```

﻿**查看服务**

```
helm get manifest test-app-1 | cat
```

**验证服务是否存在**

```bash
$ kubectl get all -l app.kubernetes.io/instance=test-app-1
﻿
NAME                                                      READY   STATUS    RESTARTS   AGE
pod/test-app-1-apolloviz-dataserver-7f68d46764-rm7kr   1/1     Running   0          39m
﻿
NAME                                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/test-app-1-apolloviz-dataserver   ClusterIP   10.100.77.200   <none>        8111/TCP   39m
﻿
NAME                                                 READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/test-app-1-apolloviz-dataserver   1/1     1            1           39m
﻿
NAME                                                            DESIRED   CURRENT   READY   AGE
replicaset.apps/test-app-1-apolloviz-dataserver-7f68d46764   1         1         1       39m
```

﻿

**更新部署（需要更改配置文件后）**

```bash
$ helm upgrade test-app-1 ./K8S_config/aws_helem_chart -f K8S_config/aws_helem_chart/values.yaml
Release "test-app-1" has been upgraded. Happy Helming!
NAME: test-app-1
LAST DEPLOYED: Fri Apr 18 15:17:08 2025
NAMESPACE: default
STATUS: deployed
REVISION: 2
TEST SUITE: None
```

﻿

**查看部署历史记录**

```bash
$ helm history test-app-1
REVISION    UPDATED                     STATUS        CHART                         APP VERSION    DESCRIPTION
1           Fri Apr 18 14:29:47 2025    superseded    apolloviz-dataserver-0.1.0    1.0.0          Install complete
2           Fri Apr 18 15:17:08 2025    deployed      apolloviz-dataserver-0.1.0    1.0.0          Upgrade complete
```

﻿

**回滚到指定部署记录上**

```bash
$ helm rollback test-app-viz5 1
```