import socket
import matplotlib.pyplot as plt
import array
import numpy as np

A1 = array.array('i', [0]*1000)
A2 = array.array('i', [0]*1000)
A3 = array.array('i', [0]*1000)
A4 = array.array('i', [0]*1000)
A5 = array.array('i', [0]*1000)
fig = plt.figure()
plt.ion()
ax = fig.add_subplot(111)
line1, = ax.plot([], [],'-k',label='black')
line1.set_ydata(A1)
line1.set_xdata(range(len(A1)))
line2, = ax.plot([], [],'-g',label='green')
line2.set_ydata(A2)
line2.set_xdata(range(len(A2)))
line3, = ax.plot([], [],'-r',label='red')
line3.set_ydata(A3)
line3.set_xdata(range(len(A3)))
line4, = ax.plot([], [],'-b',label='blue')
line4.set_ydata(A4)
line4.set_xdata(range(len(A4)))
line5, = ax.plot([], [],'-m',label='magenta')
line5.set_ydata(A5)
line5.set_xdata(range(len(A5)))
#ax.relim()
#ax.autoscale_view()
plt.axis([0, 1000, 0, 26000])
plt.show()

UDP_IP = "10.52.90.236"
UDP_PORT = 2600
sonarNum = 0
sonarMeas = 0

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

A1.append(1)
A2.append(1)
A3.append(1)
A4.append(1)
A5.append(1)
line1.set_ydata(A1)
line1.set_xdata(range(len(A1)))
line2.set_ydata(A2)
line2.set_xdata(range(len(A2)))
line3.set_ydata(A3)
line3.set_xdata(range(len(A3)))
line4.set_ydata(A4)
line4.set_xdata(range(len(A4)))
line5.set_ydata(A5)
line5.set_xdata(range(len(A5)))
ax.relim()
ax.autoscale_view()
plt.draw()

# Collect sonar data and update plot in an infinite loop!
i = 1
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    # print "received message:", data
    # Check if this is the right packet type
    if(ord(data[0]) == 16):
        sonarNum = ord(data[1])
        sonarMeas = ord(data[2])*0x100 + ord(data[3])
        #print "S", sonarNum, "  Val = ", sonarMeas
        if(sonarNum == 0):
            A1.pop(0)
            A1.append(sonarMeas)
        if(sonarNum == 1):
            A2.pop(0)
            A2.append(sonarMeas+5000)
        if(sonarNum == 2):
            A3.pop(0)
            A3.append(sonarMeas+10000)
        if(sonarNum == 3):
            A4.pop(0)
            A4.append(sonarMeas+15000)
        if(sonarNum == 4):
            A5.pop(0)
            A5.append(sonarMeas+20000)

        i = i + 1
        if i == 20:
            i = 0
            line1.set_ydata(A1)
            line1.set_xdata(range(len(A1)))
            line2.set_ydata(A2)
            line2.set_xdata(range(len(A2)))
            line3.set_ydata(A3)
            line3.set_xdata(range(len(A3)))
            line4.set_ydata(A4)
            line4.set_xdata(range(len(A4)))
            line5.set_ydata(A5)
            line5.set_xdata(range(len(A5)))
            plt.draw()



