from scapy.all import *
import sys
if sys.platform == "darwin":
    conf.use_pcap = True

spoofed_ip = "1.2.3.4"
target = "127.0.0.1"

ip = IP(dst=target, src=spoofed_ip)

icmp = ICMP()

pkt = ip / icmp

print(pkt)
sr1(pkt)