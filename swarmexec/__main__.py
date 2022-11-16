import os
import sys
from swarmexec.swarm_cluster import SwarmCluster
from swarmexec.swarm_host import validate_ssh_connection_string, SwarmHost
from configparser import ConfigParser
import argparse

usage = "swarmexec <service_name> <command>"
config_file = 'swarm_config.ini'

def get_args():
    ap = argparse.ArgumentParser(prog="swarmexec", description="Execute command on swarm services")
    ap.add_argument("-H", "--host", type=validate_ssh_connection_string, help="Swarm ssh host")
    ap.add_argument('service', nargs=1, help='service name')
    ap.add_argument('cmd', nargs=argparse.REMAINDER, help='command to run')
    return ap.parse_args()

def get_docker_host(args):
    if args['host']:
        docker_host = args['host']
    else:
        docker_host = os.environ.get('DOCKER_HOST')
    if docker_host:
        return SwarmHost(docker_host)


def main():
    args = vars(get_args())
    docker_host = get_docker_host(args)

    if docker_host and args['service'] and args['cmd']:
        service_name = args['service']
        cmd = " ".join(args['cmd'])

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