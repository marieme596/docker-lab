# Deploy and run a simple flask backend with Kubernetes

## Prerequisites
- install [kubectl](https://kubernetes.io/releases/download/)
- install [minikube](https://kubernetes.io/fr/docs/tasks/tools/install-minikube/)

## Initiate a cluster with minikube
Here we will initiate a Kubernetes cluster with **three nodes** using **Docker** as the driver. Those nodes will host **replicas** of the backend.
```
minikube start --nodes 3 --driver=docker
```

## Deploying app
1. First, we apply all the manifests files to the cluster. If those files are in k8s/ directory, then we run :
```
kubectl apply -f k8s/
```
2. We can verify if the pods are running with the command :
```
kubectl get pods
```
3. To view more details and events about a specific pod or the reasons of the current pod status, we can use :
```
kubectl describe pod <pod-name>
```
Replace `pod-name` with the name of the pod you want to see the details.

**This command is useful for debugging running issues with pods.**

## Accessing app
1. Show all the services with the following command :
```
kubectl get services
```
2. When deployed in minikube, a Kubernetes service configured with **NodePort** can be accessed easily by running :
```
minikube service <service-name> --url
```
Replace `service-name` with the name of the service you want to access.
This command create a temporary URL that you can access via your browser to test or interact with the service.

3. It is possible to establish a connection between your local machine and a pod and test the API instead of testing it with the service. For that, we run the command :
```
kubectl port-forward <pod-name> 5000:5000
```
Replace `pod-name` with the name of the pod you want to access.
After running this previous command, we can open another terminal and test the API using `curl` or use an API platform as **Postman**.

N.B: **5000** is the port where the API is exposed.

## Debugging app
1. Monitoring logs from a specific container within a pod :
```
kubectl logs <pod-name> -c <container-name>
```
Replace `pod-name` and `container-name` respectively with the name of the pod you want to see the logs and the container within the pod.

2. Health checks
Testing the liveness and readiness manually is a good way of debugging problems with the database connection to the API.
- To check `liveness`, use the following command :
```
kubectl exec <pod-name> -- curl -I http://localhost:5000/health/live
```
- To check `readiness`, use the following :
```
kubectl exec <pod-name> -- curl -I http://localhost:5000/health/ready
```
Replace `pod-name` with the name of the pod you want to access.

N.B: **5000** is the port where the API is exposed.

3. Minikube provides a dashboard which is a graphical interface for managing and monitoring Kubernetes resources locally. It is very useful to determine quickly issues when running pods. To launch it and open it in a browser, use this command :
```
minikube dashboard
```

## Cleaning Up
When finished, we release the resources and delete the minikube cluster by running the commands :
```
minikube stop
minikube delete
```