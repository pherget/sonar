import socket
import select
import matplotlib.pyplot as plt
import numpy as np
import time

# Initialize motors and home stage on startup?  1 = yes
global startup = 1

# Read all data to clear the buffer
def empty_socket(sock):
    #"""remove the data present on the socket"""
    input = [sock]
    while 1:
        inputready, o, e = select.select(input,[],[], 0.0)
        if len(inputready)==0: break
        for s in inputready: 
            s.recv(1)

# Send data to the rail and read and return the reply.
def sendrail(command):
    sockRail.sendto(command, ("10.52.90.230", 2390))
    time.sleep(0.2)
    data, addr = sockRail.recvfrom(1024) # buffer size is 1024 bytes
    return(data)
 
def startupRail():
    if startup==1:
        print "Starting Motors"
        sendrail("1,start")
        time.sleep(.5)
        sendrail("2,start")
        print "Finding Home"
        sendrail("1,home")
        time.sleep(.5)
        sendrail("2,home")
        time.sleep(30)    
        startup = 0
                  
# Calibraion in counts/mm
xCalib = 27.5615346426423/4.0 
yCalib = 10.0860243724961/4.0         

# Number of points to measure            
numPointsX = 25
numPointsY = 20
numSamples = 20
# Starting (top left) position
xPos_mm = 750
yPos_mm = 500
# Increments in x and y
xInc_mm = 12.5
yInc_mm = 12.5

# Read the previously saved parameters for numpoints and positions
f = open("/Users/Phil/Savioke/SweepParms.csv", 'r')
line = f.readline()
vals = line.split(',')
xPos_mm = float(vals[0])
yPos_mm = float(vals[1])
xInc_mm = float(vals[2])
yInc_mm = float(vals[3])
numPointsX = int(float(vals[4]))
numPointsY = int(float(vals[5]))
numSamples = int(float(vals[6]))
f.close()

# IP and port of the Rail (on WiFi) and MBED (on Ethernet)
UDP_MBED_IP = "10.2.98.1"
UDP_MBED_PORT = 2600
UDP_RAIL_IP = "10.52.90.236"
UDP_RAIL_PORT = 2600

# Open Ports
sockRail = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sockRail.bind((UDP_RAIL_IP, UDP_RAIL_PORT))
sockRail.settimeout(4)

sockMbed = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sockMbed.bind((UDP_MBED_IP, UDP_MBED_PORT))

