import sys
import os
import socket
import time
import struct
import select


def future():
    if not len(sys.argv) == 3:
        usage()
        sys.exit(1)
    ttl = 1
    host, port = sys.argv[1:]
    port_int = None
    try:
        port_int = int(port)
    except ValueError:
        if not os.path.exists('/etc/services'):
            print
            'port needs to be an integer if /etc/services does not exist.'
            sys.exit(1)
        fd = open('/etc/services')
        for line in fd:
            match = re.match(r'^%s\s+(\d+)/tcp.*$' % port, line)
            if match:
                port_int = int(match.group(1))
                break
        if not port_int:
            print
            'port %s not in /etc/services' % port
            sys.exit(1)
    port = port_int


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
    s.close()
    # connecting to the server
    for ttl in range(1, 30):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))
        s.settimeout(4)
        try:
            try:
                s.connect((host_ip, port))
                print('Yeah!')
                # msg_in = s.recv(1024).decode()
                # print(msg_in)
            except (socket.error, socket.timeout) as err:
                print('ttl=%02d: %s' % (ttl, err), s.getpeername(), s.getsockname())
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
