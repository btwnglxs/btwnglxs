import socket
import argparse
from rich import print
import threading
import time
from my_netutils import parse_ports

parser = argparse.ArgumentParser()
parser.add_argument("-ip", type=str, required=True, help="IP address to scan")
parser.add_argument("-ports", type=parse_ports, required=True, help="Ports to scan")
args = parser.parse_args()

start_time = time.time()
threads = []

IP = args.ip
PORTS = args.ports

def scan_port(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1.0)
	result = s.connect_ex((IP, port))
	if not result:
		print(f"[bold green][+][/] Port {port} is open.")
	s.close()

for port in PORTS:
	t = threading.Thread(target=scan_port, args=(port,))
	threads.append(t)
	t.start()

for t in threads:
	t.join()

finish_time = time.time() - start_time
elapsed_time = round(finish_time)

print(f"[bold white][i][/] Scanning complete. [bright_black]ET: {elapsed_time}[/]")
