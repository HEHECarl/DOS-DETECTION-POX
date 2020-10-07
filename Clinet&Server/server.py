import socket
import time

PORT = 12345
MESSAGE = "Response"


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', PORT))
    while True:
        message, address = s.recvfrom(512)
        print("Receive from {}".format(address))
        s.sendto(MESSAGE.encode(), address)


if __name__ == '__main__':
    server()