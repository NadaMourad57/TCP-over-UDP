from reliable_udp_sender import ReliableUDPSender

sender = ReliableUDPSender('127.0.0.1', 12000)
sender.connect()

# List of messages to send
messages = [
    "Hello from sender",
    "This is message 2",
    "And here comes message 3",
    "Final message before close"
]

# Send each message reliably
for msg in messages:
    sender.send(msg)

# Graceful connection close
sender.close()
