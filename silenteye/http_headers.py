import requests
from colorama import Fore, Style

def analyze_headers(target):
    if not target.startswith("http"):
        target = "http://" + target

    try:
        response = requests.get(target, timeout=5)
        headers = response.headers

        print(f"\n{Fore.CYAN}[+] Cabeceras HTTP encontradas para: {target}{Style.RESET_ALL}\n")

        for key, value in headers.items():
            print(f"{Fore.YELLOW}{key}: {Fore.WHITE}{value}{Style.RESET_ALL}")

        print("\n[🔎] Análisis de seguridad:")
        security_headers = [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Referrer-Policy",
            "Permissions-Policy"
        ]

        for sh in security_headers:
            if sh in headers:
                print(f"{Fore.GREEN}[✔] {sh} está presente.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[✘] {sh} está ausente.{Style.RESET_ALL}")

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[!] Error al conectar con el objetivo: {e}{Style.RESET_ALL}")
