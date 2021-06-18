#Numpy
import numpy as np
#Fits opening
from astropy.io import fits
from image_processor import *

imgproc = ImageProcessor()
imgproc.add_process(EqualHist())

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
