import socket
import subprocess
import argparse

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_free_port(start_port, end_port):
    for port in range(start_port, end_port):
        if not is_port_in_use(port):
            return port
    raise Exception("No free ports available in the given range")

def run_erigon(custom_args):
    # Define port ranges to search for free ports
    port_ranges = {
        'http.port': (8750, 8800),
        'authrpc.port': (8550, 8600),
        'ws.port': (8500, 8550),
        'private.api.addr': (9090, 9150),
        'torrent.port': (42060, 42100),
        'port': (30300, 30310),
        'p2p.allowed-ports': (30310, 30320),
    }

    # Find free ports
    ports = {name: find_free_port(*range_) for name, range_ in port_ranges.items()}

    # Base command
    command = [
        "./build/bin/erigon",
        "--http.api=eth,net,engine,erigon,admin",
        f"--http.port={ports['http.port']}",
        "--authrpc.addr=0.0.0.0",
        f"--authrpc.port={ports['authrpc.port']}",
        "--ws",
        f"--ws.port={ports['ws.port']}",
        "--db.size.limit=8TB",
        "--txpool.gossip.disable=true",
        f"--private.api.addr=127.0.0.1:{ports['private.api.addr']}",
        f"--torrent.port={ports['torrent.port']}",
        f"--port={ports['port']}",
        f"--p2p.allowed-ports={ports['p2p.allowed-ports']}"
    ]

    # Add custom arguments to the command
    if custom_args:
        command.extend(custom_args)
    
    # Write the configuration to a file
    with open('erigon_run.txt', 'w') as f:
        f.write("Erigon Node Configuration:\n")
        for param in command:
            f.write(param + "\n")
    
    # Run the command
    subprocess.run(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Erigon with custom configurations.')
    parser.add_argument('custom_args', nargs=argparse.REMAINDER, help='Custom arguments for Erigon')

    args = parser.parse_args()

    run_erigon(args.custom_args)
