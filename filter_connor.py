"""Time filter data using data_analysis.TimeFilter."""

import datetime
import os

import iris
import iris.quickplot as qplt
import matplotlib.pyplot as plt

import data_analysis as da


BASEDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data')
#BASEDIR=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')

BASEDIR_ARCHIVE=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')

#ARCHIVE=True
ARCHIVE=False  # If batch submitting: archive manually afterwards so you don't set fire to ADA :'(





#VAR_NAME='swtheta'; LEVEL=21.598; SOURCE='glorys12v1aeq1erai_zlev_d';
#LEVEL=40.344; SOURCE='glorys12v1aeq1erai_zlev_d';
#SOURCE='glorys12v1aeq1erai_zlev_d';

LEVEL=1; SOURCE='era5gloerai_sfc_d';


FILTER='b20_200_n241' # 'rm5_n5' 'h20_n241' 'b20_200_n241' etc.

FILEPRE='_rac' # e.g., '', '_rac',
SUBTRACT=False


####
####
##### YEAR=range(2004,2019+1)
##### MONTH=-999 # Dummy value if outfile_frequency is 'year'
##### MONTH=range(1,12+1) # If outfile_frequency is less than 'year' 
#### 
####   FILTER_CONNOR.PY HAS YEAR AND MONTH HARD CODED BELOW TO BE FROM MAY 2003 TO AUG 2020
#### 
####    IF THIS IS UNEXPECTED, USE FILTER.PY INSTEAD!
####
#######################################################################################

SPLITBLOCK=False


VERBOSE=2


PLOT=False

#==========================================================================
# # Moved out the way

#
#==========================================================================

descriptor={}
descriptor['verbose']=VERBOSE
descriptor['file_weights']=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data','weights','w_'+FILTER+'.txt')
descriptor['var_name']=VAR_NAME
descriptor['level']=LEVEL
descriptor['source']=SOURCE
descriptor['basedir']=BASEDIR
descriptor['archive']=ARCHIVE
descriptor['basedir_archive']=BASEDIR_ARCHIVE
descriptor['filepre']=FILEPRE
descriptor['filter']=FILTER
descriptor['splitblock']=SPLITBLOCK

# Create instance of TimeFilter object
aa=da.TimeFilter(**descriptor)

# Overwrite irrelevant MONTH1,MONTH2 if outfile_frequency is 'year'
if aa.outfile_frequency=='year':
    MONTH=-999






## DO 2003
YEAR=range(2003,2003+1); MONTH=range(5,12+1)
#
iter_year=da.iter_generator(YEAR)
iter_month=da.iter_generator(MONTH)
for year in iter_year:
    for month in iter_month:
        print('### year={0!s} month={1!s}'.format(year,month))
        aa.year=year
        aa.month=month
        aa.time_filter(subtract=SUBTRACT)




## DO 2004-2019
YEAR=range(2004,2019+1); MONTH=range(1,12+1)
#
iter_year=da.iter_generator(YEAR)
iter_month=da.iter_generator(MONTH)
for year in iter_year:
    for month in iter_month:
        print('### year={0!s} month={1!s}'.format(year,month))
        aa.year=year
        aa.month=month
        aa.time_filter(subtract=SUBTRACT)




## DO 2020
YEAR=range(2020,2020+1); MONTH=range(1,8+1)
#
iter_year=da.iter_generator(YEAR)
iter_month=da.iter_generator(MONTH)
for year in iter_year:
    for month in iter_month:
        print('### year={0!s} month={1!s}'.format(year,month))
        aa.year=year
        aa.month=month
        aa.time_filter(subtract=SUBTRACT)






if PLOT:
    print('# Plot')
    time_constraint=iris.Constraint(time = lambda cell: aa.timeout1 <= cell <= aa.timeout2)
    tol=0.1
    lon0=0.0
    lon_constraint=iris.Constraint(longitude = lambda cell: lon0-tol <= cell <= lon0+tol)
    lat0=55.0
    lat_constraint=iris.Constraint(latitude = lambda cell: lat0-tol <= cell <= lat0+tol)
    x1=aa.data_in.extract(time_constraint & lon_constraint & lat_constraint)
    x1=x1.concatenate_cube()
    x2=aa.data_out.extract(lon_constraint & lat_constraint)
    qplt.plot(x1,label='in')
    qplt.plot(x2,label='out')
    plt.legend()
    plt.axis('tight')
    qplt.show()
    
