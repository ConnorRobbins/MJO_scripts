"""Create a spatially subsetted field using data_analysis.SpatialSubset."""

import datetime
import os

import iris.quickplot as qplt
import matplotlib.pyplot as plt
import pdb

import data_analysis as da

BASEDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data')
#BASEDIR=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')

#ARCHIVE=True
ARCHIVE=False  # If batch submitting: archive manually afterwards so you don't set fire to ADA :'(

BASEDIR_ARCHIVE=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')

#SUBDIR='std'       # : input data with time axis
SUBDIR='processed' # : input data with no time axis

# Optional
#TDOMAINID='rmm008FS-djf1'
#TDOMAINID='2003-to-2020'

#VAR_NAME='nsquared'; LEVEL='all'; SOURCE='glorys12v1aeq1erai_zlev_d'
#LEVEL='all'; SOURCE='glorys12v1aeq1erai_zlev_d'
LEVEL=1; SOURCE='era5gloerai_sfc_d'


# Compulsory band1
BAND1_NAME='latitude' # Dimension to average over: 'latitude' or 'longitude'
#BAND1_VAL1=-2.625 # TRMM precip for CCKW trajectories
#BAND1_VAL1=-10 # TRMM precip for CCKW trajectories
#BAND1_VAL1=-15 # TRMM precip for CCER trajectories
#BAND1_VAL1='-0.875'
BAND1_VAL1= 5
BAND1_VAL2= 5
# Option to calculate symmetric or antisymmetric component in BAND1
BAND1_SYM=False # False, 'sym', or 'antisym'

# Optional band2 
BAND2=False
# Set True to use band2
BAND2_NAME='longitude' # Dimension to average over: 'latitude' or 'longitude'
BAND2_VAL1=100.375
BAND2_VAL2=100.375

if SUBDIR=='std':
    FILEPRE='' # e.g., '', '_rac', '_rac_b20_200_n241', '_rac_rm5_n5'
    YEAR=range(1998,2022+1)
    #MONTH=[-999] # Dummy value if outfile_frequency is 'year'
    MONTH=range(1,12+1) # If outfile_frequency is less than 'year' 
elif SUBDIR=='processed':
    FILEPRE='_rac_b20_200_n241'+'_'+TDOMAINID+'_lag' # e.g., TDOMAINID of time mean data. # for lagged data
    #FILEPRE='_' + TDOMAINID # for mean fields when tdomain set to 2003-to-2020 above
else:
    raise UserWarning('SUBDIR is invalid.')

CREATE=True

PLOT=False

VERBOSE=2

#------------------------------------------------------------------

descriptor={}
descriptor['verbose']=VERBOSE
descriptor['basedir']=BASEDIR
descriptor['archive']=ARCHIVE
descriptor['basedir_archive']=BASEDIR_ARCHIVE
descriptor['subdir']=SUBDIR
descriptor['var_name']=VAR_NAME
descriptor['level']=LEVEL
descriptor['source']=SOURCE
descriptor['filepre']=FILEPRE
descriptor['band1_name']=BAND1_NAME
descriptor['band1_val1']=BAND1_VAL1
descriptor['band1_val2']=BAND1_VAL2
descriptor['band1_sym']=BAND1_SYM
descriptor['band2']=BAND2
if BAND2:
    descriptor['band2_name']=BAND2_NAME
    descriptor['band2_val1']=BAND2_VAL1
    descriptor['band2_val2']=BAND2_VAL2
    

if CREATE:
    if SUBDIR=='std':
        iter_year=da.iter_generator(YEAR)
        iter_month=da.iter_generator(MONTH)
        for year in iter_year:
            for month in iter_month:
                print('### year={0!s} month={1!s}'.format(year,month))
                descriptor['year']=year
                descriptor['month']=month
                aa=da.SpatialSubset(**descriptor)
                aa.f_spatial_subset()
    elif SUBDIR=='processed':
        aa=da.SpatialSubset(**descriptor)
        aa.f_spatial_subset()
else:
    aa.f_read_spatial_subset()
    aa.data_subset_current=aa.data_subset[-1]

if PLOT:
    x1=aa.data_subset_current
    ndim=x1.data.ndim
    if ndim==2:
        qplt.contourf(x1)
    elif ndim==1:
        qplt.plot(x1)
    
    plt.show()

print('Successfully completed.')
