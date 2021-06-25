#!/usr/bin/env python

#Imports:
#Numpy
import numpy as np
#Fits opening
from astropy.io import fits
#image processor class
from image_processor import *
#GUI
import wx

# Test Data & Processing
imgproc = ImageProcessor()
imgproc.add_process(Process("equal_hist"))
imgproc.add_process(Process("gamma_corr", 3))
imgproc.add_process(Process("log_corr",3))
imgproc.add_process(Process("chop", [1, 100]))
imgproc.add_process(Process("denoise", 0.1))
imgproc.add_process(Process("destar", 1))

f = fits.open("NGC_5257_SDSS_u.fits")
input = f[0].data

imgproc.set_input(input)
output = imgproc.process()

from matplotlib import pyplot as plt
fig = plt.figure()
frame = fig.add_subplot(1, 2, 1)
frame.imshow(input)
frame = fig.add_subplot(1, 2, 2)
frame.imshow(output)
plt.show()
