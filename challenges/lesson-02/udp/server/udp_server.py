import select
import socket

# 5555: servizio echo (risponde)
echo = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
echo.bind(("0.0.0.0", 5555))

# 5556: servizio silenzioso (ascolta ma non risponde)
silent = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
silent.bind(("0.0.0.0", 5556))

print("UDP target: echo on 5555, silent on 5556", flush=True)

while True:
    ready, _, _ = select.select([echo, silent], [], [])
    for sock in ready:
        data, addr = sock.recvfrom(2048)
        if sock is echo:
            sock.sendto(b"UDP-OK:" + data, addr)
        # silent: intentionally no response
