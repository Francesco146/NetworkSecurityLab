from scapy.all import *
import re
import subprocess
import sys

conf.L3socket = L3RawSocket


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

dns_query = IP(dst="8.8.8.8") / UDP(sport=RandShort(), dport=53) / DNS(rd=1, qd=DNSQR(qname="www.univr.it"))

response = sr1(dns_query, timeout=5)

if response:
    print(response.show())
