import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

from astropy.utils.data import get_pkg_data_filename
from matplotlib.backends.backend_pdf import PdfPages
from astropy.io import fits
from astropy.io import ascii
import sys
from astropy import wcs
import math as mt
import numpy as np
import glob
from scipy.ndimage import filters
from scipy import stats

def main():

	writedir = '/home/conor/Galfit/Fits/'
	writedir1 = '/home/conor/Galfit/Fits2/'	
	writedir2 = '/home/conor/Galfit/Fits3/'
	asymmetries = '/home/conor/Galfit/asymmetries.txt'

	asyms = ascii.read(asymmetries)

	fits_list = sorted(glob.glob(writedir+'*.fits')) + sorted(glob.glob(writedir2 + '*.fits'))+sorted(glob.glob(writedir1+'*.fits'))
	j = 0
	for i in fits_list:
		name = i.split("_")[1]

		asymmetry = 'NA'


		for j in range(len(asyms['Names'])):
			if asyms['Names'][j] == name:
				asymmetry = asyms['Asymmetries'][j]
			else:
				continue


		fig, (ax1,ax2,ax3) = plt.subplots(nrows=1,ncols = 3)
		j+=1
		a = fits.open(i)
		image_file = get_pkg_data_filename(i)
		fits.info(image_file)

		image_data = fits.getdata(image_file, ext=1)
		simg = filters.gaussian_filter(image_data, .5)
		std = 1.4826 * stats.median_absolute_deviation(simg)
		std = np.median(std)
		ax1.imshow(image_data, cmap='binary',origin='lower')
		m1 = ax1.imshow(image_data, cmap='binary',origin='lower')
		cbar = fig.colorbar(m1, ax=ax1,shrink = .3)
		cbar.ax.tick_params(labelsize=7.5) 
		ax1.contour(simg,[std,2*std,3*std,4*std,5*std], colors='red',alpha = .3)
		m1 = ax1.contour(simg, [std,2*std,3*std,4*std,5*std],colors='red', alpha = .3)
		min = np.amin(simg)
		max = np.amax(simg)

		image_data = fits.getdata(image_file, ext=2)
		simg = filters.gaussian_filter(image_data, .5)
		ax2.imshow(image_data, cmap='binary',origin='lower')
		m2 = ax2.imshow(image_data, cmap='binary',vmin = min,vmax = max,origin='lower')
		cbar2 = fig.colorbar(m2,ax=ax2,shrink = .3)
		cbar2.ax.tick_params(labelsize=7.5)
		ax2.contour(simg,[std,2*std,3*std,4*std,5*std], colors='red',alpha =.3)
		m2 = ax2.contour(simg,[std,2*std,3*std,4*std,5*std], colors='red',vmin = min,vmax = max, alpha = .3)
		

		image_data = fits.getdata(image_file, ext=3)
		simg = filters.gaussian_filter(image_data, .5)
		ax3.imshow(image_data, cmap='binary',origin='lower')
		m3 = ax3.imshow(image_data, cmap='binary',vmin = min, vmax = max,origin='lower')
		cbar3 = fig.colorbar(m3,ax=ax3,shrink = .3)
		cbar3.ax.tick_params(labelsize=7.5) 

		ax1.tick_params(labelsize=8.5)
		ax2.tick_params(labelsize=8.5)
		ax3.tick_params(labelsize=8.5)

		if asymmetry != 'NA':

			asymmetry = round(asymmetry,3)

			asymmetry = str(asymmetry)

		plt.text(0, -7, 'A = ' + asymmetry)

		
		
		pp = PdfPages('/home/conor/Galfit/Contours/model_'+name+'.pdf')
		pp.savefig(fig)
		pp.close()



main()