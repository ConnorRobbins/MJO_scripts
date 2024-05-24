"""Get NEMO reanalysis data that previously failed, saved in "temp_miss.txt" . 

Run this script from ada.  Can run interactively, but best to run as batch job.

"""

import os

import cftime
import datetime
import pdb
import copernicusmarine

BASEDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data')
#BASEDIR=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')


MISSDIR=os.path.join(os.path.sep,'gpfs','home','rgq13jzu','tmp')
#MISSDIR=os.path.join(os.path.sep,'home','stusci1','rgq13jzu','Documents','MJO_WORK','MJO_scripts')




SOURCE='glorys12v1aeq1_zlev_d'

DOWNLOAD=True





    
    
   
#### Build lists of variables for the files to download

VAR_NAMES=[]
LEVELS=[]
YEARS=[]
MONTHS=[]


missing_files=open(MISSDIR + "/temp_miss.txt" , "r")


for line in missing_files:
    string_list=line.split('/')
    string_list=string_list[-1].split('_')
    VAR_NAMES.append(string_list[0])
    LEVELS.append(float(string_list[1]))
    YEARS.append(int(string_list[2][:4]))
    MONTHS.append(int(string_list[2][4:6]))
    





delta_level=0.001 # for selecting depth level

##### Loop over lists and download
for (VAR_NAME,LEVEL,year,month) in zip(VAR_NAMES,LEVELS,YEARS,MONTHS):
    # Set variable name and depth
    depth_min=LEVEL-delta_level
    depth_max=LEVEL+delta_level
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
    
    #
    if DOWNLOAD:
        attempt_counter=0
        while attempt_counter < 3: #reattempt download  up to 3 times
            try:
                # Attempt to retrieve data from CMEMS
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
                break # If download was successful then don't reattempt the download!
            except Exception:
                if attempt_counter == 2:
                    print("Download has failed three times, now skipping and moving onto next file.")
                    break
                else:
                    # If download fails increment counter and wait 20-40 seconds before trying again
                    attempt_counter += 1
                    sleeptime=np.random.randint(20, 40 + 1)
                    print(f"Download attempt failed {attempt_counter}/3 times(s), sleeping for {sleeptime} seconds before reattempting.")
                    time.sleep(sleeptime)
