import socket
#import matplotlib.pyplot as plt
#import array
#import numpy as np

UDP_IP = "10.52.90.236"
UDP_PORT = 2600

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
string = raw_input(">")
#print "sending"
sock.sendto(string, ("10.52.90.230", 2390))

while (string != 'exit') and (string !='quit'):
    sock.settimeout(2)

#    print "waiting for reply"
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print data

    string = raw_input(">")
    print "sending"
    sock.sendto(string, ("10.52.90.230", 2390))


sock.close()
