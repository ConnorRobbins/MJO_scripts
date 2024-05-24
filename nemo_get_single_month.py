"""Get NEMO reanalysis data. 

Run this script from ada.  Can run interactively, but best to run as batch job.

"""

import os

import cftime
import datetime
import pdb
import copernicusmarine

BASEDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data')
#BASEDIR=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')

SOURCE='glorys12v1aeq1_zlev_d'

VAR_NAME='vcur'

#LEVEL=1941.893
LEVEL=1684.284

# LEVEL values in NEMO reanalysis data. Make sure to use 3 decimal places exactly
#    0.494, 1.541, 2.645, 3.819, 5.078, 6.440, 7.929, 
#    9.572, 11.405, 13.467, 15.810, 18.495, 21.598, 25.211, 
#    29.444, 34.434, 40.344, 47.373, 55.764, 65.807, 77.853, 
#    92.326, 109.729, 130.666, 155.850, 186.125, 222.475, 266.040, 
#    318.127, 380.213, 453.937, 541.088, 643.566, 763.333, 902.339, 
#    1062.440, 1245.291, 1452.251, 1684.284, 1941.893, 2225.078, 2533.336, 
#    2865.703, 3220.820, 3597.032, 3992.484, 4405.224, 4833.291, 5274.784, 
#    5727.917 ;

YEAR_BEG=2003; 
MONTH1=1;

DOWNLOAD=True



#==========================================================================


YEAR_END=YEAR_BEG
MONTH2=MONTH1 

# Set variable name
if VAR_NAME=='swtheta':
    variable='thetao'
elif VAR_NAME=='swsal':
    variable='so'
elif VAR_NAME=='ucur':
    variable='uo'
elif VAR_NAME=='vcur':
    variable='vo'
else:
    raise UserWarning('VAR_NAME not recognised.')

# Set level
delta_level=0.001
depth_min=LEVEL-delta_level
depth_max=LEVEL+delta_level

# Loop over years and months
for year in range(YEAR_BEG,YEAR_END+1):
    for month in range(MONTH1,MONTH2+1):
        print('### year={0!s} month={1!s}'.format(year,month))
        date_min=cftime.DatetimeGregorian(year,month,1)
        if month<12:
            date_max=cftime.DatetimeGregorian(year,month+1,1)-datetime.timedelta(seconds=1)
        else:
            date_max=cftime.DatetimeGregorian(year+1,1,1)-datetime.timedelta(seconds=1)
        date_min=str(date_min)
        date_max=str(date_max)
        print('date_min,date_max: {0!s}, {1!s}'.format(date_min,date_max,))

        # Set download file name
        out_dir=os.path.join(BASEDIR,SOURCE,'raw','tmp')
        out_name=os.path.join(VAR_NAME+'_'+str(LEVEL)+'_'+str(year)+str(month).zfill(2)+'.nc')
        print('out_dir: {0!s}'.format(out_dir))
        print('out_name: {0!s}'.format(out_name))

        if DOWNLOAD:
            # Retrieve data from CMEMS
            copernicusmarine.subset(
              dataset_id="cmems_mod_glo_phy_my_0.083_P1D-m",
              variables=[variable],
              minimum_longitude=-180,
              maximum_longitude=179.9167,
              minimum_latitude=-15,
              maximum_latitude=15,
              start_datetime=date_min,
              end_datetime=date_max,
              minimum_depth=depth_min,
              maximum_depth=depth_max,
              output_filename = out_name,
              output_directory = out_dir,
              overwrite_output_data=True,
              force_download=True
            )


