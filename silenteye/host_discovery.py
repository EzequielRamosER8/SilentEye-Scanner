import ipaddress
import socket
import threading
import os
from datetime import datetime
from colorama import init, Fore
from net_autodetect import get_local_ip, get_subnet

init()

def ping_host(ip, results):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((str(ip), 80))
        if result == 0 or result == 10061:
            results.append(str(ip))
        sock.close()
    except:
        pass

def os_guess(ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, 80))
        ttl = sock.getsockopt(socket.IPPROTO_IP, socket.IP_TTL)
        sock.close()

        if ttl <= 64:
            return "Linux/Unix"
        elif ttl <= 128:
            return "Windows"
        elif ttl <= 255:
            return "Cisco/Dispositivo de red"
        else:
            return "Desconocido"
    except:
        return "Desconocido"

def discover_hosts(network_cidr=None):
    if not network_cidr:
        local_ip = get_local_ip()
        network_cidr = get_subnet(local_ip)
        print(f"[~] IP detectada: {local_ip}")
        print(f"[~] Rango generado: {network_cidr}")

    print(f"\n[~] Iniciando escaneo de red...")
    print(f"[~] Escaneando red: {network_cidr}")
    net = ipaddress.ip_network(network_cidr, strict=False)
    results = []
    threads = []

    for ip in net.hosts():
        t = threading.Thread(target=ping_host, args=(ip, results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    output_lines = []
    print(f"\n[✔] Hosts activos encontrados: {len(results)}")
    for r in results:
        guess = os_guess(r)
        info = f"[+] {r}   -   Sistema Estimado: {guess}"
        print(info)
        print(f"    [>] Escaneando puertos rápidos...")
        from scanner_pro import scan_target
        scan_target(r, "21,22,23,80,443,445", False)
        output_lines.append(info)

    # Guardar en archivo
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("output", exist_ok=True)
    file_path = f"output/scan_lan_{timestamp}.txt"
    with open(file_path, "w") as f:
        f.write(f"Escaneo LAN - {network_cidr}\n\n")
        for line in output_lines:
            f.write(line + "\n")
    print(f"\n[💾] Resultados guardados en: {file_path}")

