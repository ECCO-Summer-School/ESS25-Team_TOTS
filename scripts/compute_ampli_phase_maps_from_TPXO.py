'''
This script computes the amplitude and phase maps of 15 components  from TPXO9.1 model
It uses the package pytmd (https://pytmd.readthedocs.io/en/latest/)

'''
# To run this python3.8 ampli_phase_maps_1month.py on pcluster                                                                                                                         
# CHANGE THE WRITING FOLDERS. Reading folders should be ok   

from utide import solve, reconstruct
import utide
from xmitgcm import open_mdsdataset
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from os.path import expanduser,join,isdir
import sys

import pandas as pd
import pyTMD.crs
import pyTMD.io
import pyTMD.tools
from pyTMD.solve import constants
from datetime import datetime, timedelta
import pyTMD
import xarray as xr
import time

#Informative only, the constituents which are fitted.
#constituents = ['m2', 's2', 'n2', 'k2','k1', 'o1', 'p1', 'q1']#, 'mm', 'mf', 'm4', 'mn4', 'ms4', '2n2']


# available model list
model_list = sorted(pyTMD.io.model.ocean_elevation())

# get model parameters
model = pyTMD.io.model('/efs_ecco/hplombat/TMD', #TOCHANGE: path of the TPXO data
                       compressed= False
                       ).elevation('TPXO9.1')

# read tidal constants and interpolate to grid points
if model.format in ('OTIS','ATLAS-compact','TMD3'):
    # if reading a single OTIS solution
    xi,yi,hz,mz,iob,dt = pyTMD.io.OTIS.read_otis_grid(model.grid_file)


def amp_phase(longit, latit):
    '''
     Returns amplitude and phase of tidal constituents, bathymetry of tidal model, and list of tidal constituents
    '''
    amp,ph,D,c = pyTMD.io.OTIS.extract_constants(longit,latit, model.grid_file, model.model_file, 4326,
                                                 type='z',
                                                 method= 'bilinear', 
                                                 grid='OTIS')
    return amp, ph 



def make_map():                                                                                                                                                                            # Returns amplitude and phase of tidal constituents, bathymetry of tidal model, and list of tidal constituents
    longitude = np.arange(0,361)
    latitude = np.arange(-90,91)
    lon2d,lat2d = np.meshgrid(longitude,latitude) # We want to treat the whole map at once, but the function only takes longitude and latitude arrays of equal size
    lonflat = lon2d.ravel() #packs 2d array in 1d array
    latflat= lat2d.ravel() 
    amp,ph,D,components = pyTMD.io.OTIS.extract_constants(lonflat,latflat, model.grid_file, model.model_file, 4326,
                                                 type='z',
                                                 method='bilinear',
                                                 grid='OTIS')
    ny, nx = lon2d.shape     # e.g. (180, 180)
    n_constituents = amp.shape[1]  # should be 15
    # Now reshape into (ny, nx, n_constituents)
    amp_grid = amp.reshape(ny, nx, n_constituents)
    ph_grid  = ph.reshape(ny, nx, n_constituents)
    print(components)
    for c in range(len(components)): #CHANGE the writing path 
        np.savetxt('./test/ampli_ll_txpo_'+str(components[c])+'.txt',amp_grid[:,:,c])
        np.savetxt('./test/ph_ll_txpo_'+str(components[c])+'.txt',ph_grid[:,:,c])
make_map()


            
