"""Preprocess data using data_analysis.DataConverter."""

import datetime
import os
import pdb

import iris
import iris.quickplot as qplt
import matplotlib.pyplot as plt

import data_analysis as da

#BASEDIR=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data') # UEA
BASEDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data') # UEA

ARCHIVE=False
BASEDIR_ARCHIVE=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')

FILE_MASK=False # Default value



#VAR_NAME='vcur'; LEVEL=1684.284; SOURCE='glorys12v1aeq1_zlev_d'
#LEVEL=1062.440; SOURCE='glorys12v1aeq1_zlev_d'
SOURCE='glorys12v1aeq1_zlev_d'


#YEAR=2003
#YEAR=range(2007,2020+1)
YEAR=range(2003,2020+1)

#MONTH=1
#MONTH=-999 # if outfile_frequency is 'year'
MONTH=range(1,12+1) # If outfile_frequency is less than 'year' 


PLOT=False

VERBOSE=2

#------------------------------------------------------------------

descriptor={}
descriptor['verbose']=VERBOSE
descriptor['basedir']=BASEDIR
descriptor['archive']=ARCHIVE
descriptor['basedir_archive']=BASEDIR_ARCHIVE
descriptor['var_name']=VAR_NAME
descriptor['level']=LEVEL
descriptor['source']=SOURCE
descriptor['file_mask']=FILE_MASK

aa=da.DataConverter(**descriptor)

iter_year=da.iter_generator(YEAR)
iter_month=da.iter_generator(MONTH)
for year in iter_year:
    for month in iter_month:
        print('### year={0!s} month={1!s}'.format(year,month))
        aa.year=year
        aa.month=month
        aa.read_cube()
        aa.format_cube()
        aa.write_cube()

if PLOT:
    tcoord=aa.cube.coord('time')
    time1=tcoord.units.num2date(tcoord.points[0])
    time_constraint=iris.Constraint(time=time1)
    x1=aa.cube.extract(time_constraint)

    #x1=aa.cube
    qplt.contourf(x1)
    plt.gca().coastlines()
    
    plt.show()
