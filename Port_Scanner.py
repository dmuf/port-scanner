import socket
import threading
import re

# ANSI escape codes for coloring output
GREEN = '\033[92m'
RESET = '\033[0m'

# Function to check if a port is open
def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set a timeout of 1 second for the connection
        result = sock.connect_ex((host, port))
        
        if result == 0:
            print(f"{GREEN}Port {port} is open{RESET}")
        else:
            print(f"Port {port} is closed")
        
        sock.close()
    except socket.error as e:
        print(f"Error scanning port {port}: {e}")

# Function to scan a range of ports
def scan_ports(host, start_port, end_port):
    print(f"Scanning {host} for open ports in range {start_port}-{end_port}")
    
    # Create a thread for each port scan to speed up the process
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(host, port))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

# Function to get well-known ports
def well_known_ports():
    return {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        80: 'HTTP',
        443: 'HTTPS',
        3306: 'MySQL',
        8080: 'HTTP (alternative)'
    }

# Function to validate IP address
def is_valid_ip(ip):
    regex = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
    return re.match(regex, ip) is not None

# Function to validate port range
def validate_ports(start_port, end_port):
    if start_port < 1 or start_port > 65535 or end_port < 1 or end_port > 65535:
        print("Port numbers must be between 1 and 65535.")
        return False
    if start_port > end_port:
        print("Start port cannot be greater than end port.")
        return False
    return True

# Main function
def main():
    # Get user input for IP address
    target_host = input("Enter the target IP address: ")
    
    if not is_valid_ip(target_host):
        print("Invalid IP address. Please enter a valid IPv4 address.")
        return
    
    # Get user input for scanning options
    scan_type = input("Do you want to scan well-known ports (y/n)? ").lower()
    
    if scan_type == 'y':
        # Get the well-known ports
        ports = well_known_ports()
        for port in ports:
            print(f"Scanning {ports[port]} port: {port}")
            scan_port(target_host, port)
    else:
        try:
            start_port = int(input("Enter the start port: "))
            end_port = int(input("Enter the end port: "))
            
            if not validate_ports(start_port, end_port):
                return
            
            scan_ports(target_host, start_port, end_port)
        except ValueError:
            print("Invalid input. Please enter a valid integer for ports.")

# Start the program
main()
