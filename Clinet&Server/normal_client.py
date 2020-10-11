import socket
import sys
import time

PORT = 12345
MESSAGE = "HELLO,WORLD"


def normal_client(address, frequency):
    add = (address, PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(10)
    while True:
        start = time.time()
        s.sendto(MESSAGE.encode(), add)
        try:
            data, server = s.recvfrom(1024)
            end = time.time()
            elapsed = end - start
            print("Get response in {}".format(elapsed))
        except socket.timeout:
            print('Request Time Out')
        time.sleep(float(frequency))


if __name__ == '__main__':
    normal_client(sys.argv[1], sys.argv[2])
