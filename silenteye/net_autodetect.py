import socket
import platform
import ipaddress

def get_local_ip():
    try:
        # Esto funciona en Windows, Linux, etc.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS como destino temporal
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_subnet(ip):
    # Asumimos máscara /24 (255.255.255.0) como predeterminada
    network = ipaddress.ip_network(f"{ip}/24", strict=False)
    return str(network)

