import socket
import argparse
from colorama import Fore, Style

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL",
    3389: "RDP", 8080: "HTTP-Proxy"
}

def detect_firewall(ip, ports):
    dropped_count = 0
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, port))
            if result == 0:
                sock.close()
                return False  # No hay firewall, puerto abierto
            elif result != 111:  # Si no es "connection refused"
                dropped_count += 1
            sock.close()
        except:
            dropped_count += 1
    return dropped_count == len(ports)  # Todos bloqueados

def detect_service_banner(sock):
    try:
        sock.settimeout(2)
        return sock.recv(1024).decode(errors='ignore')
    except:
        return None

def aggressive_banner_grab(sock):
    try:
        sock.sendall(b'HEAD / HTTP/1.0\r\n\r\n')
        return sock.recv(1024).decode(errors='ignore')
    except:
        return None

def scan_target(ip, start_port, end_port, verbose=False, aggressive=False):
    ports = range(start_port, end_port + 1)
    open_ports = []

    print(f"\n[~] Escaneando {ip} del puerto {start_port} al {end_port}...\n")

    detected_firewall = detect_firewall(ip, [21, 22, 23, 80, 443, 3306])
    if detected_firewall and not aggressive:
        print(f"{Fore.RED}[!] Posible firewall o IDS detectado. Evitando escaneo de versiones por seguridad.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Puede intentar usar --aggressive para forzar la detección de versiones bajo su propio riesgo.{Style.RESET_ALL}")
        return

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))

            if result == 0:
                service_name = COMMON_PORTS.get(port, "Desconocido")
                print(f"{Fore.GREEN}[+] Puerto {port} abierto ({service_name}){Style.RESET_ALL}")
                banner = detect_service_banner(sock)

                if banner:
                    print(f"    ↳ Versión detectada: {Fore.CYAN}{banner[:100]}{Style.RESET_ALL}")
                else:
                    if aggressive:
                        banner = aggressive_banner_grab(sock)
                        if banner:
                            print(f"    ↳ Versión (modo agresivo): {Fore.MAGENTA}{banner[:100]}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}    ❌ No se pudo obtener la versión incluso en modo agresivo.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}    ❌ No se pudo identificar la versión del servicio en el puerto {port}.{Style.RESET_ALL}")
                        print(f"       Puede intentar con técnicas más agresivas usando la opción {Fore.CYAN}--aggressive{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}       ⚠️ Advertencia: Esto puede activar alertas en firewalls o sistemas IDS.{Style.RESET_ALL}")

                open_ports.append((port, service_name, banner if banner else "N/A"))

            sock.close()
        except Exception as e:
            if verbose:
                print(f"{Fore.RED}[!] Error al escanear el puerto {port}: {e}{Style.RESET_ALL}")

    if not open_ports:
        print(f"{Fore.RED}[!] No se encontraron puertos abiertos en el rango especificado.{Style.RESET_ALL}")
    else:
        print(f"\n[✔] Escaneo completo. Puertos abiertos encontrados: {len(open_ports)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Escáner avanzado de puertos con detección de versiones")
    parser.add_argument("target", help="Dirección IP o dominio del objetivo")
    parser.add_argument("--start", type=int, default=1, help="Puerto de inicio (default: 1)")
    parser.add_argument("--end", type=int, default=1024, help="Puerto final (default: 1024)")
    parser.add_argument("--verbose", action="store_true", help="Muestra errores detallados")
    parser.add_argument("--aggressive", action="store_true", help="Activa técnicas agresivas de detección de versión")
    args = parser.parse_args()

    scan_target(args.target, args.start, args.end, verbose=args.verbose, aggressive=args.aggressive)
