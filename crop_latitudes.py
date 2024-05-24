import os
import iris
import pdb


BASEDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data')


#SOURCE='glorys12v1aeq1erai_zlev_d'; 
SOURCE='era5gloerai_sfc_d'; 

SUBDIR='std'


#VARS=['swsal','swtheta','ucur','vcur']
#VARS=['swpd']
VARS=['uwnd']


LEVELS=[1]
#LEVELS=[1.541, 2.645, 3.819, 5.078, 6.440, 7.929, 9.572, 11.405, 13.467, 15.810, 18.495, 21.598, 25.211, 29.444, 34.434, 40.344, 47.373, 55.764, 65.807, 77.853, 92.326, 109.729, 130.666, 155.850, 186.125, 222.475, 266.040, 318.127, 380.213, 453.937, 541.088, 643.566, 763.333, 902.339, 1062.440, 1245.291, 1452.251, 1684.284, 1941.893]


YEAR_BEG=2003; YEAR_END=2020

MONTH_BEG=1; MONTH_END=12

LAT_BEG=-15; LAT_END=15







################

def fun_Quick_Cube_Load(filepath):
    """
    Loads cube from file into cubelist, concatenates then returns cube.
    """
    print('Loading cube from: {0!s}'.format(filepath))
    cubelist=iris.load(filepath)   # Loads in a Cubelist of cubes
    cubelist.realise_data() # force iris to realise data rather than lazy loading
    loaded_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist
    return loaded_cube





##################



data_dir=os.path.join(BASEDIR,SOURCE,SUBDIR)

latitude_constraint_1 =  iris.Constraint(latitude = lambda cell: cell > LAT_BEG)
latitude_constraint_2 =  iris.Constraint(latitude = lambda cell: cell < LAT_END)


for VAR in VARS:
    for LEVEL in LEVELS:
        for YEAR in range(YEAR_BEG, YEAR_END+1, 1):
            for MONTH in range(MONTH_BEG, MONTH_END+1, 1):
                filename = VAR + '_' + str(LEVEL) + '_' + str(YEAR) + str(MONTH).zfill(2) +'.nc'
                filepath = os.path.join(data_dir,filename)
                cube = fun_Quick_Cube_Load(filepath)
                cube=cube.extract(latitude_constraint_1 & latitude_constraint_2)
                iris.save(cube,filepath)
                
                
                
                
               



