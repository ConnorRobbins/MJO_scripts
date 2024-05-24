import os


BASEDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data')

BASEDIR_ARCHIVE=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')


SOURCE='glorys12v1aeq1erai_zlev_d'; 


#VARS=['swsal','swtheta','ucur','vcur']
VARS=['tsc','sa','swpd']


#LEVELS=[0.494]
LEVELS=[ 1.541, 2.645, 3.819, 5.078, 6.440, 7.929, 9.572, 11.405, 13.467, 15.810, 18.495, 21.598, 25.211, 29.444, 34.434, 40.344, 47.373, 55.764, 65.807, 77.853, 92.326, 109.729, 130.666, 155.850, 186.125, 222.475, 266.040, 318.127, 380.213, 453.937, 541.088, 643.566, 763.333, 902.339, 1062.440, 1245.291, 1452.251, 1684.284, 1941.893]


YEAR_BEG=2003; YEAR_END=2020
MONTH_BEG=1; MONTH_END=12





file_list=[]


for VAR in VARS:
    for LEVEL in LEVELS:
        LEVEL=str(LEVEL)
        for YEAR in range(YEAR_BEG, YEAR_END + 1, 1):
            YEAR=str(YEAR)
            for MONTH in range(MONTH_BEG, MONTH_END + 1, 1):
                file1=VAR + '_' + LEVEL + '_' + YEAR + str(MONTH).zfill(2) + '.nc'
                file_list.append(file1)
        
                


for file in file_list:
        command1="cp -v " + os.path.join(BASEDIR,SOURCE,'std',file) + " " + os.path.join(BASEDIR_ARCHIVE,SOURCE,'std',file)
        #print(command1)
        os.system(command1)