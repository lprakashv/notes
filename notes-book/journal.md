# Work Learnings Journal

## 19-10-2022

- Kubernetes:
  - `initContainers` (for `DaemonSet`) - step by step short lived containers, can be used to fixing privileges and setup tasks
- Linux:
  - list users : `/etc/passwd`
  - list groups : `/etc/group`
  - members of group : `lid <group-name>`
  - owning directory (recursively) `chown -R <uid>:<gid> <dir-path>`

## 20-10-2022

- Kubernetes hostPath ownership are set based on kubelet's
- Kubernetes pod logs are stored under `/var/log/containers/<pod-name>*<container-id>/*.log` (by container runtime)

## ... - 13-11-2022

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
