"""
Project: Port Scanner
Author: Ryan Brinkman
Date: February 11, 2025

Description:
A high-performance Port Scanner that allows users to scan a target machine's ports.
Includes multiple scan modes and logs results in a structured format.

GitHub Repository: https://github.com/RyanBrin/python/tree/main/vs-code/port-scanner/
"""

import socket
import os
import threading
from pathlib import Path
from datetime import datetime

# Commonly used service ports (Top 50)
common_ports = [
    21, 22, 23, 25, 53, 67, 68, 80, 110, 123, 135, 139, 143, 161, 162, 389,
    443, 445, 465, 587, 993, 995, 1433, 1521, 1723, 2049, 3306, 3389, 5432,
    5800, 5900, 6000, 6379, 8000, 8080, 8443, 8888, 9000, 9090, 10000, 32768
]

# Commonly scanned ports based on different levels
top_100_ports = [
    21, 22, 23, 25, 53, 67, 68, 69, 80, 110, 123, 135, 139, 143, 161, 162,
    389, 443, 445, 465, 587, 993, 995, 1025, 1080, 1194, 1433, 1521, 1723,
    2049, 2082, 2083, 2181, 2483, 2484, 3306, 3389, 3690, 4000, 4045, 4190,
    4321, 4500, 5000, 5432, 5632, 5800, 5900, 6000, 6379, 6667, 7000, 8000,
    8080, 8443, 8888, 9000, 9090, 9200, 10000, 32768, 49152, 65535
]

top_1000_ports = list(range(1, 1001))  # First 1000 ports

all_ports = range(1, 65536)  # All 65535 ports


RESULTS_DIR = "logs" # Directory to store scan results
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") # Timestamp
BASE_DIR = Path(__file__).resolve().parent  # Gets the directory where the script is located
PORT_SCANNER_DIR = BASE_DIR  # Ensure "port-scanner" is the base folder
RESULTS_DIR = PORT_SCANNER_DIR / "logs"  # Logs folder inside "port-scanner"
scan_dir = RESULTS_DIR / f"scan-{timestamp}"  # Scan-specific folder
runtime_log_file = scan_dir / "runtime-log.txt"  # Runtime log file

# Ensure all required directories exist
os.makedirs(PORT_SCANNER_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(scan_dir, exist_ok=True)


def log_message(message: str):
    """Logs a message to the runtime log file with a timestamp."""
    with open(runtime_log_file, "a") as log:
        log.write(f"[{datetime.now()}] {message}\n")

log_message("Scan started.")
log_message(f"Results will be stored in: {scan_dir}")

def get_target() -> str:
    """Prompts the user to enter a target IP or hostname and sanitizes the input."""
    target = input("Enter the target IP: ").strip()
    
    log_message(f"Target resolved: {target}")
    return target

target = get_target()

def get_ports_to_scan() -> list:
    """Allows the user to choose the scan type and defines the ports to be scanned."""
    print("\nChoose a scan type:")
    print("    1. Common Ports Scan")
    print("    2. Fast Scan (Top 100 Ports)")
    print("    3. Extended Scan (Top 1000 Ports)")
    print("    4. Full Scan (All 65535 Ports)")

    while True:
        try:
            scan_type = int(input("Enter your choice (1-4): "))
            if scan_type in [1, 2, 3, 4]:
                break
            print("Invalid choice. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    if scan_type == 1:
        log_message("Performing Common Ports Scan.")
        return common_ports
    elif scan_type == 2:
        log_message("Performing Fast Scan (Top 100 Ports).")
        return top_100_ports
    elif scan_type == 3:
        log_message("Performing Extended Scan (Top 1000 Ports).")
        return top_1000_ports
    elif scan_type == 4:
        log_message("Performing Full Scan (1-65535).")
        return all_ports

ports_to_scan = get_ports_to_scan()

open_ports = []
closed_ports = []
scanned_ports = 0

def scan_port(target: str, port: int):
    """Scans a single port on the target machine and logs the result."""
    global scanned_ports, open_ports, closed_ports
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)  # Faster scanning with lower timeout
        result = s.connect_ex((target, port))

        if result == 0:
            open_ports.append(port)
            log_message(f"Port {port} is OPEN")
        else:
            closed_ports.append(port)
            log_message(f"Port {port} is CLOSED")
        
        scanned_ports += 1
    except Exception as e:
        log_message(f"ERROR scanning port {port}: {e}")
    finally:
        s.close()

def scan_ports_multithreaded(target: str, ports: list):
    """Uses threading to scan ports faster by running multiple scans in parallel."""
    threads = []
    for port in ports:
        thread = threading.Thread(target=scan_port, args=(target, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

scan_ports_multithreaded(target, ports_to_scan)

log_message("Scan completed.")
log_message(f"Total scanned ports: {scanned_ports}")
log_message(f"Open ports: {len(open_ports)}")
log_message(f"Closed ports: {len(closed_ports)}")
log_message(f"Results saved in: {scan_dir}")

# Save final results in files
with open((scan_dir / "open-ports.txt"), "w") as f:
    f.write("Open Ports:\n")
    f.writelines([f"{port}\n" for port in open_ports])

with open(scan_dir / "closed-ports.txt", "w") as f:
    f.write("Closed Ports:\n")
    f.writelines([f"{port}\n" for port in closed_ports])