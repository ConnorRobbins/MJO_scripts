"""Calculate conservative temperature from absolute salinity and potential temperature using gsw."""

import os
import pdb

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

TDOMAINID='2003-to-2020'

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


# Lazy read data: absolute salinity
aa.f_read_data_processed('sa',LEVEL,TDOMAINID)
# Lazy read data: potential temperature
aa.f_read_data_processed('swtheta',LEVEL,TDOMAINID)


# Calculate conservative temperature
aa.f_CT_from_pt_no_time()


