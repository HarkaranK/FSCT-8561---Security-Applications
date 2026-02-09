from scapy.all import rdpcap, IP, TCP, UDP #type: ignore
from collections import defaultdict

def detect_flooding(pcap_file):
    print(f"--- Analyzing {pcap_file} ---")
    
    # Load the PCAP file
    packets = rdpcap(pcap_file)
    
    ip_history = defaultdict(list) # timestamps 
    alerted_ips = set()            
    tcp_count = 0
    udp_count = 0

    for pkt in packets:
        if pkt.haslayer(IP):
            src_ip = pkt[IP].src
            timestamp = pkt.time # Uses the internal PCAP time

            # Protocol Counting
            if pkt.haslayer(TCP): tcp_count += 1
            elif pkt.haslayer(UDP): udp_count += 1

            
            ip_history[src_ip].append(timestamp)
            
            # Remove packet timestamps older than 5 seconds from the current packet
            ip_history[src_ip] = [t for t in ip_history[src_ip] if timestamp - t <= 5]

            # Detection Rule (> 20 packets in 5s) & Single Alert
            if len(ip_history[src_ip]) > 20 and src_ip not in alerted_ips:
                print(f"[!] ALERT: Potential Flooding Detected from {src_ip}")
                alerted_ips.add(src_ip)

    # 5: Output Summary
    print("\n" + "="*30)
    print("   PCAP ANALYSIS SUMMARY")
    print("="*30)
    print(f"Total TCP Packets    : {tcp_count}")
    print(f"Total UDP Packets    : {udp_count}")
    print(f"Suspicious IPs Found : {len(alerted_ips)}")
    print("="*30)

if __name__ == "__main__":
    # Ensure the .pcap file is in the same directory as this script
    detect_flooding("botnet-capture-20110812-rbot.pcap")