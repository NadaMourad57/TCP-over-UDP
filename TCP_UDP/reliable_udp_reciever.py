import socket
from packet import Packet

class ReliableUDPReceiver:
    def __init__(self, listen_port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', listen_port))
        self.expected_seq = 0
        self.connected = False

    def send_ack(self, addr, seq):
        ack = f"{seq}|ACK||".encode()
        self.socket.sendto(ack, addr)
        print(f"Sent ACK for seq {seq}")

    def listen(self):
        print("Receiver ready.")
        while True:
            raw_data, addr = self.socket.recvfrom(4096)
            pkt = Packet.from_bytes(raw_data)

            if not pkt or not pkt.is_valid():
                print("Invalid or corrupted packet received.")
                continue

            print(f"Received packet: flag={pkt.flag}, seq={pkt.seq}, data={pkt.data}")

            if pkt.flag == "SYN":
                print("Received SYN")
                synack = Packet(pkt.seq, "SYN-ACK", flag="SYN-ACK")
                self.socket.sendto(synack.to_bytes(), addr)
                print("Sent SYN-ACK")

            elif pkt.flag == "ACK":
                print("Handshake complete with client.")
                self.connected = True

            elif pkt.flag == "FIN":
                if self.connected:
                    print("Received FIN. Closing connection.")
                    break
                else:
                    print("Received FIN before connection. Ignored.")
                    continue

            elif not self.connected:
                print("Data received before handshake. Ignored.")
                continue

            elif pkt.seq == self.expected_seq:
                print(f"Received packet seq {pkt.seq}: {pkt.data}")
                self.send_ack(addr, pkt.seq)
                self.expected_seq ^= 1

            else:
                print(f"Duplicate packet seq {pkt.seq} received.")
                self.send_ack(addr, pkt.seq)

if __name__ == "__main__":
    receiver = ReliableUDPReceiver(12000)
    receiver.listen()
