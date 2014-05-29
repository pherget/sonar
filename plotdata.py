# -*- coding: utf-8 -*-
"""
Created on Tue May  6 20:18:19 2014

@author: Phil
"""

soundSpeed = 340   # m/s

import matplotlib.pyplot as plt
import numpy as np

f = open("data/data.csv", 'r')

# The first line contains the size of the array
line = f.readline()
vals = line.split(',')
numPointsX = int(vals[0])
numPointsY = int(vals[1])
numSamples = int(vals[2])
xInc_mm = float(vals[3])
yInc_mm = float(vals[4])
numSonars = int(vals[5])

# Create Arrays of Zeros
X = np.zeros((numPointsX, numPointsY))
Y = np.zeros((numPointsX, numPointsY))
A0 = np.zeros((numSamples, numPointsX, numPointsY))
A1 = np.zeros((numSamples, numPointsX, numPointsY))
A2 = np.zeros((numSamples, numPointsX, numPointsY))
A3 = np.zeros((numSamples, numPointsX, numPointsY))
A4 = np.zeros((numSamples, numPointsX, numPointsY))
STD0 = np.zeros((numPointsX, numPointsY))
STD1 = np.zeros((numPointsX, numPointsY))
STD2 = np.zeros((numPointsX, numPointsY))
STD3 = np.zeros((numPointsX, numPointsY))
STD4 = np.zeros((numPointsX, numPointsY))
MED0 = np.zeros((numPointsX, numPointsY))
MED1 = np.zeros((numPointsX, numPointsY))
MED2 = np.zeros((numPointsX, numPointsY))
MED3 = np.zeros((numPointsX, numPointsY))
MED4 = np.zeros((numPointsX, numPointsY))
MEAN0 = np.zeros((numPointsX, numPointsY))
MEAN1 = np.zeros((numPointsX, numPointsY))
MEAN2 = np.zeros((numPointsX, numPointsY))
MEAN3 = np.zeros((numPointsX, numPointsY))
MEAN4 = np.zeros((numPointsX, numPointsY))

S0 = np.zeros((numPointsX, numPointsY))
S1 = np.zeros((numPointsX, numPointsY))
Combined = np.zeros((numPointsX, numPointsY))
Combined2 = np.zeros((numPointsX, numPointsY))

# Fill in the X and Y positions
for ix in range(numPointsX):
    for iy in range(numPointsY):
        X[ix][iy] = xInc_mm*ix
        Y[ix][iy] = yInc_mm*(numPointsY-1-iy)

# Each following line contains data
for ix in range(0,numPointsX):
    for iy in range(0,numPointsY):
        line = f.readline()
        vals = line.split(',')
        for iz in range(0,numSamples-1):
            # Read in and convert to mm (/2 andles out and back)
            A0[iz,ix,iy] = float(vals[iz])/1000*soundSpeed/2   
        # Calculate the standard deviation
        STD0[ix][iy] = np.std(A0[0:19,ix,iy])
        MED0[ix][iy] = np.median(A0[0:19,ix,iy])        
        MEAN0[ix][iy] = np.mean(A0[0:19,ix,iy])                
        S0[ix][iy] = MED0[ix,iy] > 2000

if(numSonars > 1):
    # Each following line contains data
    for ix in range(0,numPointsX):
        for iy in range(0,numPointsY):
            line = f.readline()
            vals = line.split(',')
            for iz in range(0,numSamples-1):
                # Read in and convert to mm (/2 andles out and back)
                A1[iz,ix,iy] = float(vals[iz])/1000*soundSpeed/2   
            # Calculate the standard deviation
            STD1[ix][iy] = np.std(A1[0:19,ix,iy])
            MED1[ix][iy] = np.median(A1[0:19,ix,iy])        
            MEAN1[ix][iy] = np.mean(A1[0:19,ix,iy])                
            S1[ix][iy] = MED1[ix,iy] < 2000

if(numSonars > 2):
    # Each following line contains data
    for ix in range(0,numPointsX):
        for iy in range(0,numPointsY):
            line = f.readline()
            vals = line.split(',')
            for iz in range(0,numSamples-1):
                # Read in and convert to mm (/2 andles out and back)
                A2[iz,ix,iy] = float(vals[iz])/1000*soundSpeed/2   
            # Calculate the standard deviation
            STD2[ix][iy] = np.std(A2[0:19,ix,iy])
            MED2[ix][iy] = np.median(A2[0:19,ix,iy])        
            MEAN2[ix][iy] = np.mean(A2[0:19,ix,iy])                

if(numSonars > 3):
    # Each following line contains data
    for ix in range(0,numPointsX):
        for iy in range(0,numPointsY):
            line = f.readline()
            vals = line.split(',')
            for iz in range(0,numSamples-1):
                # Read in and convert to mm (/2 andles out and back)
                A3[iz,ix,iy] = float(vals[iz])/1000*soundSpeed/2   
            # Calculate the standard deviation
            STD3[ix][iy] = np.std(A3[0:19,ix,iy])
            MED3[ix][iy] = np.median(A3[0:19,ix,iy])        
            MEAN3[ix][iy] = np.mean(A3[0:19,ix,iy])                

