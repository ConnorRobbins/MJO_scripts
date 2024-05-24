"""Calculate time mean statistics using data_analysis.TimeDomStats."""

import os

import cftime
import iris
import iris.quickplot as qplt
import matplotlib.pyplot as plt

import data_analysis as da

BASEDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data')
#BASEDIR=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')

#ARCHIVE=True
ARCHIVE=False  # If batch submitting: archive manually afterwards so you don't set fire to ADA :'(
BASEDIR_ARCHIVE=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')



#VAR_NAME='ucur'; LEVEL=453.937; SOURCE='glorys12v1aeq1erai_zlev_d'; TDOMAINID='ann2006'
#LEVEL=55.764; SOURCE='glorys12v1aeq1erai_zlev_d';
#SOURCE='glorys12v1aeq1erai_zlev_d';

#VAR_NAME='uwnd'; LEVEL=1; SOURCE='era5gloerai_sfc_d';
VAR_NAME='taux'; LEVEL=1; SOURCE='era5gloerai_sfc_d';

# TDOMAINID='2003-to-2020' # for calculating means over whole time period only


FILEPRE='' # e.g., '', '_rac', '_rac_minus_l30_n241'

# Usually will calculate time mean from e.g., daily data. Set DATA_FROM_ANNCYCLE to False for this.
# To calculate time mean from annual cycle (i.e., to get a mean background state for selected dates)
#   set DATA_FROM_ANNCYCLE to a 2-tuple of (year_beg,year_end) from which annual cycle was calculated
#   e.g., (1998,2018)
DATA_FROM_ANNCYCLE=False
#DATA_FROM_ANNCYCLE=(1998,2018)

# Optional parameters for use in null distribution calculation
#NMC=10; PERCENTILES_NULL=[1,2.5,5,10,20,30,50,70,80,90,95,97.5,99]; MAX_DAY_SHIFT=15
#TIME_FIRST=cftime.DatetimeGregorian(1998,1,1)
#TIME_LAST=cftime.DatetimeGregorian(2012,12,31)

LAZY_LOAD=True
VERBOSE=2

PLOT=False

#==========================================================================

descriptor={}
descriptor['verbose']=VERBOSE
descriptor['var_name']=VAR_NAME
descriptor['level']=LEVEL
descriptor['source']=SOURCE
descriptor['tdomainid']=TDOMAINID
descriptor['basedir']=BASEDIR
descriptor['archive']=ARCHIVE
descriptor['basedir_archive']=BASEDIR_ARCHIVE
descriptor['filepre']=FILEPRE
descriptor['data_from_anncycle']=DATA_FROM_ANNCYCLE
if 'NMC' in locals():
    descriptor['nmc']=NMC
if 'PERCENTILES_NULL' in locals():
    descriptor['percentiles_null']=PERCENTILES_NULL
if 'MAX_DAY_SHIFT' in locals():
    descriptor['max_day_shift']=MAX_DAY_SHIFT
if 'TIME_FIRST' in locals():
    descriptor['time_first']=TIME_FIRST
if 'TIME_LAST' in locals():
    descriptor['time_last']=TIME_LAST
if 'NODE_NUMBER' in locals():
    descriptor['node_number']=NODE_NUMBER

# Create instance of TimeDomStats object
aa=da.TimeDomStats(lazy_load=LAZY_LOAD,**descriptor)

# Calculate event means and time mean
aa.event_means()
aa.f_time_mean()

# Calculate components of null distribution (use with batch distribution)
#aa.f_time_mean_null_distribution_component()

# Calculate percentiles of null distribution
#aa.f_percentiles_null()

if PLOT:
    print('# Plot')
    fig=plt.figure()
    x1=aa.time_mean

    #per_constraint=iris.Constraint(percentile=2.5)
    #x1=aa.mean_percentiles_null.extract(per_constraint)
    lat_constraint=iris.Constraint(latitude=lambda cell: 30<=cell<=60)
    lon_constraint=iris.Constraint(longitude=lambda cell: 300<=cell<=350)
    #x1=x1.extract(lat_constraint & lon_constraint)

    qplt.contourf(x1)
    plt.gca().coastlines()
    plt.show()

    fig.savefig('/gpfs/home/rgq13jzu/tmp/fig1.png')
