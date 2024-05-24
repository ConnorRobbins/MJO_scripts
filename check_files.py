"""Check that files exist and have minimum file size."""

import os

BASEDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data')
#BASEDIR=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')



#CHECK='spatial_subset'
#CHECK='wheelerkiladis'
#CHECK='combine_latitudes'

#CHECK='time_average'
#
#CHECK='nemo_get'; SUBDIR='raw/tmp'; SOURCE='glorys12v1aeq1_zlev_d'
#CHECK='preprocess'; SUBDIR='std'; SOURCE='glorys12v1aeq1_zlev_d'
#CHECK='regrid'; SUBDIR='std'; SOURCE='glorys12v1aeq1erai_zlev_d'
#CHECK='lagged_mean'; SUBDIR='processed'; SOURCE='glorys12v1aeq1erai_zlev_d'


#CHECK='regrid'; SUBDIR='std'; SOURCE='era5gloerai_sfc_d'
CHECK='lagged_mean'; SUBDIR='processed'; SOURCE='era5gloerai_sfc_d'







#VAR_NAMES=['swsal','swtheta','ucur','vcur']
#VAR_NAMES=['vcur']
#VAR_NAMES=['swtheta','swsal']

#VAR_NAMES=['tsc','sa']
#VAR_NAMES=['swpd']

VAR_NAMES=['uwnd']
#VAR_NAMES=['taux']


LEVELS=[1]

#LEVELS=[0.494, 1.541, 2.645, 3.819]
#LEVELS=[5.078, 6.440, 7.929, 9.572]
#LEVELS=[11.405, 13.467, 15.810, 18.495]
#LEVELS=[21.598, 25.211, 29.444, 34.434]
#LEVELS=[40.344, 47.373, 55.764, 65.807]
#LEVELS=[77.853, 92.326, 109.729, 130.666]
#LEVELS=[155.850, 186.125, 222.475, 266.040]
#LEVELS=[318.127, 380.213, 453.937, 541.088, 643.566, 763.333, 902.339, 1062.440, 1245.291, 1452.251, 1684.284, 1941.893]

#LEVELS=[266.040, 318.127, 453.937, 541.088, 643.566, 763.333]
#LEVELS=[266.040, 318.127]
#LEVELS=[453.937, 541.088, 643.566, 763.333]
#LEVELS=[902.339, 1062.440, 1245.291, 1452.251, 1684.284, 1941.893]

#LEVELS=[0.494, 1.541, 2.645, 3.819, 5.078, 6.440, 7.929, 9.572, 11.405, 13.467, 15.810, 18.495, 21.598, 25.211, 29.444, 34.434, 40.344, 47.373, 55.764, 65.807, 77.853, 92.326, 109.729, 130.666, 155.850, 186.125, 222.475, 266.040, 318.127, 380.213, 453.937, 541.088, 643.566, 763.333, 902.339, 1062.440, 1245.291, 1452.251, 1684.284, 1941.893]

# LEVEL values in NEMO reanalysis data. Make sure to use 3 decimal places exactly
#    0.494, 1.541, 2.645, 3.819, 5.078, 6.440, 7.929, 
#    9.572, 11.405, 13.467, 15.810, 18.495, 21.598, 25.211, 
#    29.444, 34.434, 40.344, 47.373, 55.764, 65.807, 77.853, 
#    92.326, 109.729, 130.666, 155.850, 186.125, 222.475, 266.040, 
#    318.127, 380.213, 453.937, 541.088, 643.566, 763.333, 902.339, 
#    1062.440, 1245.291, 1452.251, 1684.284, 1941.893, 2225.078, 2533.336, 
#    2865.703, 3220.820, 3597.032, 3992.484, 4405.224, 4833.291, 5274.784, 
#    5727.917 ;



YEARS=range(2003,2020+1)
#YEARS=[2003]

MONTHS=range(1,12+1)
#MONTHS=[1]

LAG_SEASONS=['all']
#LAG_SEASONS=['jja']
#LAG_SEASONS=['djf','jja','all']

LAG_PHASES=range(1,8+1)

#LONGITUDES=[xx for xx in range(-170,180,10)]
#LONGITUDES=[40]

