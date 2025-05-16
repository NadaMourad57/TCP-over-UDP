from transport import ReliableUDP

client = ReliableUDP('localhost', 0)
server_addr = ('localhost', 9000)

client.connect(server_addr)

request = "GET / HTTP/1.0\nHost: localhost\n\n"
client.sendto(request, server_addr)
data, _ = client.recvfrom()
print("Response from server:\n", data)
