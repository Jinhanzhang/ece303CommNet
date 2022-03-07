#!/usr/bin/env python3
import sys, getopt
import socket

DEFAULT = {
    21: 'FTP',
    22: 'SSH',
    23: 'TELNET',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    115: 'SFTP',
    135: 'RPC',
    139: 'NetBIOS',
    143: 'IMAP',
    194: 'IRC',
    443: 'SSL',
    445: 'SMB',
    1433: 'MSSQL',
    3306: 'MySQL'
}

def main(argv):
    if(len(argv)==1):
        print('Missing hostname')
        exit(2)
    hostname = argv[1]
    port_start = 0
    port_end = 65353
    try:
        opts, args = getopt.getopt(argv[2:], 'p')
    except getopt.GetoptError:
        print('./tcp_scanner hostname [-p 15:25]')
        sys.exit(2)
    if len(args)>0:
        arg = args[0].split(':')
        port_start = int(arg[0])
        port_end = int(arg[0])
        if len(arg)>1:
            port_end = int(arg[1])
            if(port_start>port_end):
                print("Port Range Invalid")
                exit(2)
            print("Scanning", hostname, "from port", port_start, "to port", port_end)
        else:
            print("Scanning", hostname, "on port", port_start)
    else:
        print("Scanning", hostname, "from port", port_start, "to port", port_end)
    open_ports = scan(hostname, port_start, port_end)
    print('All open ports:', open_ports)


def scan(hostname, port_start, port_end):
    try:
        target = socket.gethostbyname(hostname)
        print('IP:', target)
        open_ports = []
        for port in range(port_start, port_end+1):
            socket.setdefaulttimeout(1)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            con = s.connect_ex((target, port))
            if con == 0:
                if port in DEFAULT.keys():
                    port = DEFAULT[port]
                open_ports.append(port)
            s.close()
        return open_ports
    except KeyboardInterrupt:
        print('Exiting')
        exit(1)
    except socket.error:
        print('Server Not Responding')
        exit(2)
    except socket.gaierror:
        print('Hostname Could Not Be Resolved')
        exit(2)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
