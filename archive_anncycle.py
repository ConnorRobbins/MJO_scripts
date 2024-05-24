import os


BASEDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data')

BASEDIR_ARCHIVE=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data')


SOURCE='glorys12v1aeq1erai_zlev_d'; YEAR1=2003; YEAR2=2020


#VARS=['swsal','swtheta','ucur','vcur']
VARS=['swpd']


#LEVELS=[0.494]
LEVELS=[1.541, 2.645, 3.819, 5.078, 6.440, 7.929, 9.572, 11.405, 13.467, 15.810, 18.495, 21.598, 25.211, 29.444, 34.434, 40.344, 47.373, 55.764, 65.807, 77.853, 92.326, 109.729, 130.666, 155.850, 186.125, 222.475, 266.040, 318.127, 380.213, 453.937, 541.088, 643.566, 763.333, 902.339, 1062.440, 1245.291, 1452.251, 1684.284, 1941.893]

processed_file_list=[]
std_file_list=[]

for VAR in VARS:
    for LEVEL in LEVELS:
        LEVEL=str(LEVEL)
        file1=VAR + '_' + LEVEL + '_ac_smooth_'+ str(YEAR1) + '_'+ str(YEAR2) + '.nc'
        file2=VAR + '_' + LEVEL + '_ac_raw_'+ str(YEAR1) + '_'+ str(YEAR2) + '.nc'
        file3=VAR + '_' + LEVEL + '_ac_cc_'+ str(YEAR1) + '_'+ str(YEAR2) + '.nc'
        file4=VAR + '_' + LEVEL + '_ac_mm_'+ str(YEAR1) + '_'+ str(YEAR2) + '.nc'
        file5=VAR + '_' + LEVEL.split('.')[0] + '_leap.'+ LEVEL.split('.')[1] + '_ac_smooth_'+ str(YEAR1) + '_'+ str(YEAR2) + '_leap.nc'
        
        processed_file_list.append(file1)
        processed_file_list.append(file2)
        processed_file_list.append(file3)
        processed_file_list.append(file4)
        processed_file_list.append(file5)
        
        for YEAR in range(YEAR1,YEAR2+1):
            for MONTH in range(1, 12+1):
                file6=VAR + '_' + LEVEL + '_rac_' + str(YEAR) + str(MONTH).zfill(2)+'.nc'
                std_file_list.append(file6)
        
        
        


for file in processed_file_list:
        command1="cp -v " + os.path.join(BASEDIR,SOURCE,'processed',file) + " " + os.path.join(BASEDIR_ARCHIVE,SOURCE,'processed',file)
        #print(command1)
        os.system(command1)
        


for file in std_file_list:
        command1="cp -v " + os.path.join(BASEDIR,SOURCE,'std',file) + " " + os.path.join(BASEDIR_ARCHIVE,SOURCE,'std',file)
        #print(command1)
        os.system(command1)