import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits
import sys
from astropy import wcs
import math as mt
import numpy as np

def main():
	fname = sys.argv[1]

	a = fits.open(fname)
	image_file = get_pkg_data_filename(fname)
	fits.info(image_file)

	image_data = fits.getdata(image_file, ext=1)
	plt.figure()
	plt.imshow(image_data, cmap='binary')
	plt.colorbar()
	image_data = fits.getdata(image_file, ext=2)
	print(image_data.shape)
	plt.figure()
	plt.imshow(image_data, cmap='binary')
	plt.colorbar()
	image_data = fits.getdata(image_file, ext=3)
	print(image_data.shape)
	plt.figure()
	plt.imshow(image_data, cmap='binary')
	plt.colorbar()
	plt.show()



main()