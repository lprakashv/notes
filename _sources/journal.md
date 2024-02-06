# Work Learnings Journal (Appended to each topic section)

## Kubernetes
  
- `initContainers` (for `DaemonSet`) - step by step short lived containers, can be used to fixing privileges and setup tasks
- Kubernetes hostPath ownership are set based on kubelet's
- Kubernetes pod logs are stored under `/var/log/containers/<pod-name>*<container-id>/*.log` (by container runtime)

## Linux

- list users : `/etc/passwd`
- list groups : `/etc/group`
- members of group : `lid <group-name>`
- owning directory (recursively) `chown -R <uid>:<gid> <dir-path>`

## Go

- `go mod init <current-module-name>` - initializing module for a new app/project
- `go get <dep-name>` - install dependencies manually
- Makefile general target structure

  ```makefile
  target : dependency1 dependency2
  recipe-command1
  recipe-command2
  ```

- Makefile forcefully run without checking dependency build

  ```makefile
  .PHONY all: clean build coverage run
  ```

  it does not matter if any of the above dependencies are unsatisfied/failed, the whole command will still forcefully be executed

## TODOs

- Linux Services - sigterm, sigkill
- AWS - ECS - EC2 (setup), ECS Fargate, ELB, VPC
- k8s - resource limits vs requests
- go - build flags (and commented tags etc.), cgo, select, channels concurrency etc.
- docker - host specific builds, golang-crossbuild
- python - pipenv, venv
- OAuth2
- TLS, mTLS
- HTTP2, gRPC

## Yearly Learning Journal

TODO

### 2024

TODO

### 2023

TODO

### 2022

TODO

### 2021

TODO

### 2020

TODO

### 2019

TODO
