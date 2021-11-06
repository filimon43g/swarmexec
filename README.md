# Swarmexec
swarmexec executes command in swarm service

## Install
```
pip install git+https://github.com/filimon43g/swarmexec.git
```

## Usage
```
In swarm_config.ini map your node host names with public hostnames or nodes IPs if neccessery. 
```

### Run command
```
export DOCKER_HOST=ssh://<manager node hostname>
swarmexec <service_name> <command>
```
