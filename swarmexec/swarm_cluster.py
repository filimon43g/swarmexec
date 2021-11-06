import docker
import logging

class SwarmCluster:

    def __init__(self, base_url, nodes_mapping={}) -> None:
        self.client = docker.DockerClient(base_url=base_url)
        self._nodes_mapping = nodes_mapping
        self._find_all_nodes()

    def exec(self, service_name:str, cmd):
        """ Execute command and exit """
        container = self._get_container_by_service_name(service_name)
        if container:
            exict_code, output = container.exec_run(cmd=cmd)
            print_output(output)
            exit(exict_code)
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
            except Exception as e:
                logging.error(f"Could not connect to {self._get_node_ssh_url(node_hostname)}")
                logging.error(e.args[1])
                exit(e.args[0])
            
    def _get_node_ssh_url(self, node_hostname):
        if self._nodes_mapping:
            if node_hostname in self._nodes_mapping:
                return "ssh://" + self._nodes_mapping[node_hostname]
        else:
            return "ssh://" + node_hostname


def print_output(output):
    for line in output.decode("utf-8").split('\n'):
        print(line)