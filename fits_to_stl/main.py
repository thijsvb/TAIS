#Imports
#Numpy
import numpy as  np
#Fits opening
from astropy.io import fits
#Plotting
from matplotlib.pyplot import figure, show
#image manipulation
from skimage import data, io, exposure, filters, restoration, morphology, transform
#custom code
from data_to_stl import *

# Open file
f = fits.open("NGC_4594_SDSS_i bms2014.fits")
data = f[0].data

# #prep then log data to make peaks less steep
# data -= data.min()
# data += 1
# # data = np.log10(np.log10(data)+1)
# data = np.log10(data)

# IMAGE PROCESSING
# scale data resolution
Nres = int(50//0.3) # rough estimation for needed array length based on nozzle size (0.3) and model size (50)
scalef = data.shape[0]//Nres
data = transform.downscale_local_mean(data, (scalef, scalef))
# chop
# mask = data > 25
# data[mask] = 25
#equalize histogram
data = exposure.equalize_hist(data, nbins=256, mask="none")
# gamma correction
data = exposure.adjust_gamma(data, 2)
# log correction
data = exposure.adjust_log(data, 3)
logcor = data.copy()
# denoise
# data = restoration.denoise_tv_chambolle(data, weight=0.05, multichannel=False)
# tophat filter
selem = morphology.disk(1)
res = morphology.white_tophat(data, selem)
data = data - res

# plot data
fig = figure()
frame = fig.add_subplot(2, 2, 1)
frame.imshow(data, cmap="Greys")
frame = fig.add_subplot(2, 2, 2)
frame.hist(data.flatten(), bins=100)
frame = fig.add_subplot(2, 2, 3)
frame.imshow(logcor, cmap="Greys")
frame = fig.add_subplot(2, 2, 4)
frame.hist(logcor.flatten(), bins=100)
show()

size = (50, 50, 11) #x,y,z in mm
#Creating the list of faces out of the array
data_to_stl("sombrero_skimaged.stl",data,size)

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
