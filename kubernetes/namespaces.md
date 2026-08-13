# Kubernetes Namespaces

- __Isolation__ - provides isolation among different groups, e.g., prod, dev, team1, team2.
- __Resource Limits__ - we can put resource limits (memory. cpu, disk) on each "groups" / namespaces.
- __Policies__ - we can put certain policies for each "groups" / namespaces.
- __DNS__ - simplified name resolution, e.g. `mysql.connect("db-service")`, `mysql.connect("db-service.dev.svc.cluster.local")`.

DNS explained for: __"db-service.dev.svc.cluster.local"__

| "db-service" | "dev" | "svc" | "cluster.local" |
|-|-|-|-|
| service name | namespace | __Service__ | domain |

## Standard namespaces

- __default__
- kube-system
- kube-public

## Namespaces Resources

YAML:

```yaml
apiVersion: ...
kind: ...
metadata:
  name: ...
  namespace: ns-name
  labels:
    ...
spec:
  ...
```

Command: __`kubectl [command] [TYPE] [NAME] [--additional-options=value] --namespace=ns-name`__

Getting Resources in all namespaces:

```bash
kubectl get [TYPE] [NAME] --all-namespaces
```

## Switching to Namespace

```bash
kubectl config set-context $(kubectl config current-context) --namespace=new-ns
```

## ResourceQuota

For putting limitations on the resources in a namespace

compute-quota.yaml

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: dev
spec:
  hard:
    pods: "10"
    requests.cpu: "4"
    requests.memory: 5Gi
    limits.cpu: "10"
    limits.memory: 10Gi
```
