from scapy.all import *
import re
import subprocess
import sys

conf.L3socket = L3RawSocket  # may resolve some issues when sending packets in Linux


def _macos_sync_arp():
    try:
        out = subprocess.check_output(["arp", "-an"], text=True)
    except Exception:
        return
    for line in out.splitlines():
        match = re.search(r"\(([\d.]+)\) at ([0-9a-fA-F:]+)", line)
        if match:
            conf.netcache.arp_cache[match.group(1)] = match.group(2)


def _macos_sync_iface():
    iface = conf.iface
    if getattr(iface, "mac", None) not in (None, "00:00:00:00:00:00"):
        return
    try:
        out = subprocess.check_output(["ifconfig", iface.name], text=True)
    except Exception:
        return
    match = re.search(r"ether ([0-9a-fA-F:]+)", out)
    if match:
        iface.mac = match.group(1)


if sys.platform == "darwin":
    conf.use_pcap = True
    _macos_sync_iface()
    _macos_sync_arp()

TARGET = "scanme.nmap.org" 

for port in range(1, 100):
    pkt = IP(dst=TARGET)/TCP(dport=port, sport=RandShort(), flags="S")  # SYN
    response = sr1(pkt, timeout=2, verbose=0)
    
    if response is not None and response.haslayer(TCP):
        if response.getlayer(TCP).flags == 0x12:  # SYN-ACK
            print(f"Port {port} is open")
            # Send RST to close the connection
            send(IP(dst=TARGET)/TCP(dport=port, flags="R"), verbose=0)
        elif response.getlayer(TCP).flags == 0x14:  # RST-ACK
            pass # port closed
    else:
        pass # no response, port filtered
