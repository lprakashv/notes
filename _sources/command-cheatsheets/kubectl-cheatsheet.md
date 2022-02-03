# Kubectl Cheat Sheet

## Creating Resource

| Description | Command |
|-|-|
| With YAML resource definition file  |  __kubectl create -f resource-def-file.yaml__                 |
| With command line details           | __kubectl create [TYPE] [NAME] --[additional details=value]__ |

## Getting resource

```bash
kubectl get [TYPE] [NAME]
```

Getting "all" resources

```bash
kubectl get all
```

## Describing resource

```bash
kubectl describe [TYPE] [NAME]
```

## Deleting resource

```bash
kubectl delete [TYPE] [NAME]
```

## Formatting output

Usage: __kubectl [command] [TYPE] [NAME] -o \<output-format\>__

- `-o json` output JSON formatted API object
- `-o name` output only name of the resource
- `-o wide` output in plaintext format with additional information
- `-o yaml` output YAML formatted object

Examples:

```bash
kubectl create namespace test-123 --dry-run -o json

kubectl create namespace test-123 --dry-run -o yaml

# Wide
kubectl get pods -o wide
```

## Imperative Commands (Single command to create resources)

| Task | Command |
|-|-|
| __Create Pod__ | `kubectl run nginx --image=nginx`
| __Create Pod Manifest YAML (-o yaml), don't create (--dry-run)__ | `kubectl run nginx --image=nginx --dry-run=client -o yaml` |
| __Create Deployment__ | `kubectl create deployment nginx --image=nginx --replicas=4` |
| __Create Deployment Manifest YAML (-o yaml), don't create (--dry-run)__ | `kubectl create deployment nginx --image=nginx --replicas=4 --dry-run=client -o yaml` |
| __Generate a YAML file out of YAML manifests__ | `[kubectl-command] -o yaml > manifest.yaml` |
| __Creating a Service - 1__ | `kubectl expose pod redis --port=6379 --name redis-service --dry-run=client -o yaml` |
| __Creating a Service - 2__ (this will not use pods label as selector, instead assume selector as __app=redis__) | `kubectl create service clusterip redis --tcp=6379:6379 --dry-run=client -o yaml` |
| __Creating NodePort Service to expose pod nginx's port 80 on port 30080 on the nodes__ | `kubectl expose pod nginx --port=80 --name nginx-service --type=NodePort --dry-run=client -o yaml` |
| __NodePort 2__ | `kubectl create service nodeport nginx --tcp=80:80 --node-port=30080 --dry-run=client -o yaml` |
