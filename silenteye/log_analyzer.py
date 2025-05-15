import os
import platform
import re
from colorama import Fore, Style

KEYWORDS = [
    "error", "failed", "unauthorized", "malware", "attack",
    "exploit", "ransomware", "critical", "suspicious", "denied"
]

DEFAULT_LOG_PATHS = {
    "Windows": [
        os.path.expandvars(r"%SystemRoot%\System32\LogFiles"),
        os.path.expandvars(r"%ProgramFiles%"),
        os.path.expandvars(r"%ProgramFiles(x86)%"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Local"),
    ],
    "Linux": [
        "/var/log",
        "/var/tmp",
        "/tmp"
    ]
}

def is_log_file(filename):
    return filename.lower().endswith(('.log', '.txt'))

def scan_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f, 1):
                for keyword in KEYWORDS:
                    if re.search(rf'\\b{re.escape(keyword)}\\b', line, re.IGNORECASE):
                        return (i, keyword, line.strip())
    except Exception as e:
        return None
    return None

def analyze_logs():
    system = platform.system()
    print(f"\n[~] Analizando logs del sistema operativo: {system}")

    paths_to_scan = DEFAULT_LOG_PATHS.get(system, [])
    results = []

    for base_dir in paths_to_scan:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if is_log_file(file):
                    file_path = os.path.join(root, file)
                    result = scan_file(file_path)
                    if result:
                        line_num, keyword, content = result
                        print(f"{Fore.YELLOW}[!] Posible hallazgo en: {file_path}{Style.RESET_ALL}")
                        print(f"    ↳ Línea {line_num} (clave: '{keyword}'): {content[:100]}{Style.RESET_ALL}")
                        results.append((file_path, line_num, keyword, content))

    if not results:
        print(f"{Fore.GREEN}[✔] No se encontraron patrones sospechosos en los archivos analizados.{Style.RESET_ALL}")
    else:
        output_dir = "log_reports"
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "log_analysis.txt"), 'w', encoding='utf-8') as f:
            for path, line, keyword, content in results:
                f.write(f"[!] {path} - línea {line} (clave: {keyword})\n")
                f.write(f"    → {content}\n\n")
        print(f"\n[💾] Reporte guardado en: {output_dir}/log_analysis.txt")


