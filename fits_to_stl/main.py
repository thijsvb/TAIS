#Imports
#Numpy
import numpy as  np
#Fits opening
from astropy.io import fits
#Plotting
from matplotlib.pyplot import figure, show
#image manipulation
import cv2
#custom code
from data_to_stl import *

# Open file
f = fits.open("NGC_4594_SDSS_i bms2014.fits")
data = f[0].data
#prep then log data to make peaks less steep
data -= data.min()
data += 1
# data = np.log10(np.log10(data)+1)
data = np.log10(data)

# scale data resolution
Nres = int(50//0.3) # rough estimation for needed array length based on nozzle size (0.3) and model size (50)
data = cv2.resize(data, (Nres,Nres), interpolation=cv2.INTER_NEAREST)

# cut of noise
thold = 0.2
data -= thold
ncols, nrows = data.shape
for i in range(ncols):
    for j in range(nrows):
        if data[i][j] < 0:
            data[i][j] = 0

# plot data
fig = figure()
frame = fig.add_subplot(1, 2, 1)
frame.imshow(data, cmap="Greys")
frame = fig.add_subplot(1, 2, 2)
frame.hist(data.flatten(), bins=100)
show()

size = (50, 50, 11) #x,y,z in mm
#Creating the list of faces out of the array
data_to_stl("sombrero_downscaled_noisecutoff.stl",data,size)

#TEST DATA
# # Initializing value of x-axis and y-axis
# # in the range 0 to 1
# x, y = np.meshgrid(np.linspace(0,1,10), np.linspace(0,1,10))
# dst = np.sqrt(x*x+y*y)
#
# # Intializing sigma and muu
# sigma = 1
# muu = 0.500
#
# # Calculating Gaussian array
# testdata = np.exp(-( (dst-muu)**2 / ( 2.0 * sigma**2 ) ) )
