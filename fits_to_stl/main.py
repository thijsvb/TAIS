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
size = (80, 80, 5) #x,y,z in mm

# Open file
f = fits.open("../../Data/m51_B_band_cor.fits")
data = f[0].data
# raw = data.copy()
# f = fits.open("../../Data/m51_R_band_cor.fits")
# f = fits.open("../../Data/m101_R_band_cor.fits")
raw = data.copy()

# IMAGE PROCESSING

# chop
floor, ceil = -15, None
if not floor is None:
    mask = data < floor
    data[mask] = floor
if not ceil is None:
    mask = data > ceil
    data[mask] = ceil
chopped = data.copy()

#equalize histogram
data = exposure.equalize_hist(data, nbins=256, mask="none")
eqhist = data.copy()

# gamma correction
# data = exposure.adjust_gamma(data, 2)
# gamcor = data.copy()

# log correction
# data = exposure.adjust_log(data, 10)
# logcor = data.copy()

# denoise
# data = restoration.denoise_tv_chambolle(data, weight=0.1, multichannel=False)
# denoise = data.copy()

# tophat filter
# selem = morphology.disk(1)
# res = morphology.white_tophat(data, selem)
# data = data - res
# destar = data.copy()

# f = 7
# data = transform.downscale_local_mean(data, (f, f))

# plot data
if True:
    imgA = eqhist
    imgB = data

    fig = figure()
    frame = fig.add_subplot(2, 2, 1)
    im = frame.imshow(imgA, cmap="Greys_r")
    fig.colorbar(im, ax=frame)
    frame = fig.add_subplot(2, 2, 2)
    frame.hist(imgA.flatten(), bins=256)
    frame = fig.add_subplot(2, 2, 3)
    im = frame.imshow(imgB, cmap="Greys_r")
    fig.colorbar(im, ax=frame)
    frame = fig.add_subplot(2, 2, 4)
    frame.hist(imgB.flatten(), bins=256)
    show()


data_to_stl("m51_B.stl", data, size, base_off=3)

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
