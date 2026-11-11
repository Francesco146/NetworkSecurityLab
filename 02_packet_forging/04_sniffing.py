from scapy.all import *
import sys
if sys.platform == "darwin":
    conf.use_pcap = True

print("Sniffing packets...")

def print_pkt(pkt):
    print(pkt.summary())

#pkt = sniff(filter='tcp', prn=print_pkt)
iface = "lo0" if sys.platform == "darwin" else "lo"
pkt = sniff(filter='icmp', prn=print_pkt, iface=iface)