string = "none"
while(string != "9"):
    # Menu
    print "\nTop Lft : (%.1f, %.1f)mm  = [%d, %d]" % (xPos_mm, yPos_mm, xPos_mm*xCalib, yPos_mm*yCalib)
    print "Bot Rt  : (%.1f, %.1f)mm  = [%d, %d]" % (xPos_mm+xInc_mm*numPointsX, yPos_mm+yInc_mm*numPointsY, xCalib*(xPos_mm+xInc_mm*numPointsX), yCalib*(yPos_mm+yInc_mm*numPointsY))
    print "Num Pts : (%d, %d) & %d samples" % (numPointsX, numPointsY, numSamples)
    print("\n1) Get Top Left Corner")
    print("2) Get Botton Right Corner")
    print("3) Collect Data")
    print("4) Go to Top Lft")
    print("5) Go to Bot Rt")
    print("9) Quit")
    string = raw_input(">")

    if string == "1":  # Set top right
        startupRail()
        
        # Move to the top left position
        sendrail("2,p0")
        time.sleep(3)
        sendrail("2,home")
        time.sleep(1)
        print "Moving to " + str(int(xPos_mm*xCalib)) + "," + str(int(yPos_mm*yCalib))
        sendrail("1,p" + str(int(xPos_mm*xCalib)) )
        time.sleep(3)
        sendrail("2,p" + str(int(yPos_mm*yCalib)) )
        time.sleep(3)
        sendrail("1,powerdown")
        sendrail("2,powerdown")
            
        print("\nMove to top left position and press ENTER.")
        string = raw_input(">")
        
        # Get the new top left position
        data = sendrail("1,getp")
        toplfx = int(data[3:])
        data = sendrail("2,getp")
        toplfy = int(data[3:])
        print "x, y = " + str(toplfx) + ", " + str(toplfy)

    if string == "2":  # Set bottom right
        startupRail()

        sendrail("2,p0")
        time.sleep(3)
        sendrail("2,home")
        time.sleep(1)
        print "Moving to " + str(int((xPos_mm+xInc_mm*numPointsX)*xCalib)) + "," + str(int((yPos_mm+yInc_mm*numPointsY)*yCalib))
        sendrail("1,p" + str(int((xPos_mm+xInc_mm*(numPointsX-1))*xCalib)))
        time.sleep(3)
        sendrail("2,p" + str(int((yPos_mm+yInc_mm*(numPointsY-1))*yCalib)))
        time.sleep(3)
        sendrail("1,powerdown")
        sendrail("2,powerdown")
            
        print("\nMove to bottom right position and press ENTER.")
        string = raw_input(">")

        # Get the new bottom right position
        data = sendrail("1,getp")
        botrtx = int(data[3:])
        data = sendrail("2,getp")
        botrty = int(data[3:])
        print "x, y = " + str(botrtx) + ", " + str(botrty)
        
        # Calculate the step sizes and center positions
        sizex = botrtx - toplfx;
        sizey = botrty - toplfy;
        stepx = sizex/(numPointsX-1);
        stepy = sizey/(numPointsY-1);
        centerx = toplfx + sizex/2;
        centery = toplfy + sizey/2;

        print "xDist " + str(sizex) + " or " + str(sizex/xCalib) + "mm" 
        print "yDist " + str(sizey) + " or " + str(sizey/yCalib) + "mm" 
        print "xStep " + str(stepx) + " or " + str(stepx/xCalib) + "mm" 
        print "yStep " + str(stepy) + " or " + str(stepy/yCalib) + "mm" 

        # Set the new configuration positions
        xPos_mm = toplfx/xCalib
        yPos_mm = toplfy/yCalib
        xInc_mm = stepx/xCalib
        yInc_mm = stepy/yCalib

        # Write the positions to a file
        f = open('/Users/Phil/Savioke/SweepParms.csv', 'w')
        # First line contains the array size and x and y increment sizes
        f.write(str(xPos_mm))
        f.write(',')
        f.write(str(yPos_mm))
        f.write(',')
        f.write(str(xInc_mm))
        f.write(',')
        f.write(str(yInc_mm))
        f.write(',')
        f.write(str(numPointsX))
        f.write(',')
        f.write(str(numPointsY))
        f.write(',')
        f.write(str(numSamples))
        f.close()

        # Move the rail to the center of the scan area
        sendrail("2,p0")
        time.sleep(3)
        sendrail("2,home")
        time.sleep(1)
        sendrail("1,p"+ str(centerx))
        time.sleep(3)
        sendrail("2,p"+ str(centery))

    if string == "4":  # Go to top left
        startupRail()

        # Go to Top Left
        sendrail("2,p0")
        time.sleep(3)
        sendrail("2,home")
        time.sleep(1)
        sendrail("1,p"+ str(int(xPos_mm*xCalib)))
        time.sleep(3)
        sendrail("2,p"+ str(int(yPos_mm*yCalib)))
        
    if string == "5":  # Go to bottom right
        startupRail()

        # Go to Bottom Right
        sendrail("2,p0")
        time.sleep(3)
        sendrail("2,home")
        time.sleep(1)
        sendrail("1,p"+ str(int(xCalib*(xPos_mm+xInc_mm*(numPointsX-1)))))
        time.sleep(3)
        sendrail("2,p"+ str(int(yCalib*(yPos_mm+yInc_mm*(numPointsY-1)))))
                
    if string == "9":
        # Close the ports before exiting
        sockRail.close()
        sockMbed.close()
 
    if string == "3":
        # Create Arrays of Zeros
        X = np.zeros((numPointsX, numPointsY))
        Y = np.zeros((numPointsX, numPointsY))
        A0 = np.zeros((numSamples, numPointsX, numPointsY))
        A1 = np.zeros((numSamples, numPointsX, numPointsY))
        A2 = np.zeros((numSamples, numPointsX, numPointsY))
        A3 = np.zeros((numSamples, numPointsX, numPointsY))
        A4 = np.zeros((numSamples, numPointsX, numPointsY))
        
        # Fill in the X and Y positions for each point
        for ix in range(numPointsX):
            for iy in range(numPointsY):
                X[ix][iy] = xInc_mm*ix
                Y[ix][iy] = yInc_mm*iy
        
        # Plot the sensor 0 data (now blank) to pull up figure        
        fig = plt.figure(1)
        plt.subplot(3,2,1)
        plt.ion()
        plt.pcolor(X, Y, A0[5,:,:])
        plt.show()
        plt.draw()
        
        sonarNum = 0
        sonarMeas = 0
        
        startupRail()
       
        print "Raising Y"
        # Send to the top of the range.
        sockRail.sendto("2,p0", ("10.52.90.230", 2390))
        time.sleep(3)    
        # Homing brings the axis against the collision stop
        sockRail.sendto("2,home", ("10.52.90.230", 2390))
        time.sleep(1)    
        
        print "Moving to X start"
        sockRail.sendto("1,p" + str(int(xPos_mm*xCalib)), ("10.52.90.230", 2390))
        time.sleep(5)    
        
        # Move through all x points
        for ix in range(0,numPointsX):
            print str(int(float(ix)/numPointsX*100)) + "% done"
        
            print "X Position " + str(int(xPos_mm+ix*xInc_mm)) + "mm"
            sockRail.sendto("1,p" + str(int((xPos_mm+ix*xInc_mm)*xCalib)), ("10.52.90.230", 2390))
            time.sleep(2)    
        
            sockRail.sendto("2,p" + str(int(yPos_mm*yCalib)), ("10.52.90.230", 2390))
            time.sleep(4)    
            
            # Move through all y points
            #    print "Taking Data Y Data"
            for iy in range(0,numPointsY):
                #print str(iy*100/numPointsY) + "% done"
                sockRail.sendto("2,p" + str(int((yPos_mm+iy*yInc_mm)*yCalib)), ("10.52.90.230", 2390))
                time.sleep(1)    
                
                # Read in all the UDP packets to empty the buffer
                empty_socket(sockMbed)
                # Collect a number of samples
                Samples0 = 0;
                Samples1 = 0;
                Samples2 = 0;
                Samples3 = 0;
                Samples4 = 0;
                
                # Get the required number of samples for each sonar
                while(Samples0 < numSamples or Samples1 < numSamples or Samples2 < numSamples or Samples3 < numSamples or Samples4 < numSamples):
                    data, addr = sockMbed.recvfrom(1024) # buffer size is 1024 bytes
                    # print "received message:", data
                    # Check if this is the right packet type
                    if(ord(data[0]) == 16):
                        sonarNum = ord(data[1])
                        if(sonarNum == 0 and Samples0 < numSamples):
                            sonarMeas = ord(data[2])*0x100 + ord(data[3])
                            #print "S", sonarNum, "  Val = ", sonarMeas
                            A0[Samples0,ix,iy] = sonarMeas
                            Samples0 = Samples0 + 1
                            #print sonarMeas
                        if(sonarNum == 1 and Samples1 < numSamples):
                            sonarMeas = ord(data[2])*0x100 + ord(data[3])
                            #print "S", sonarNum, "  Val = ", sonarMeas
                            A1[Samples1,ix,iy] = sonarMeas
                            Samples1 = Samples1 + 1
                            #print sonarMeas
                        if(sonarNum == 2 and Samples2 < numSamples):
                            sonarMeas = ord(data[2])*0x100 + ord(data[3])
                            #print "S", sonarNum, "  Val = ", sonarMeas
                            A2[Samples2,ix,iy] = sonarMeas
                            Samples2 = Samples2 + 1
                            #print sonarMeas
                        if(sonarNum == 3 and Samples3 < numSamples):
                            sonarMeas = ord(data[2])*0x100 + ord(data[3])
                            #print "S", sonarNum, "  Val = ", sonarMeas
                            A3[Samples3,ix,iy] = sonarMeas
                            Samples3 = Samples3 + 1
                            #print sonarMeas
                        if(sonarNum == 4 and Samples4 < numSamples):
                            sonarMeas = ord(data[2])*0x100 + ord(data[3])
                            #print "S", sonarNum, "  Val = ", sonarMeas
                            A4[Samples4,ix,iy] = sonarMeas
                            Samples4 = Samples4 + 1
                            #print sonarMeas
                        
            # Redraw the plot after each set of y values  
            plt.subplot(3,2,1)   
            plt.pcolor(X, Y, A0[5,:,:])
            plt.clim(0,5000)
            plt.subplot(3,2,2)   
            plt.pcolor(X, Y, A1[5,:,:])
            plt.clim(0,5000)
            plt.subplot(3,2,3)   
            plt.pcolor(X, Y, A2[5,:,:])
            plt.clim(0,5000)
            plt.subplot(3,2,4)   
            plt.pcolor(X, Y, A3[5,:,:])
            plt.clim(0,5000)
            plt.subplot(3,2,5)   
            plt.pcolor(X, Y, A4[5,:,:])
            plt.clim(0,5000)
            plt.draw()
        
            #print "Raising Y"
            # Send to the top of the range.
            sockRail.sendto("2,p0", ("10.52.90.230", 2390))
            time.sleep(3)    
            # Homing brings the axis against the collision stop
            sockRail.sendto("2,home", ("10.52.90.230", 2390))
            time.sleep(1)    
        
        # Write the collected data to a file
        f = open('data.csv', 'w')
        # First line contains the array size and x and y increment sizes
        f.write(str(numPointsX))
        f.write(',')
        f.write(str(numPointsY))
        f.write(',')
        f.write(str(numSamples))   # Samples at each point
        f.write(',')
        f.write(str(xInc_mm))
        f.write(',')
        f.write(str(yInc_mm))
        f.write(',')
        f.write(str(5))             # The number of Sonars in the file
        f.write('\n')
        
        # Each sucessive line contains all the samples for each data point
        for ix in range(0,numPointsX):
            for iy in range(0,numPointsY):
                for iz in range(0,numSamples-1):
                    f.write(str(A0[iz,ix,iy]))
                    f.write(',')        
                f.write(str(A0[numSamples-1,ix,iy]))
                f.write('\n')        

        # Each sucessive line contains all the samples for each data point
        for ix in range(0,numPointsX):
            for iy in range(0,numPointsY):
                for iz in range(0,numSamples-1):
                    f.write(str(A1[iz,ix,iy]))
                    f.write(',')        
                f.write(str(A1[numSamples-1,ix,iy]))
                f.write('\n')        
                
        # Each sucessive line contains all the samples for each data point
        for ix in range(0,numPointsX):
            for iy in range(0,numPointsY):
                for iz in range(0,numSamples-1):
                    f.write(str(A2[iz,ix,iy]))
                    f.write(',')        
                f.write(str(A2[numSamples-1,ix,iy]))
                f.write('\n')        
                
        # Each sucessive line contains all the samples for each data point
        for ix in range(0,numPointsX):
            for iy in range(0,numPointsY):
                for iz in range(0,numSamples-1):
                    f.write(str(A3[iz,ix,iy]))
                    f.write(',')        
                f.write(str(A3[numSamples-1,ix,iy]))
                f.write('\n')        

        # Each sucessive line contains all the samples for each data point
        for ix in range(0,numPointsX):
            for iy in range(0,numPointsY):
                for iz in range(0,numSamples-1):
                    f.write(str(A4[iz,ix,iy]))
                    f.write(',')        
                f.write(str(A4[numSamples-1,ix,iy]))
                f.write('\n')        

        f.close()
        
   

