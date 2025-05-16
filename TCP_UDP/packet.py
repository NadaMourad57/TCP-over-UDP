# packet.py
import hashlib

class Packet:
    def __init__(self, seq, data, checksum=None, flag=None):
        self.seq = seq
        self.data = data
        self.flag = flag
        self.checksum = checksum or self.calculate_checksum()

    def calculate_checksum(self):
        content = f"{self.seq}{self.data}{self.flag or ''}"
        return hashlib.md5(content.encode()).hexdigest()

    def is_valid(self):
        return self.checksum == self.calculate_checksum()

    def to_bytes(self):
        return f"{self.seq}|{self.flag or ''}|{self.data}|{self.checksum}".encode()

    @staticmethod
    def from_bytes(raw_bytes):
        try:
            parts = raw_bytes.decode().split('|')
            if len(parts) != 4:
                raise ValueError("Invalid packet format")
            seq = int(parts[0])
            flag = parts[1] if parts[1] else None
            data = parts[2]
            checksum = parts[3]
            return Packet(seq, data, checksum, flag)
        except Exception as e:
            print("Packet parse error:", e)
            return None
