# Uses the package pyTMD to fit the tidal constituents.                                                                                                                         
# CHANGE THE WRITING FOLDERS. Reading folders should be ok   
from utide import solve, reconstruct
import utide
from xmitgcm import open_mdsdataset
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from os.path import expanduser,join,isdir
import sys
user_home_dir = expanduser('~')
import pandas as pd
import pyTMD.crs
import pyTMD.io
import pyTMD.tools
from pyTMD.solve import constants
from datetime import datetime, timedelta
import pyTMD
import xarray as xr

data_dir ='/efs_ecco/hvanderz/export_tides' #CHANGE: directory of ETAN files
grid_dir ='/efs_ecco/hvanderz/r5/WORKINGDIR/ECCOV4/release5_ToTs/run' #CHANGE: directory of grid files (e.g. XC.data)
ds_llc = open_mdsdataset(data_dir, 
                        grid_dir=grid_dir, 
                         prefix={'ETAN'},
                         geometry="llc") #non-native grid
# Rename to be consistent with ECCOV4-py
ds_llc = ds_llc.rename({'face':'tile'})

#We need to change the format of time to make it relative to the first day.
ds_llc['time'] = xr.cftime_range(start='1992-01-01T13:00:00', periods=ds_llc.dims['time'], freq='H')
ds_llc = ds_llc.unify_chunks()
ds_clm = ds_llc.groupby('time.month')#.mean('time')#ds_llc.mean('time')
ds_llc_anom = ds_llc.groupby('time.month') - ds_clm #Remove monthly mean of the signal

n_files = len(ds_llc_anom.time)              # number of data files                                                                                                                    
start_time = '1992-01-01 13:00:00'       # starting date of the simulation   
freq = 'h'                   # time frequency (e.g. hourly)                                                                  
time_eta = pd.date_range(start=start_time, periods=n_files, freq=freq)

epoch = datetime(1992, 1, 1, 0, 0, 0) 
dates = np.array([(ti.to_pydatetime() - epoch).total_seconds() / 86400.0 for ti in time_eta])

#CONSTITUENTS TO FIT
constituents = ['m2', 's2', 'n2', 'k2','k1', 'o1', 'p1', 'q1', 'mm', 'mf', 'm4', 'mn4', 'ms4', '2n2']

ntile=13
ni=90
nj=90

#compute the amplitude and phase from an ETAN time series.
def amp_phase(time,ssh,latp):
    amp_fit, phase_fit = constants(
    t=dates,
    ht=ssh,
    constituents=constituents,
    deltat=0.0,
    corrections='OTIS',
    solver='lstsq'
    )
    return amp_fit, phase_fit

#Function looping over all the i,j coordinates of 1 tile
def loop_1tile(ttile, time,ds):
    lat = ds_llc['YC'].isel(tile=ttile).values
    amp_map = np.full((len(constituents),ni, ni), np.nan)
    pha_map = np.full((len(constituents),nj, nj), np.nan)
    for ii in range(ni):
        for jj in range(nj):
            sshp = ds[:,ii,jj]
            latpp=  lat[ii,jj]
            amp_consts, pha_consts =  amp_phase(time,sshp,latpp) #len 15 lists (constituents)
            for c in range(len(constituents)):
                amp_map[c,ii, jj], pha_map[c,ii, jj] = amp_consts[c], pha_consts[c]
    return amp_map, pha_map

#Function looping over the tiles
def loop_tiles(ds):
    for tilenum in (range(ntile)):
        print('TILE NUMBER', tilenum)
        ds=  ds_llc.ETAN.isel(tile=tilenum).values
        amp_allconsts, pha_allconsts = loop_1tile(ttile = tilenum, time  = dates, ds = ds)
        amp_2d = amp_allconsts.reshape(amp_allconsts.shape[0], -1)#Flattens a 3d array (constituent,i,j) in a 2d array before saving it.
        pha_2d = pha_allconsts.reshape(pha_allconsts.shape[0], -1)
        #Saves 13 amplitude and phase files, one per tile.
        np.savetxt('./new_maps_mitgcm_1year/amp_comsts_'+str(tilenum)+'.txt', amp_2d) #CHANGE SAVE PATH
        np.savetxt('./new_maps_mitgcm_1year/pha_consts_'+str(tilenum)+'.txt', pha_2d)

loop_tiles(ds_llc)

