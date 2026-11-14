from scapy.all import IP, UDP, ICMP, Raw, sr1

TARGET = "udp-target"

for port in range(5554, 5558):
    packet = IP(dst=TARGET) / UDP(dport=port) / Raw(b"CCIT")
    response = sr1(packet, timeout=0.7, verbose=0)

    # TODO: classifica la risposta
    # - response is None -> open|filtered
    # - response.haslayer(UDP) -> open (stampa il payload)
    # - response.haslayer(ICMP) con type 3 e code 3 -> closed
    print(port, response.summary() if response else "nessuna risposta")
