# Swarmexec
swarmexec executes command in swarm service

## Install
```
pip install git+https://github.com/filimon43g/swarmexec.git
```

## Config

### On the local machine
```
In swarm_config.ini map your node host names with public hostnames or nodes IPs if neccessery. 
```

### On all swarm nodes
#### Put ssh keys and add your user to the docker group 
```
ssh username@node1.example
mkdir .ssh
echo "YOUR PUB SSH KEY" > .ssh/authorized_keys
chmod 700 .ssh
chmod 600 .ssh/authorized_keys 
sudo gpasswd -a username docker
```

How to create ssh keys http://linuxproblem.org/art_9.html

## Usage
```
export DOCKER_HOST=ssh://<manager node hostname>
swarmexec <service_name> <command>
```
or
```
swarmexec --hostname username@<manager node hostname> <command>
```

## Examples
```
swarmexec --hostname username@example.com nginx_proxy "ls -l /"
```
```
swarmexec --hostname username@example.com nginx_proxy bash
```
