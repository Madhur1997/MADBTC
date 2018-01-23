### Basic Terminology

1. Images :  
The blueprints of our application which form the basis of containers. In the demo above, we used the docker pull command to download the busybox image.
2. Containers :  
Created from Docker images and run the actual application. We create a container using docker run which we did using the busybox image that we downloaded. A list of running containers can be seen using the docker ps command.
3. Docker Daemon :  
The background service running on the host that manages building, running and distributing Docker containers. The daemon is the process that runs in the operating system to which clients talk to.
4. Docker Client :  
The command line tool that allows the user to interact with the daemon. More generally, there can be other forms of clients too - such as Kitematic which provide a GUI to the users.
5. Docker Hub :  
A registry of Docker images. You can think of the registry as a directory of all available Docker images. If required, one can host their own Docker registries and can use them for pulling images.

### Basic Commands

1. docker pull   
obtains images or a repository from a registry

2. docker run   
* runs a command in a new container
* **docker run will automatically pull an image from the registry if not already present**

* docker run -it #containername sh  
runs an interactive shell, means you can give multiple commands

3. docker ps  
list all active containers

* ps -a : displays history of active containers  


4. Deleting containers

* Single container
```bash
docker rm #containerid
```
* All historical containers :  
```bash
$ docker rm $(docker ps -a -q -f status=exited)
```

5. Deploying web apps in docker Containers

```bash
$ docker run -d -P --name static-site prakhar1989/static-site
```
flag -d : means detach, so we can close the terminal and the container will run in the background.  
To shutdown the detached container use :  
```bash
docker stop #containerid
```

To map specific ports to the container ports
```bash
$ docker run -p 8888:80 prakhar1989/static-site
```