if(numSonars > 4):
    # Each following line contains data
    for ix in range(0,numPointsX):
        for iy in range(0,numPointsY):
            line = f.readline()
            vals = line.split(',')
            for iz in range(0,numSamples-1):
                # Read in and convert to mm (/2 andles out and back)
                A4[iz,ix,iy] = float(vals[iz])/1000*soundSpeed/2   
            # Calculate the standard deviation
            STD4[ix][iy] = np.std(A4[0:19,ix,iy])
            MED4[ix][iy] = np.median(A4[0:19,ix,iy])        
            MEAN4[ix][iy] = np.mean(A4[0:19,ix,iy]) 
            Combined2[ix][iy] = min(MED0[ix][iy], MED1[ix][iy], MED2[ix][iy], MED3[ix][iy], MED4[ix][iy])               


# Construct a plot for the overlap between S1 and S2
for ix in range(0,numPointsX):
    for iy in range(0,numPointsY):
         Combined[ix][iy] = 10;        
         if(S0[ix][iy]==1 and S1[ix][iy]==0):
             Combined[ix][iy] = 1;
         if(S0[ix][iy]==0 and S1[ix][iy]==1):
             Combined[ix][iy] = 1.5;
         if(S0[ix][iy]==1 and S1[ix][iy]==1):
             Combined[ix][iy] = 1.25;
# Add one patch of a different color to ensure the full scale in the image

zLim = 850

######## Sensor 1 data
fig = plt.figure(1)
plt.subplot(2,2,1)
plt.ion()
plt.pcolor(X, Y, A0[0,:,:])
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Single Point')
plt.ylabel('Distance (mm)')
plt.clim(0,zLim)

plt.subplot(2,2,2)
plt.pcolor(X, Y, STD0)
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Standard Dev')

plt.subplot(2,2,3)
plt.pcolor(X, Y, MEAN0)
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Mean')
plt.ylabel('Distance (mm)')
plt.xlabel('Distance (mm)')
plt.clim(0,zLim)

plt.subplot(2,2,4)
plt.pcolor(X, Y, MED0)
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Median')
plt.xlabel('Distance (mm)')
plt.clim(0,zLim)
plt.show()
plt.draw()

######## Sensor 2 data
fig = plt.figure(2)
plt.subplot(2,2,1)
plt.ion()
plt.pcolor(X, Y, A1[0,:,:])
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Single Point')
plt.ylabel('Distance (mm)')
plt.clim(0,zLim)

plt.subplot(2,2,2)
plt.pcolor(X, Y, STD1)
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Standard Dev')

plt.subplot(2,2,3)
plt.pcolor(X, Y, MEAN1)
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Mean')
plt.ylabel('Distance (mm)')
plt.xlabel('Distance (mm)')
plt.clim(0,zLim)

plt.subplot(2,2,4)
plt.pcolor(X, Y, MED1)
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Median')
plt.xlabel('Distance (mm)')
plt.clim(0,zLim)
plt.show()
plt.draw()

######## Sensor 3 data
fig = plt.figure(3)
plt.subplot(2,2,1)
plt.ion()
plt.pcolor(X, Y, A2[0,:,:])
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Single Point')
plt.ylabel('Distance (mm)')
plt.clim(0,zLim)

plt.subplot(2,2,2)
plt.pcolor(X, Y, STD2)
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Standard Dev')

plt.subplot(2,2,3)
plt.pcolor(X, Y, MEAN2)
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Mean')
plt.ylabel('Distance (mm)')
plt.xlabel('Distance (mm)')
plt.clim(0,zLim)

plt.subplot(2,2,4)
plt.pcolor(X, Y, MED2)
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Median')
plt.xlabel('Distance (mm)')
plt.clim(0,zLim)
#plt.colorbar()
plt.show()
plt.draw()

######### Combined Data
fig = plt.figure(10)
plt.pcolor(X, Y, Combined, cmap='spectral')
# Set the 'Z' limits from 0 to 10
plt.clim(0,10)
plt.title('Two Sensor')
plt.ylabel('Distance (mm)')
plt.show()
plt.draw()

fig = plt.figure(11)
plt.pcolor(X, Y, Combined2)
# Set the 'Z' limits from 0 to 10
plt.title('Min of All Sensors')
plt.ylabel('Distance (mm)')
plt.colorbar()
plt.show()
plt.draw()

######### All Medians on one plot
fig = plt.figure(12)
plt.subplot(2,3,2)
plt.ion()
plt.pcolor(X, Y, MED0)
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Median - Sensor 0')
plt.ylabel('Distance (mm)')
plt.clim(0,zLim)

plt.subplot(2,3,3)
plt.ion()
plt.pcolor(X, Y, MED1)
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Median - Sensor 1')
plt.ylabel('Distance (mm)')
plt.clim(0,zLim)

plt.subplot(2,3,1)
plt.ion()
plt.pcolor(X, Y, MED2)
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Median - Sensor 2')
plt.ylabel('Distance (mm)')
plt.clim(0,zLim)
plt.show()
plt.draw()

plt.subplot(2,3,4)
plt.ion()
plt.pcolor(X, Y, MED3)
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Median - Sensor 2')
plt.ylabel('Distance (mm)')
plt.clim(0,zLim)
plt.show()
plt.draw()

plt.subplot(2,3,6)
plt.ion()
plt.pcolor(X, Y, MED4)
plt.axis([0, (numPointsX-1)*xInc_mm, 0, (numPointsY-1)*yInc_mm])
plt.title('Median - Sensor 2')
plt.ylabel('Distance (mm)')
plt.clim(0,zLim)
plt.show()
plt.draw()
