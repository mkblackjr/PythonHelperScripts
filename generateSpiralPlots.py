# generateSpiralPlots.py

import numpy as np
import plotData as p
import matplotlib.pyplot as plt

# Physical Parameters
R = 286.9 # J/kg/K
K = 273.15 # K

# Initializations
time = []; lat = []; lon = []; alt = []; temp = []; pres = []; dens = []
filepath = "/Users/mac/Documents/PythonScripts/20170921131853.txt"

# Read data from file
with open(filepath,'r') as f:
	for line in f:
		fields = line.split(',')
		# Convert txt data (string) to float
		try:
			time.append(float(fields[0]))
			lat.append(float(fields[1]))
			lon.append(float(fields[2]))
			alt.append(float(fields[3]))
			temp.append(float(fields[4]))
			pres.append(float(fields[5]))
			dens.append(100*float(fields[5])/(R*(float(fields[4])+K)))
		except:
			print("Skipping header.\n")
	f.close()

# # Define the regions of ascent and descent for the three spiral maneuvers
s1start = time.index(134636.5); s1top = time.index(141125.5); s1end = time.index(142619)
s2start = time.index(144431); s2top = time.index(150527.5); s2end = time.index(152359.5)
s3start = s2end; s3top = time.index(154333); s3end = time.index(160045)

climb1 = alt[s1start:s1top]; dec1 = alt[s1top:s1end]
climb1temp = temp[s1start:s1top]; dec1temp = temp[s1top:s1end]
climb1pres = pres[s1start:s1top]; dec1pres = pres[s1top:s1end]
climb1dens = dens[s1start:s1top]; dec1dens = dens[s1top:s1end]

climb2 = alt[s2start:s2top]; dec2 = alt[s2top:s2end]
climb2temp = temp[s2start:s2top]; dec2temp = temp[s2top:s2end]
climb2pres = pres[s2start:s2top]; dec2pres = pres[s2top:s2end]
climb2dens = dens[s2start:s2top]; dec2dens = dens[s2top:s2end]

climb3 = alt[s3start:s3top]; dec3 = alt[s3top:s3end] 
climb3temp = temp[s3start:s3top]; dec3temp = temp[s3top:s3end]
climb3pres = pres[s3start:s3top]; dec3pres = pres[s3top:s3end]
climb3dens = dens[s3start:s3top]; dec3dens = dens[s3top:s3end]

# Plot settings
titles = ["20170921 - Spiral 1","20170921 - Spiral 2","20170921 - Spiral 3"]
x_labels = ["Altitude (m)","Altitude (m)","Altitude (m)"]
y_labels = ["Temperature (°C)","Pressure (hPa)","Density (kg/m^3)"]
legend = ["Ascending", "Descending"]

# # Plot altitude v time for insight into flight path
# p.plotData(time[start:num_entries+start],alt[start:num_entries+start],titles[0],x_labels,y_labels,1)

# # Configure and plot the parameters of interest (ascent and descent) versus altitude
spiral1alt = [climb1,dec1,climb1,dec1,climb1,dec1]
spiral1data = [climb1temp,dec1temp,climb1pres,dec1pres,climb1dens,dec1dens]
p.plotData(spiral1alt,spiral1data,titles[0],x_labels,y_labels,legend,'Spiral1_20170921.pdf',3)

spiral2alt = [climb2,dec2,climb2,dec2,climb2,dec2]
spiral2data = [climb2temp,dec2temp,climb2pres,dec2pres,climb2dens,dec2dens]
p.plotData(spiral2alt,spiral2data,titles[1],x_labels,y_labels,legend,'Spiral2_20170921.pdf',3)

spiral3alt = [climb3,dec3,climb3,dec3,climb3,dec3]
spiral3data = [climb3temp,dec3temp,climb3pres,dec3pres,climb3dens,dec3dens]
p.plotData(spiral3alt,spiral3data,titles[2],x_labels,y_labels,legend,'Spiral3_20170921.pdf',3)