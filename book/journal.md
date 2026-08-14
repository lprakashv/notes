# Work Learnings Journal

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

### 2024

- TLS

### 2023

- AWS Kinesis Firehose - buffering, processor lambda (lambda buffering), output, intput (kinesis data streams, direct put), failure etc.
- AWS Cloudformation - custom event, constants, conditions, roles, resources, output, parameters, custom lambda (init processing)
- AWS S3 events - triggering Lambdas
- Lambda - cloudwatch loggroup, logstream, event, timeout, cost calc, cold-start and lambda (container) level caching.
- Eventbridge rules and schedules
- AWS VPC and Subnets
- AWS Secrets Manager
- Linux packages - deb, rpm
- Oauth2
- AWS ECS (EC2) - cluster bootstrapping (joining), task-def, service, task, daemon, execution role, volumes and mounts
- AWS EFS
- Docker - inspects contents, download files from containers, live debugging and inspection
- Wrapping executor application with piping STDOUT output and taking input
- Go - Cobra, flag, options etc.

### 2022

- Kubernetes (kubectl), Daemonset, ConfigMap, Service, Deployment, ServiceAccount, ClusterRole, ClusterRoleBindings
- Kubernetes Operators (pattern), Go Operator SDK
- Go, Go string templates
- Helm charts, Helm templates, Helm repos
- Kubectx
- OTel protocol, SDK - logs, metrics
- OTel collector - receivers (otlp, filelog), exporters (otlp, logging, prometheus), processors (batch, resourcedetection, attribute), extensions
- OpAMP protocol, SDK - client, server, deployment patterns
- Elastic Filebeat

### 2021

- Java Agents, Java Instrumentation, Java Bytecode Injection
- Java Vertx framework internals
- Java remote debugging, conditional breakpoints, thread debugging
- Angular, RxJS, Typescript, Jest

### 2020

- React, Redux

### 2019

- Spring Boot, Spring Batch, Spring-Kafka, Spring Data JPA, Spring Data JDBC, Kafka Consumers
- Apache Camel (pipelines) with Kafka, batch etc.
- Oracle, MS SQL Server, Stored Procedures
- Apache Livy
- Maven