#LATITUDES=['-00.3508']
#LATITUDES=['-89.4629', '-88.7669', '-88.0669', '-87.3660', '-86.6648', '-85.9633', '-85.2618', '-84.5602', '-83.8586', '-83.1569', '-82.4553', '-81.7536', '-81.0519', '-80.3502', '-79.6485', '-78.9468', '-78.2450', '-77.5433', '-76.8416', '-76.1399', '-75.4381', '-74.7364', '-74.0346', '-73.3329', '-72.6312', '-71.9294', '-71.2277', '-70.5260', '-69.8242', '-69.1225', '-68.4207', '-67.7190', '-67.0172', '-66.3155', '-65.6137', '-64.9120', '-64.2102', '-63.5085', '-62.8067', '-62.1050', '-61.4033', '-60.7015', '-59.9998', '-59.2980', '-58.5963', '-57.8945', '-57.1928', '-56.4910', '-55.7893', '-55.0875', '-54.3858', '-53.6840', '-52.9823', '-52.2805', '-51.5788', '-50.8770', '-50.1753', '-49.4735', '-48.7718', '-48.0700', '-47.3683', '-46.6665', '-45.9647', '-45.2630', '-44.5612', '-43.8595', '-43.1577', '-42.4560', '-41.7542', '-41.0525', '-40.3507', '-39.6490', '-38.9472', '-38.2455', '-37.5437', '-36.8420', '-36.1402', '-35.4385', '-34.7367', '-34.0350', '-33.3332', '-32.6315', '-31.9297', '-31.2280', '-30.5262', '-29.8244', '-29.1227', '-28.4209', '-27.7192', '-27.0174', '-26.3157', '-25.6139', '-24.9122', '-24.2104', '-23.5087', '-22.8069', '-22.1052', '-21.4034', '-20.7017', '-19.9999', '-19.2982', '-18.5964', '-17.8947', '-17.1929', '-16.4911', '-15.7894', '-15.0876', '-14.3859', '-13.6841', '-12.9824', '-12.2806', '-11.5789', '-10.8771', '-10.1754', '-09.4736', '-08.7719', '-08.0701', '-07.3684', '-06.6666', '-05.9649', '-05.2631', '-04.5613', '-03.8596', '-03.1578', '-02.4561', '-01.7543', '-01.0526', '-00.3508', '00.3508', '01.0526', '01.7543', '02.4561', '03.1578', '03.8596', '04.5613', '05.2631', '05.9649', '06.6666', '07.3684', '08.0701', '08.7719', '09.4736', '10.1754', '10.8771', '11.5789', '12.2806', '12.9824', '13.6841', '14.3859', '15.0876', '15.7894', '16.4911', '17.1929', '17.8947', '18.5964', '19.2982', '19.9999', '20.7017', '21.4034', '22.1052', '22.8069', '23.5087', '24.2104', '24.9122', '25.6139', '26.3157', '27.0174', '27.7192', '28.4209', '29.1227', '29.8244', '30.5262', '31.2280', '31.9297', '32.6315', '33.3332', '34.0350', '34.7367', '35.4385', '36.1402', '36.8420', '37.5437', '38.2455', '38.9472', '39.6490', '40.3507', '41.0525', '41.7542', '42.4560', '43.1577', '43.8595', '44.5612', '45.2630', '45.9647', '46.6665', '47.3683', '48.0700', '48.7718', '49.4735', '50.1753', '50.8770', '51.5788', '52.2805', '52.9823', '53.6840', '54.3858', '55.0875', '55.7893', '56.4910', '57.1928', '57.8945', '58.5963', '59.2980', '59.9998', '60.7015', '61.4033', '62.1050', '62.8067', '63.5085', '64.2102', '64.9120', '65.6137', '66.3155', '67.0172', '67.7190', '68.4207', '69.1225', '69.8242', '70.5260', '71.2277', '71.9294', '72.6312', '73.3329', '74.0346', '74.7364', '75.4381', '76.1399', '76.8416', '77.5433', '78.2450', '78.9468', '79.6485', '80.3502', '81.0519', '81.7536', '82.4553', '83.1569', '83.8586', '84.5602', '85.2618', '85.9633', '86.6648', '87.3660', '88.0669', '88.7669', '89.4629']


LOOPVAR1=LOOPVAR2=LOOPVAR3=LOOPVAR4=LOOPVAR5=['X']

#------------------------------------------------------------------

if CHECK=='spatial_subset':
    LOOPVAR1=VAR_NAMES
    LOOPVAR2=LEVELS
    LOOPVAR3=LATITUDES
    LOOPVAR4=YEARS
    LOOPVAR5=MONTHS
    #FILELENGTH_MIN=3005000; FILELENGTH_MAX=3030000
    FILELENGTH_MIN=481000; FILELENGTH_MAX=534000
elif CHECK=='wheelerkiladis':
    LOOPVAR1=VAR_NAMES
    LOOPVAR2=LEVELS
    LOOPVAR3=LATITUDES
    #FILELENGTH_MIN=125000000; FILELENGTH_MAX=128000000
    FILELENGTH_MIN=295000000; FILELENGTH_MAX=305000000
elif CHECK=='lagged_mean':
    LOOPVAR1=VAR_NAMES
    LOOPVAR2=LEVELS
    LOOPVAR3=LAG_SEASONS
    LOOPVAR4=LAG_PHASES
    #FILELENGTH_MIN=17000000; FILELENGTH_MAX=18000000
    FILELENGTH_MIN=3000000; FILELENGTH_MAX=4000000
