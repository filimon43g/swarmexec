import os
import sys
from swarm_cluster import SwarmCluster
from configparser import ConfigParser

usage = "swarmexec <service_name> <command>"
config_file = 'swarm_config.ini'

def main():
    if len(sys.argv) > 2:
        docker_host = os.environ['DOCKER_HOST']
        service_name = sys.argv[1]
        cmd = sys.argv[2:]

        nodes_mapping = {}
        if os.path.exists(config_file):
            config = ConfigParser()
            config.read(config_file)
            if 'nodes_mapping' in config:
                nodes_mapping = config['nodes_mapping']

        cluster = SwarmCluster(base_url=docker_host, nodes_mapping=nodes_mapping)
        cluster.exec(service_name, cmd)
    else:
        print(usage)


if __name__ == "__main__":
    main()