from scapy.all import sniff, IP, TCP, UDP, get_if_list, conf, Raw #type: ignore
import time

protocol_counts = {"TCP": 0, "UDP": 0, "Other": 0}

def packet_callback(packet):
    if packet.haslayer(IP):
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        proto = "TCP" if packet.haslayer(TCP) else "UDP" if packet.haslayer(UDP) else "Other"
        
        if packet.haslayer(TCP):
            proto = "TCP"
            protocol_counts["TCP"] += 1

        elif packet.haslayer(UDP):
            proto = "UDP"
            protocol_counts["UDP"] += 1

        else:
            proto = "Other"
            protocol_counts["Other"] += 1
        
        src_port = packet.sport if hasattr(packet, 'sport') else "N/A"
        dst_port = packet.dport if hasattr(packet, 'dport') else "N/A"
        
        print(f"[{proto}] {ip_src}:{src_port} -> {ip_dst}:{dst_port} | Summary: {packet.summary()}")

        if packet.haslayer(Raw):
                    try:
                        payload = packet[Raw].load.decode('utf-8', errors='ignore')
                        
                        if any(key in payload.lower() for key in ["user", "pass", "login", "pwd"]):
                            print(f"  [!] ALERT: Sensitive Data Found: {payload.strip()}")
                    except Exception:
                        pass

def main():
    target_ip = "127.0.0.1"
    # target_ip = "192.168.1.143" #Kali ip 
    # interface = r"\Device\NPF_{3BA1E4C2-FBD0-422B-8236-3DBB23265E60}"
    interface = r"\Device\NPF_Loopback"
    interfaceDNS = conf.iface
    
    print(f"--- Starting Live Packet Capture for Server {target_ip} ---")
    
    # Filter 1 TCP
    print(f"\n[Part 1] Capturing 50 TCP packets for {target_ip}...")
    sniff(iface=interface, filter=f"tcp and host {target_ip}", count=50, prn=packet_callback, timeout=10)
    # sniff(filter=f"tcp and host {target_ip}", count=50, prn=packet_callback, timeout=10)

    # Filter 2 HTTP
    print(f"\n[Part 2] Capturing 50 HTTP (Port 8080) packets for {target_ip}...") # Changed to 8080 since my local docker server is on 8080
    sniff(iface=interface, filter=f"tcp port 8080 and host {target_ip}", count=50, prn=packet_callback, timeout=10)
    # sniff(filter=f"tcp port 80 and host {target_ip}", count=50, prn=packet_callback, timeout=10)
    
    # Filter 3 DNS
    print(f"\n[Part 3] Capturing 50 DNS (Port 53) packets")
    sniff(iface=interfaceDNS,filter=f"udp port 53", count=50, prn=packet_callback, timeout=20) # host / target ip was removed so dns traffic could be captured
    # sniff(filter=f"udp port 53 and host {target_ip}", count=50, prn=packet_callback, timeout=10)

    print("\n" + "="*45)
    print(f"{'PROTOCOL':<15} | {'PACKET COUNT':<15}")
    print("-" * 45)
    for proto, count in protocol_counts.items():
        print(f"{proto:<15} | {count:<15}")
    print("="*45)

    print("\n--- Capture Complete ---")

if __name__ == "__main__":
    main()