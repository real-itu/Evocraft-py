import socket
from contextlib import closing
import docker
import click

class EvoCraftDockerInstance:
    def __init__(self, minecraft_server_port, grpc_port):
        self.minecraft_server_port = minecraft_server_port
        self.grpc_port = grpc_port
        self.name = "evocraft-server_grpc{}_minecraft_server{}".format(self.grpc_port, self.minecraft_server_port)
        self.client = docker.from_env()
        self.container = None

    def start(self, cpu_shares=1.5, mem_limit="2g"):
        cpu_quota_multipler = 100000
        command = "java -jar spongevanilla-1.12.2-7.3.0.jar"
        port_dict = {"5001":self.grpc_port, "25565":self.minecraft_server_port}
        self.container = self.client.containers.run("evocraft-server:latest", name=self.name, command=command, detach=True, tty=True, ports=port_dict, cpu_quota=int(cpu_quota_multipler*cpu_shares), mem_limit=mem_limit)
    
    def get_container_from_client(self):
        containers = self.client.containers.list()
        for c in containers:
            if c.name == self.name:
                return c
        return None
    
    def stop(self):
        successful = False
        if self.container is not None:
            try:
                self.container.stop()
                self.container.remove()
                return True
            except Exception as e:
                print("Failed to stop and remove server container: {}".format(e))
                c = self.get_container_from_client()
                if c is not None:
                    c.stop()
                    c.remove()
                    return True
                return False
        else:
            self.container = self.get_container_from_client()
            return self.stop()
                
def kill_all_servers():
    client = docker.from_env()
    server_containers = [c for c in client.containers.list() if "evocraft-server" in c.name]
    for c in server_containers:
        try:
            c.stop()
            c.remove()
        except Exception as e:
            print("Caught exception: ", e)
    
def find_free_port(port_set):
    port = None
    while port is None or port in port_set:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            port = s.getsockname()[1]
    port_set.add(port)
    return port

def find_free_server_grpc_ports(num_ports=10):
    port_tuples = []
    port_set = set([])
    for i in range(num_ports):
        server_port = find_free_port(port_set)
        grpc_port = find_free_port(port_set)
        port_tuples.append((server_port,grpc_port))
    return port_tuples

def run_minecraft_servers(num_servers = 1, cpu_shares=1.0, mem_limit="500mb"):
    minecraft_server_dict = {}
    port_tuples = find_free_server_grpc_ports(num_servers)
    for p in port_tuples:
        server_port, grpc_port = p
        minecraft_server_dict[p] = EvoCraftDockerInstance(server_port, grpc_port)
        minecraft_server_dict[p].start( cpu_shares=cpu_shares, mem_limit=mem_limit)
    
    return minecraft_server_dict


@click.command()
@click.option("--kill_servers", default=False, flag_value='kill_servers', help="set to true to kill servers")
@click.option('--num_servers', default=1, type=click.INT, help='Number of servers')
@click.option('--memory_limit', default="2gb", help='Memory limit for each container')
@click.option("--cpu_shares", default=1.0,type=click.FLOAT, help="CPU allocation for each container")
def manage_evocraft_servers(kill_servers: bool, num_servers: int, memory_limit: str, cpu_shares: float):
    if kill_servers:
        print("Killing servers")
        return kill_all_servers()
    print("Starting {} minecraft servers with cpu_shares {} and memory_limit {}".format(num_servers, cpu_shares, memory_limit))
    return run_minecraft_servers(num_servers, cpu_shares, memory_limit)

if __name__ == "__main__":
    manage_evocraft_servers()