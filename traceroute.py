import socket

import sys

import struct

from netifaces import interfaces, ifaddresses, AF_INET


def traceroute(str):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create socket object on UDP connection
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" % (err))

    # default port for socket
    port = 80
    try:
        host_ip = socket.gethostbyname(str)
    except socket.gaierror:
        # this means could not resolve the host
        print("there was an error resolving the host")
        sys.exit()

    print(host_ip)
    # connecting to the server
    for ttl in range(1, 30):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))
        s.settimeout(4)
        try:
            try:
                s.connect((host_ip, port))
                print('Yeah!')
            except (socket.error, socket.timeout) as err:
                print('ttl=%02d: %s' % (ttl, err), s.getpeername(), s.getsockname(), s.proto, s.type, s.gettimeout())
                continue
            except KeyboardInterrupt:
                print('ttl=%02d (KeyboardInterrupt)' % ttl)
                break

        finally:
            s.close()
        print('ttl=%02d: OK' % (ttl))
        break


if __name__ == '__main__':
    traceroute(input('Enter IP: '))