elif CHECK=='nemo_get':
    LOOPVAR1=VAR_NAMES
    LOOPVAR2=LEVELS
    LOOPVAR3=YEARS
    LOOPVAR4=MONTHS
    FILELENGTH_MIN=80000000; FILELENGTH_MAX=100000000
elif CHECK=='preprocess':
    LOOPVAR1=VAR_NAMES
    LOOPVAR2=LEVELS
    LOOPVAR3=YEARS
    LOOPVAR4=MONTHS
    FILELENGTH_MIN=170000000; FILELENGTH_MAX=200000000
elif CHECK=='regrid':
    LOOPVAR1=VAR_NAMES
    LOOPVAR2=LEVELS
    LOOPVAR3=YEARS
    LOOPVAR4=MONTHS
    FILELENGTH_MIN=2400000; FILELENGTH_MAX=3000000
elif CHECK in ['time_average','combine_latitudes']:
    LOOPVAR1=VAR_NAMES
    LOOPVAR2=LEVELS
    LOOPVAR3=YEARS
    LOOPVAR4=MONTHS
    FILELENGTH_MIN=115000000; FILELENGTH_MAX=131000000
else:
    raise UserWarning('CHECK not recognised.')

nfiles=0
nfiles_theoretical=0
files_missing=[]
files_bad=[]
var3_missing=[]
for s1 in LOOPVAR1:
    for s2 in LOOPVAR2:
        for s3 in LOOPVAR3:
            for s4 in LOOPVAR4:
                for s5 in LOOPVAR5:
                    print(s1,s2,s3,s4,s5)
                    if CHECK=='spatial_subset':
                        filec=os.path.join(BASEDIR,SOURCE,SUBDIR,s1+'_'+str(s2)+'_ss_lat_'+s3+'_'+s3+'_'+str(s4)+str(s5).zfill(2)+'.nc')
                    elif CHECK=='wheelerkiladis':
                        filec=os.path.join(BASEDIR,SOURCE,SUBDIR,s1+'_'+str(s2)+'_hovWKfiltER_lat_'+s3+'_'+s3+'_1998-01-01_2022-12-30.nc')
                    elif CHECK=='lagged_mean':
                        filec=os.path.join(BASEDIR,SOURCE,SUBDIR,s1+'_'+str(s2)+'_rac_b20_200_n241_rmm008FS-'+s3+str(s4)+'_lag.nc')
                    elif CHECK in ['nemo_get','preprocess','regrid','time_average','combine_latitudes']:
                        filec=os.path.join(BASEDIR,SOURCE,SUBDIR,str(s1)+'_'+str(s2)+'_'+str(s3)+str(s4).zfill(2)+'.nc')
                    else:
                        raise UserWarning('CHECK not recognised.')
                    nfiles_theoretical+=1
                    if os.path.isfile(filec):
                        nfiles+=1
                        filec_length=os.path.getsize(filec)
                        #print('{0!s}, {1!s}'.format(filec,filec_length))
                        if not(FILELENGTH_MIN<=filec_length<=FILELENGTH_MAX):
                            print('{0!s}: filec_length = {1!s}, but should be between {2!s} and {3!s}.'.format(filec,filec_length,FILELENGTH_MIN,FILELENGTH_MAX))
                            files_bad.append(filec)
                            if s3 not in var3_missing:
                                var3_missing.append(s3)
                    else:
                        print('File does not exist.')
                        files_missing.append(filec)
                        if s3 not in var3_missing:
                            var3_missing.append(s3)
print('nfiles, nfiles_theoretical: {0!s}, {1!s}'.format(nfiles,nfiles_theoretical))
#
print('files_missing')
f11=os.path.join(os.path.sep, 'gpfs','home','rgq13jzu','tmp','temp_miss.txt')
print('f11: {0!s}'.format(f11))
fout=open(f11,'w')
for filec in files_missing:
    print('{0!s}'.format(filec))
    fout.write(filec+'\n')
fout.close()
#
print('files_bad')
f11=os.path.join(os.path.sep, 'gpfs','home','rgq13jzu','tmp','temp_bad.txt')
print('f11: {0!s}'.format(f11))
fout=open(f11,'w')
for filec in files_bad:
    filec_length=os.path.getsize(filec)
    print('{0!s}, {1!s}'.format(filec,filec_length))
    fout.write(filec+', '+str(filec_length)+'\n')
fout.close

# Write missing var3 values to file so can use in run_scripts_sub.py again
var3_missing.sort()
print('var3_missing: {0!s}'.format(var3_missing))
ss='LOOPVAR3='+str(var3_missing)+'\n'
print(ss)
f11=os.path.join(os.path.sep, 'gpfs','home','rgq13jzu','tmp','temp33.txt')
print('f11: {0!s}'.format(f11))
fout=open(f11,'w')
fout.write(ss)
fout.close()

