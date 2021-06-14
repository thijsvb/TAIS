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

# model size
size = (50, 50, 5) #x,y,z in mm

# Open file
f = fits.open("NGC_5257_SDSS_u.fits")
data = f[0].data
raw = data.copy()

# IMAGE PROCESSING

#equalize histogram
data = exposure.equalize_hist(data, nbins=256, mask="none")
eqhist = data.copy()

# gamma correction
data = exposure.adjust_gamma(data, 10)
gamcor = data.copy()

# log correction
# data = exposure.adjust_log(data, 5)
# logcor = data.copy()

# chop
floor = 0.35
mask = data < floor
data[mask] = floor
chopped = data.copy()

# denoise
data = restoration.denoise_tv_chambolle(data, weight=0.03, multichannel=False)
denoise = data.copy()

# tophat filter
# selem = morphology.disk(1)
# res = morphology.white_tophat(data, selem)
# data = data - res
# destar = data.copy()

# plot data
if False:
    imgA = chopped
    imgB = denoise

    fig = figure()
    frame = fig.add_subplot(2, 2, 1)
    frame.imshow(imgA, cmap="Greys")
    frame = fig.add_subplot(2, 2, 2)
    frame.hist(imgA.flatten(), bins=100)
    frame = fig.add_subplot(2, 2, 3)
    frame.imshow(imgB, cmap="Greys")
    frame = fig.add_subplot(2, 2, 4)
    frame.hist(imgB.flatten(), bins=100)
    show()

#Creating the list of faces out of the array
data_to_stl("NGC5257_vert.stl", data, size, base_off=3)

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
