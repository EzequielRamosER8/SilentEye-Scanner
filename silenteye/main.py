import argparse
from ascii_banner import show_banner
from scanner_pro import scan_target
from host_discovery import discover_hosts
from net_autodetect import get_local_ip, get_subnet  # 🔹 Para detección automática
from http_headers import analyze_headers
from log_analyzer import analyze_logs


def main():
    show_banner()

    parser = argparse.ArgumentParser(
    description="SilentEye - Escáner Profesional por Eleze",
    epilog="""
Ejemplos de uso:

  python main.py --target 192.168.0.10
      Escanea la IP con los puertos por defecto (1-1024)

  python main.py --target 192.168.0.10 --ports 80,443,8080
      Escanea solo los puertos indicados

  python main.py --target 192.168.0.10 --verbose
      Escaneo detallado con más información

  python main.py --scan-lan 192.168.0.0/24
      Escanea todos los dispositivos activos en esa red

  python main.py --scan-lan
      Detecta automáticamente el rango de red y escanea la LAN

Los resultados de escaneo LAN se guardan en la carpeta "output/".

Más info en: github.com/EzequielRamos
""",
    formatter_class=argparse.RawDescriptionHelpFormatter
)

    parser.add_argument("--target", help="IP o dominio a escanear")
    parser.add_argument("--ports", default="1-1024", help="Rango de puertos (ej: 80,443 o 1-1000)")
    parser.add_argument("--verbose", action="store_true", help="Muestra más detalles")
    parser.add_argument("--scan-lan", nargs='?', const='auto', metavar="192.168.1.0/24",
                        help="Escanea dispositivos en la red local. Si no se pasa rango, detecta automáticamente.")
    parser.add_argument("--headers", action="store_true", help="Analiza las cabeceras HTTP del objetivo")  # ✅ NUEVO
    parser.add_argument("--analyze-logs", action="store_true", help="Analiza los logs del sistema")  # 🔹 NUEVO ARGUMENTO
    parser.add_argument("--aggressive", action="store_true", help="Usa técnicas más agresivas para obtener versiones (riesgoso)")






    args = parser.parse_args()

    if args.analyze_logs:  # 🔹 NUEVO USO
        analyze_logs()
        return




# scaneo de red local
    if args.scan_lan:
        if args.scan_lan == 'auto':
            ip = get_local_ip()
            network = get_subnet(ip)
            print(f"[~] Rango automático detectado: {network}")
            discover_hosts(network)
        else:
            discover_hosts(args.scan_lan)
        return

    if not args.target:
        print("[!] Debes indicar un objetivo con --target o usar --scan-lan para descubrir hosts.")
        return

    print(f"[+] Objetivo: {args.target}")
    print(f"[+] Puertos: {args.ports}")
    print(f"[+] Verbose: {args.verbose}")

    if args.headers:
        analyze_headers(args.target)
    else:
         scan_target(args.target, args.ports, args.verbose)

if __name__ == "__main__":
    main()
