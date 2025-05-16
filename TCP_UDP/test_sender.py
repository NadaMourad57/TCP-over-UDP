from reliable_udp_sender import ReliableUDPSender

sender = ReliableUDPSender('127.0.0.1', 12000)
sender.connect()

# Normal send
sender.send("This is a normal message")

# Simulate duplicate
sender.send("This message will be duplicated", simulate_duplicate=True)

# Another normal message
sender.send("Final message")

sender.close()
