### Archive the output files VAR_LEVEL_rac_YYYYMM and VAR_LEVEL_rac_b20_200_n241_YYYYMM from BASEDIR TO BASDEDIR_ARCHIVE
#
# VAR_LEVEL_rac_YYYYMM is from 200301 to 202012
#
# VAR_LEVEL_rac_b20_200_n241_YYYYMM is from 200305 to 202008
#


import os


BASEDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data')

BASEDIR_ARCHIVE=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')


SOURCE='glorys12v1aeq1erai_zlev_d'; 
SUBDIR='std'


#VARS=['swsal','swtheta','ucur','vcur']
VARS=['swpd']

LEVELS=[0.494, 1.541, 2.645, 3.819, 5.078, 6.440, 7.929, 9.572, 11.405, 13.467, 15.810, 18.495, 21.598, 25.211, 29.444, 34.434, 40.344, 47.373, 55.764, 65.807, 77.853, 92.326, 109.729, 130.666, 155.850, 186.125, 222.475, 266.040, 318.127, 380.213, 453.937, 541.088, 643.566, 763.333, 902.339, 1062.440, 1245.291, 1452.251, 1684.284, 1941.893]



file_list=[]


for VAR in VARS:
    for LEVEL in LEVELS:
        for YEAR in range(2003,2020+1):
            for MONTH in range(1,12+1):
                LEVEL=str(LEVEL)
                if (not (YEAR==2003)) or MONTH>=5:
                    if (not (YEAR==2020)) or MONTH <=8:
                        file1=VAR + '_' + LEVEL + '_rac_b20_200_n241_'+ str(YEAR) + str(MONTH).zfill(2) + '.nc'
                        file_list.append(file1)

  
#print(file_list)


for file in file_list:
        command1="cp -v " + os.path.join(BASEDIR,SOURCE,SUBDIR,file) + " " + os.path.join(BASEDIR_ARCHIVE,SOURCE,SUBDIR,file)
        #print(command1)
        os.system(command1)
        
