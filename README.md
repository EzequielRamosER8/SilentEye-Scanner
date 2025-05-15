# SilentEye-Scanner

# 🛡️ SilentEye Scanner Pro

**SilentEye Scanner Pro** es un escáner de red avanzado, desarrollado en Python, capaz de identificar puertos abiertos, servicios, y realizar técnicas de banner grabbing. Incluye opciones de análisis agresivo para entornos de pentesting controlado y detección de firewalls o sistemas IDS.

## ⚙️ Características principales

* Detección de puertos abiertos.
* Identificación de servicios conocidos.
* Banner grabbing pasivo y agresivo.
* Detección básica de firewall/IDS.
* Modo verbose para depuración detallada.
* Modo agresivo opcional para extracción intensiva de información.
* Totalmente por consola, ideal para scripting o auditorías automatizadas.

## 📦 Requisitos

* Python 3.6 o superior
* colorama

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

## 🚀 Ejemplo de uso

```bash
python main.py --target 192.168.0.1 --ports 1-1000 --verbose
```

* `--target`: Dirección IP o dominio a escanear.
* `--ports`: Rango de puertos (por ejemplo, 1-1024).
* `--verbose`: Muestra mensajes detallados durante el escaneo.
* `--aggressive`: (opcional) Realiza técnicas más intrusivas para intentar obtener banners de versión.

#### Ejemplo con técnicas agresivas:

```bash
python main.py --target pagina.com --ports 20-25 --verbose --aggressive
```

## ⚠️ Advertencia

El uso de técnicas agresivas puede generar alertas en sistemas de detección de intrusos (IDS) o firewalls. Utilice esta herramienta **solo en entornos donde tenga autorización explícita.**

---

## 🧑‍💻 Autor

* **Nombre:** Ezequiel Ramos 
* **Especialización:** Ciberseguridad ofensiva y desarrollo de herramientas de pentesting.
* **GitHub:** [github.com/Ezequiel Ramos](https://github.com/EzequielRamosER8)
