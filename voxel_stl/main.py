#Imports
#Numpy
import numpy as  np
#Fits opening
from astropy.io import fits
#Plotting
from matplotlib.pyplot import figure, show
#custom code
from data_to_stl import *

# Open file
f = fits.open("NGC_4594_SDSS_i bms2014.fits")
data = f[0].data
#prep then log data to make peaks less steep
data -= data.min()
data += 1
data = np.log(data)

size = (50, 50, 11) #x,y,z in mm
#Creating the list of faces out of the array
data_to_stl("sombrero_low.stl",data,size)

# #TEST DATA
# # # Initializing value of x-axis and y-axis
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
# size = (50, 50, 25) #x,y,z in mm
#
# data_to_stl("test.stl", testdata, size)
