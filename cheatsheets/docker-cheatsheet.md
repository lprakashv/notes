# Docker cheatsheet

## Docker Registries & Repositories

Login to a Registry

```bash
docker login
docker login localhost:8080
```

Logout from a Registry

```bash
docker logout
docker logout localhost:8080
```

Searching an Image

```bash
docker search nginx
docker search nginx --stars=3 --no-trunc busybox
```

Pulling an Image

```bash
docker pull nginx
docker pull eon01/nginx localhost:5000/myadmin/nginx
```

Pushing an Image

```bash
docker push eon01/nginx
docker push eon01/nginx localhost:5000/myadmin/nginx
```

## Running Containers

Creating a Container

```bash
docker create -t -i eon01/infinite --name infinite
```

Running a Container

```bash
docker run -it --name infinite -d eon01/infinite
```

Renaming a Container

```bash
docker rename infinite infinity
```

Removing a Container

```bash
docker rm infinite
```

Updating a Container

```bash
docker update --cpu-shares 512 -m 300M infinite
```

## Starting & Stopping Containers

Starting

```bash
docker start nginx
```

Stopping

```bash
docker stop nginx
```

Restarting

```bash
docker restart nginx
```

Pausing

```bash
docker pause nginx
```

Unpausing

```bash
docker unpause nginx
```

Blocking a Container

```bash
docker wait nginx
```

Sending a SIGKILL

```bash
docker kill nginx
```

Connecting to an Existing Container

```bash
docker attach nginx
```

## Getting Information about Containers

Running Containers

```bash
docker ps
docker ps -a
```

Container Logs

```bash
docker logs infinite
```

Inspecting Containers

```bash
docker inspect infinite
docker inspect --format '{{ .NetworkSettings.IPAddress }}' $(docker ps -q)
```

Containers Events

```bash
docker events infinite
```

Public Ports

```bash
docker port infinite
```

Running Processes

```bash
docker top infinite
```

Container Resource Usage

```bash
docker stats infinite
```

Inspecting Changes to Files or Directories on a Container's Filesystem

```bash
docker diff infinite
```

## Manipulating Images

Listing Images

```bash
docker images
```

Building Images

```bash
docker build .
docker build github.com/creack/docker-firefox
docker build - < Dockerfile
docker build - < context.tar.gz
docker build -t eon/infinite .
docker build -f myOtherDockerfile .
curl example.com/remote/Dockerfile | docker build -f - .
```

Removing an Image

```bash
docker rmi nginx
```

Loading a Tarred Repository from a File or the Standard Input Stream

```bash
docker load < ubuntu.tar.gz
docker load --input ubuntu.tar
```

Save an Image to a Tar Archive

```bash
docker save busybox > ubuntu.tar
```

Showing the History of an Image

```bash
docker history
```

Creating an Image Fron a Container

```bash
docker commit nginx
```

Tagging an Image

```bash
docker tag nginx eon01/nginx
```

Pushing an Image

```bash
docker push eon01/nginx
```

## Networking

Creating Networks

```bash
docker network create -d overlay MyOverlayNetwork
docker network create -d bridge MyBridgeNetwork
docker network create -d overlay \
  --subnet=192.168.0.0/16 \
  --subnet=192.170.0.0/16 \
  --gateway=192.168.0.100 \
  --gateway=192.170.0.100 \
  --ip-range=192.168.1.0/24 \
  --aux-address="my-router=192.168.1.5" --aux-address="my-switch=192.168.1.6" \
  --aux-address="my-printer=192.170.1.5" --aux-address="my-nas=192.170.1.6" \
  MyOverlayNetwork
```

Removing a Network

```bash
docker network rm MyOverlayNetwork
```

Listing Networks

```bash
docker network ls
```

Getting Information About a Network

```bash
docker network inspect MyOverlayNetwork
```

Connecting a Running Container to a Network

```bash
docker network connect MyOverlayNetwork nginx
```

Connecting a Container to a Network When it Starts

```bash
docker run -it -d --network=MyOverlayNetwork nginx
```

Disconnecting a Container from a Network

```bash
docker network disconnect MyOverlayNetwork nginx
```

## Cleaning Docker

Removing a Running Container

```bash
docker rm nginx
```

Removing a Container and its Volume

```bash
docker rm -v nginx
```

Removing all Exited Containers

```bash
docker rm $(docker ps -a -f status=exited -q)
```

Removing All Stopped Containers

```bash
docker rm `docker ps -a -q`
```

Removing a Docker Image

```bash
docker rmi nginx
```

Removing Dangling Images

```bash
docker rmi $(docker images -f dangling=true -q)
```

Removing all Images

```bash
docker rmi $(docker images -a -q)
```

Stopping & Removing all Containers

```bash
docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q)
```

Removing Dangling Volumes

```bash
docker volume rm $(docker volume ls -f dangling=true -q)
```

## Docker Swarm

Installing Docker Swarm

```bash
curl -ssl https://get.docker.com | bash
```

Initializing the Swarm

```bash
docker swarm init --advertise-addr 192.168.10.1
```

Getting a Worker to Join the Swarm

```bash
docker swarm join-token worker
```

Getting a Manager to Join the Swarm

```bash
docker swarm join-token manager
```

Listing Services

```bash
docker service ls
```

Listing nodes

```bash
docker node ls
```

Creating a Service

```bash
docker service create --name vote -p 8080:80 instavote/vote
```

Listing Swarm Tasks

```bash
docker service ps
```

Scaling a Service

```bash
docker service scale vote=3
```

Updating a Service

```bash
docker service update --image instavote/vote:movies vote
docker service update --force --update-parallelism 1 --update-delay 30s nginx
docker service update --update-parallelism 5--update-delay 2s --image instavote/vote:indent vote
docker service update --limit-cpu 2 nginx
docker service update --replicas=5 nginx
```

## Misc

Run an image in a container with its name

```bash
docker run --rm `docker images --filter reference='*/log-generator' --format '{{.ID}}'`
```

Running a container from an image and open a shell into it with root privileges

```bash
docker run --entrypoint="sh" --user=0 --privileged=true <image>:<tag>
```

Loading image from file

```bash
docker load < Downloads/scratch.tar.gz
```

Running an image with passing a local file as argument (after creating a volume for the file dynamically)

- `-ti` for running bash into the container
- `--rm` for removing container as soon as we exit

```bash
docker run -v /local/file/path/file.txt:/dest/file/path/file.txt -ti --rm some-docker-image:tag arg1 arg2
```

Logging into AWS-ECR to pull docker images

```bash
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin "<account>.dkr.ecr.<region>.amazonaws.com"                          
```

See the contents (file and directories) inside a docker container:

```bash
docker export <container-id> | tar -t
```
