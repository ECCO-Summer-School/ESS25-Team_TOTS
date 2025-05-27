
# To run this python3.8 ampli_phase_maps_1month.py on pcluster
# CHANGE THE WRITING FOLDERS. Reading folders should be ok
#This script takes 1 month of data
from utide import solve, reconstruct
import utide
from xmitgcm import open_mdsdataset
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from os.path import expanduser,join,isdir
import sys
user_home_dir = expanduser('~')
#ecco_v4_py_dir = join(user_home_dir,'ECCOv4-py')
#if isdir(ecco_v4_py_dir):
#    sys.path.insert(0,ecco_v4_py_dir)
#from ecco_v4_py import plot_proj_to_latlon_grid
#import ecco_v4_py as ecco
import pandas as pd


#data_dir ='/efs_ecco/hvanderz/export_tides'
data_dir='/efs_ecco/hplombat/Hugo_tidal_maps/ETAN_1month/'
grid_dir ='/efs_ecco/hvanderz/r5/WORKINGDIR/ECCOV4/release5_ToTs/run'
#ds = open_mdsdataset(data_dir, grid_dir=grid_dir, prefix={'ETAN'}) #native grid
ds_llc = open_mdsdataset(data_dir, 
                        grid_dir=grid_dir, 
                         prefix={'ETAN'},
                         geometry="llc") #non-native grid

# display the contents of the Dataset
ds_llc = ds_llc.rename({'face':'tile'})

n_files = len(ds_llc.time)              # number of data files
start_time = '1993-03-01'    # starting date
freq = 'h'                   # time frequency (e.g. 'h
dates = pd.date_range(start=start_time, periods=n_files, freq=freq)
#print(len(dates))
ntile=13
ni=90
nj=90

#print(len(ds_llc.time.values))
def amp_phase(time,ssh,latp):
#    try:
    
    #print(len(time),len(ssh),latp)
    coef = solve( t = time,
                  u = ssh,
                  lat=latp,
                  nodal=False,
                  trend=False,
                  method="ols",
                  conf_int="none"
                 )
    #print(coef['name'])
    #print(coef['A'])
    #idx = np.where(coef['name'] == 'M2')[0]
    #print('idx=', idx)
    #if len(idx) > 0:
    return coef['A'][0], coef['g'][0]  # Amplitude, Phase
#else:
#        return np.nan, np.nan
    #except:
    #    print('B')
    #    return np.nan, np.nan


def loop_1tile(ttile, time,ds):
    lat = ds_llc['YC'].isel(tile=ttile).values
    amp_map = np.full((ni, ni), np.nan)
    pha_map = np.full((nj, nj), np.nan)
    #amp_map = np.full((3, 3), np.nan)                                                                                                                                             
    #pha_map = np.full((3, 3), np.nan) 
    #print('TESTloop1tile', ds_llc.ETAN.isel(tile=ttile,i=0,j=0).values)
    for ii in range(ni):#ni
        for jj in range(nj):#nj
            #print('III', ii ,'JJJ', jj)
            sshp = ds[:,ii,jj]#ds_llc.ETAN.isel(tile=ttile,i=ii,j=jj).values,#ds_t4[:,ii,jj] # ds_llc.isel(tile=ttile, i=ii,j=jj).ETAN.values
            #print('SSH', sshp)
            latpp=  lat[ii,jj]# ds_llc['YC'].isel(tile=ttile, j=jj, i=ii).values
            #print('lat', latpp)
            amp_map[ii, jj], pha_map[ii, jj] = amp_phase(time,sshp,latpp)
    
    return amp_map, pha_map
def loop_tiles(ds):
    for tilenum in (range(ntile)):
        print('TILE NUMBER', tilenum)
        #print(ds['YC'].isel(tile=tilenum).values)
        #latitude= ds['YC'].isel(tile=0).values

#        latitude = []
        #print('LAT',latitude)
        ds=  ds_llc.ETAN.isel(tile=tilenum).values
        # print('youuuu',ds,np.shape(ds))
        #print(ds.shape)
        amp_M2, pha_M2 = loop_1tile(ttile = tilenum, time  = dates, ds = ds)
       # print(amp_M2, pha_M2)
       # np.savetxt('./maps_1month/amp_M2_'+str(tilenum)+'.txt', amp_M2)
       # np.savetxt('./maps_1month/pha_M2_'+str(tilenum)+'.txt', pha_M2)


#a,b=amp_phase(dates, ds_t4[:,3,3],latitude_t4[3,3])
#print(a)
#print(b)

loop_tiles(ds_llc)


#XXX= ds_llc['YC'].isel(tile=0).values
#print(XXX)
#XXX= ds_llc['YC'].isel(tile=4).values
#print(XXX)

#print(ds_llc.ETAN.isel(tile=4,i=0,j=0).values,len(ds_llc.ETAN.isel(tile=4,i=0,j=0).values))
#amp_M2, pha_M2 = loop_1tile(ttile = 4, time  = dates)
#np.savetxt('./maps/amp_M2', amp_M2)
#np.savetxt('./maps/pha_M2', pha_M2)
