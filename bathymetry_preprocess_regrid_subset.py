#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 11:48:31 2023

@author: rgq13jzu
"""



import os

import iris
import iris.plot as iplt
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import pdb
import numpy as np


import warnings



###########
# Choose place of work

# Ada
DATADIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data','glorys12v1aeq1_zlev_d','raw');
GRIDDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data')
OUTDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data','glorys12v1aeq1erai_zlev_d','processed');
PLOTDIR=os.path.join(os.path.sep,'gpfs','home','rgq13jzu','MJO_scripts','tmp')

###########
#


VAR_NAME='deptho'

# Latitudes of dataset to be regridded
LAT_MIN=-15 
LAT_MAX=15

# Latitude band for subsetting regridded data
LAT_BAND_MIN=-1.5 
LAT_BAND_MAX=1.5


PLOTTING=True # Boolean: True for making and saving plots
SAVE_RESULT=False # Boolean: True to save results cube (will overwrite old cubes)



#
###
###############################
###############################  Load the data and package it up ready for the plotting, find extreme values while there




# Load bathymetry data cube
bathyfilename=VAR_NAME+'.nc'
file1=os.path.join(DATADIR,bathyfilename)
print('file1: {0!s}'.format(file1))
cubelist=iris.load(file1)   # Loads in a Cubelist of cubes
cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist
cube.coord(axis='x').guess_bounds()
cube.coord(axis='y').guess_bounds()


# Load target grid data cube
gridfile=os.path.join(GRIDDIR,'erainterim_plev_6h','std','uwnd_850_1998.nc')
print('gridfile: {0!s}'.format(gridfile))
cubelist=iris.load(gridfile)   # Loads in a Cubelist of cubes
gridcube=cubelist.concatenate_cube() #This line makes a cube from the cubelist

# Extract the part of target cube grid cube that is in -15S to 15N
tol=0.001
gridcubeconstraint=iris.Constraint(latitude=lambda cell: LAT_MIN-tol <= cell <= LAT_MAX+tol)
gridcube=gridcube.extract(gridcubeconstraint)
gridcube.coord(axis='x').guess_bounds()
gridcube.coord(axis='y').guess_bounds()



regridded_cube=cube.regrid(gridcube,iris.analysis.AreaWeighted())




subsetcubeconstraint=iris.Constraint(latitude=lambda cell: LAT_BAND_MIN-tol <= cell <= LAT_BAND_MAX+tol)
subsetcube=regridded_cube.extract(subsetcubeconstraint)


equatorial_cube=subsetcube.collapsed('latitude',iris.analysis.MEAN,weights=iris.analysis.cartography.area_weights(subsetcube))




if SAVE_RESULT:
    fileout=os.path.join(OUTDIR,'deptho_ss_lat_'+str(LAT_BAND_MIN)+'_'+str(LAT_BAND_MAX)  +  '.nc')
    print('fileout:', fileout)
    iris.save(equatorial_cube,fileout)







if PLOTTING:
    PLOTCONTOURLEVELS=[1000*level for level in range(0,10+1)]
    # Plot original
    fig1=plt.figure()
    qplt.contourf(cube,levels=PLOTCONTOURLEVELS)
    IMAGEFILE=os.path.join(PLOTDIR,'bathymetry_raw.png')
    fig1.savefig(IMAGEFILE)
    print('Figure saved to: '+IMAGEFILE)
    # Plot regridded
    fig2=plt.figure()
    qplt.contourf(regridded_cube,levels=PLOTCONTOURLEVELS)
    IMAGEFILE2=os.path.join(PLOTDIR,'bathymetry_regridded.png')
    fig2.savefig(IMAGEFILE2)
    print('Figure saved to: '+IMAGEFILE2)
    # Plot subsetted to equator
    fig3=plt.figure()
    longs=equatorial_cube.coord('longitude').points
    plt.plot(longs,-1*equatorial_cube.data)
    masked_points=longs[equatorial_cube.data.mask]
    plt.plot(masked_points,0*masked_points,linestyle='None',marker='.',color='red')
    IMAGEFILE3=os.path.join(PLOTDIR,'bathymetry_equatorial_subset.png')
    fig3.savefig(IMAGEFILE3)
    print('Figure saved to: '+IMAGEFILE3)
