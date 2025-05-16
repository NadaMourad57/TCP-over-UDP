
# reliable_sender.py
import socket
from packet import Packet

class ReliableUDPSender:
    def __init__(self, receiver_ip, receiver_port, timeout=2):
        self.receiver_addr = (receiver_ip, receiver_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(timeout)
        self.seq = 0

    def connect(self):
        syn_packet = Packet(self.seq, "SYN request", flag="SYN")
        self.socket.sendto(syn_packet.to_bytes(), self.receiver_addr)
        print("SYN sent")

        while True:
            try:
                raw_ack, _ = self.socket.recvfrom(1024)
                pkt = Packet.from_bytes(raw_ack)
                if pkt and pkt.flag == "SYN-ACK":
                    print("Received SYN-ACK")
                    ack_packet = Packet(self.seq, "ACK confirm", flag="ACK")
                    self.socket.sendto(ack_packet.to_bytes(), self.receiver_addr)
                    print("Connection established.")
                    break
            except socket.timeout:
                print("Timeout waiting for SYN-ACK. Resending SYN...")
                self.socket.sendto(syn_packet.to_bytes(), self.receiver_addr)

    def send(self, message):
        packet = Packet(self.seq, message)
        while True:
            self.socket.sendto(packet.to_bytes(), self.receiver_addr)
            print(f"Sent packet seq {self.seq}: {message}")
            try:
                ack_data, _ = self.socket.recvfrom(1024)
                ack_parts = ack_data.decode().split('|')
                if ack_parts[1] == "ACK" and int(ack_parts[0]) == self.seq:
                    print(f"Received ACK for seq {self.seq}")
                    self.seq ^= 1
                    break
            except socket.timeout:
                print("Timeout: retransmitting...")

    def close(self):
        fin_packet = Packet(self.seq, "Closing", flag="FIN")
        self.socket.sendto(fin_packet.to_bytes(), self.receiver_addr)
        print("FIN sent. Closing socket.")
        self.socket.close()
