"""Calculate absolute salinity from practical salinity using gsw."""

import os

import iris
import iris.quickplot as qplt
import matplotlib.pyplot as plt

import data_analysis as da

BASEDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data')
#BASEDIR=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')

ARCHIVE=False
BASEDIR_ARCHIVE=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')

#LEVEL=55.764; SOURCE='glorys12v1aeq1erai_zlev_d'
SOURCE='glorys12v1aeq1erai_zlev_d'

#YEAR=2003
YEAR=range(2003,2020+1)

#MONTH=-999 # if outfile_frequency is 'year'
MONTH=range(1,12+1) # If outfile_frequency is less than 'year' 
#MONTH=1

PLOT=False

VERBOSE=2
#------------------------------------------------------------------

descriptor={}
descriptor['verbose']=VERBOSE
descriptor['basedir']=BASEDIR
descriptor['source']=SOURCE
descriptor['level']=LEVEL
descriptor['archive']=ARCHIVE

# Create instance of CubeDiagnostics object
aa=da.CubeDiagnostics(**descriptor)

# Lazy read data: swsal
aa.f_read_data('swsal',LEVEL)

iter_year=da.iter_generator(YEAR)
iter_month=da.iter_generator(MONTH)
for year in iter_year:
    for month in iter_month:
        print('### year={0!s} month={1!s}'.format(year,month))
        aa.year=year
        aa.month=month
        aa.f_SA_from_SP()

# if PLOT:
    # time1=aa.sa.coord('time').points[-1]
    # time_constraint=iris.Constraint(time=time1)
    # x1=aa.sa.extract(time_constraint)

    # fig=plt.figure()
    # qplt.contourf(x1)
    # plt.gca().coastlines()
    # #plt.show()
    # fig.savefig('/gpfs/home/rgq13jzu/tmp/fig2.png')
