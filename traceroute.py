import socket

import sys


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

    # connecting to the server
    s.connect((host_ip, port))
    print("the socket has successfully connected to " + host_ip)
    s.send('Hello'.encode())
    print(s.recv(1024).decode())

    s.close()


if __name__ == '__main__':
    traceroute(input('Enter IP: '))
