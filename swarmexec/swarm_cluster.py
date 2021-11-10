import docker
import logging
import paramiko
from colorama import Fore
from colorama import Style
import termios
import tty
import socket
import sys
from paramiko.py3compat import u


class SwarmCluster:

    def __init__(self, base_url, nodes_mapping={}) -> None:
        self.client = docker.DockerClient(base_url=base_url)
        self._nodes_mapping = nodes_mapping
        self._find_all_nodes()

    def exec(self, service_name:str, cmd):
        """ Execute command and exit """
        container = self._get_container_by_service_name(service_name)
        if container:
            print(Fore.BLUE + container.labels.get('com.docker.swarm.task.name') + Style.RESET_ALL, end=" > ")
            print(Fore.BLUE + " ".join(cmd) + Style.RESET_ALL, end=" > ")
            exict_code, channel = container.exec_run(
                cmd=cmd,
                stdin=True,
                stdout=True, 
                stderr=True, 
                demux=True, 
                stream=True, 
                socket=True,
                tty=True
                )

            posix_shell(channel)

        else:
            logging.error(f'Could not find running container for service {service_name}')
            exit(1)

    def _get_container_by_service_name(self, service_name:str):
        """ Get connection to container on correct node"""
        for service in self.client.services.list(filters={'name': service_name}):
            for task in service.tasks():
                if task['Status']['State'] == 'running':
                    container_id = task['Status']['ContainerStatus']['ContainerID']
                    node_hostname = self.client.nodes.get(task['NodeID']).attrs['Description']['Hostname']
                    client = docker.DockerClient(base_url=self._get_node_ssh_url(node_hostname))
                    print(Fore.BLUE + node_hostname  + Style.RESET_ALL, end=" > ")
                    return client.containers.get(container_id)

    def _find_all_nodes(self):
        """ Find all nodes and check connection """
        for node in self.client.nodes.list():
            node_hostname = node.attrs['Description']['Hostname']
            if self._nodes_mapping:
                if node_hostname not in self._nodes_mapping:
                    raise Exception(f"Could not find {node_hostname} in node mpping {self._nodes_mapping}")
            try:
                docker.DockerClient(base_url=self._get_node_ssh_url(node_hostname)).ping()
            except paramiko.ssh_exception.PasswordRequiredException:
                logging.error(f"Could not connect to {self._get_node_ssh_url(node_hostname)}")
                logging.error("Please put you public ssh key to the node first, http://linuxproblem.org/art_9.html")
                exit(1)
            except docker.errors.DockerException as de:
                logging.error(de.args)
                logging.error("Have you added the user to the docker group?")
                exit(2)
            except Exception as e:
                logging.error(e.args)
                logging.error(f"Could not connect to {self._get_node_ssh_url(node_hostname)}")
                exit(3)
            
    def _get_node_ssh_url(self, node_hostname):
        if self._nodes_mapping:
            if node_hostname in self._nodes_mapping:
                return "ssh://" + self._nodes_mapping[node_hostname]
        else:
            return "ssh://" + node_hostname


def print_output(output):
    for line in output.decode("utf-8").split('\n'):
        print(line)


def posix_shell(chan):
    import select

    oldtty = termios.tcgetattr(sys.stdin)
    try:
        sys.stdout.write("\r\n")
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)

        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if len(x) == 0:
                        sys.stdout.write("\r\n*** EOF\r\n")
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                chan.send(x)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

