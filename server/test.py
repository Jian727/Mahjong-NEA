import socket

## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(socket.gethostname())

print(f"IP Address: {ip_address}")