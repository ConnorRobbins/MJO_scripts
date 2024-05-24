"""Combine levels into single cube using data_analysis.CombineLevels"""

import datetime
import os

import iris
import iris.quickplot as qplt
import matplotlib.pyplot as plt

import data_analysis as da
#import info

BASEDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data')
#BASEDIR=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')

ARCHIVE=False
BASEDIR_ARCHIVE=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')

SOURCE='glorys12v1aeq1erai_zlev_d'

#SUBDIR='std'        # 'std': input data with time axis
SUBDIR='processed'  # 'processed': input data with no time axis



#VAR_NAME='tsc'


#TDOMAINID='rmm008FS-djf3'
#TDOMAINID='2003-to-2020'



#LEVELS= [ 0.494, 9.572, 21.598, 29.444, 40.344, 55.764, 92.326, 155.850, 222.475, 318.127, 453.937, 541.088, 643.566, 763.333, 902.339, 1062.440, 1245.291, 1452.251] # For Patama's figures
LEVELS=[ 0.494, 1.541, 2.645, 3.819, 5.078, 6.440, 7.929, 9.572, 11.405, 13.467, 15.810, 18.495, 21.598, 25.211, 29.444, 34.434, 40.344, 47.373, 55.764, 65.807, 77.853, 92.326, 109.729, 130.666, 155.850, 186.125, 222.475, 266.040, 318.127, 380.213, 453.937, 541.088, 643.566, 763.333, 902.339, 1062.440, 1245.291, 1452.251, 1684.284, 1941.893]



if SUBDIR=='std':
    FILEPRE='' # e.g., '', '_rac', '_rac_b20_200_n241', '_rac_rm5_n5'
    YEAR_BEG=2003; YEAR_END=2003
    #MONTH1=MONTH2=-999 # Set both MONTH1 and MONTH2 to same (irrelevant) value if outfile_frequency is 'year'
    MONTH1=1; MONTH2=1 # Set month ranges if outfile_frequency is less than 'year'
elif SUBDIR=='processed':
    FILEPRE='_rac_b20_200_n241_' + TDOMAINID + '_lag' # e.g., TDOMAINID of time mean data. # This is for combining my filtered data 
    #FILEPRE='_' + TDOMAINID # This is for the mean data for looking at Nsquared
else:
    raise ValueError('SUBDIR is invalid.')

PLOT=False

VERBOSE=2

#------------------------------------------------------------------

descriptor={}
descriptor['verbose']=VERBOSE
descriptor['basedir']=BASEDIR
descriptor['archive']=ARCHIVE
descriptor['basedir_archive']=BASEDIR_ARCHIVE
descriptor['subdir']=SUBDIR
descriptor['source']=SOURCE
descriptor['var_name']=VAR_NAME
descriptor['levels']=LEVELS
descriptor['filepre']=FILEPRE


# Create instance of CombineLevels object
aa=da.CombineLevels(**descriptor)

if SUBDIR=='std':
    for year in range(YEAR_BEG,YEAR_END+1):
        for month in range(MONTH1,MONTH2+1):
            print('### year={0!s} month={1!s}'.format(year,month))
            aa.year=year
            aa.month=month
            aa.f_combine_levels()
elif SUBDIR=='processed':
    aa.f_combine_levels()

if PLOT:
    fig=plt.figure()
    x1=aa.data_all
    x2=x1.extract(iris.Constraint(latitude=0.0))
    qplt.contourf(x2,yrev=1)
    
    plt.show()
    fig.savefig('/gpfs/home/rgq13jzu/tmp/fig1.png')
