#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 11:48:31 2023


Plots 3 plots on one figure 
a) Map to orient. 15S-15N, 30E-30E. Surface, time mean. Potential density colour shading, and (u,v) current vectors.
b) Depth-lon section of potential density
c) Depth-lon section of zonal current

@author: rgq13jzu
"""



import os

import iris
import iris.plot as iplt
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import pdb
import numpy as np

import cartopy.crs as ccrs
import matplotlib.cm as mpl_cm
import warnings

import matplotlib.colors as colors

from panels import FigureSizeLocator

import MyPaperFigureFunctions as MFF

###########
# Choose place of work

# Ada
DATADIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data','glorys12v1aeq1erai_zlev_d','processed'); 

PLOTDIR=os.path.join(os.path.sep,'gpfs','home','rgq13jzu','MJO_scripts','Plotting_Scripts','Paper_Figures','Plotting_Scripts','Figures')


###########
#
# Choose what data to plot

# Panel A and B are the same variable and share a colourbar

PANEL_A_CONTOUR_VAR_NAME='swpd'; PANEL_A_CONTOUR_LEVELS=np.array([20,21,22,23,24,25,26])

PANEL_C_MEAN_STATE_VAR_NAME='ucur'; PANEL_C_CONTOUR_LEVELS=np.array([-0.75, -0.5, -0.25, -0.01, 0.01, 0.25, 0.5, 0.75, 1 ])








TDOMAINID='2003-to-2020'

LEVEL='0.494'

FILEPRE='_all_'  

FILE_SUFFIX ='.nc' #'_lag.nc'




LONG_BEG=30; LONG_END=390
LAT_BEG=-15; LAT_END=15


LAT_VALUE=0 # for depth plots







############
# Plotting options

SAVE_HIGH_RES_BOOL=True


LONG_MAJOR_TICK_STEP=30; LONG_MINOR_TICK_STEP=10
LAT_MAJOR_TICK_STEP=15; LAT_MINOR_TICK_STEP=5  

TEX_FIGURE_WIDTH_IN_PTS=397.48499



########################
# y axis options



MAXIMUM_DEPTH=2000

DEPTH_MAJOR_TICK_STEP=25
#DEPTH_MINOR_TICK_STEP=100


SPLIT_DEPTH_SCALES_1_BOOL=True
SPLIT_DEPTH_SCALES_1_DEPTH=50
SPLIT_DEPTH_SCALES_1_YSCALING_FACTOR=2 # Factor of compression of y axis


SPLIT_DEPTH_SCALES_2_BOOL=True
SPLIT_DEPTH_SCALES_2_DEPTH=200
SPLIT_DEPTH_SCALES_2_YSCALING_FACTOR=17.5 # Factor of compression of y axis



SPLIT_DEPTH_SCALES_1_MAJOR_TICK_STEP=50
SPLIT_DEPTH_SCALES_2_MAJOR_TICK_STEP=500

# If not commented out these ticks will be used instead.
MANUAL_DEPTH_TICKS_OVERRIDE=[0, 25, 50, 100, 150, 200, 1000,2000]



#########




X_AXIS_LABEL_FONT_SIZE=10
Y_AXIS_LABEL_FONT_SIZE=10

X_AXIS_TICK_ROTATION=0
Y_AXIS_TICK_ROTATION=0

PANEL_LABEL_FONT_SIZE=9

X_TICK_FONT_SIZE=7
Y_TICK_FONT_SIZE=7

MAJOR_TICK_LENGTH=6
MAJOR_TICK_WIDTH=1.3
MINOR_TICK_LENGTH=3
MINOR_TICK_WIDTH=1.

SHARE_X_TICKS_BOOL=True # If true only the lowest row will have the xticks labelled, otherwise all labelled individually.


COLORBAR_TICK_FONT_SIZE=8
COLORBAR_TICK_LABEL_ROTATION=45

COLORBAR_TITLE_FONT_SIZE=9


COLORBAR_WIDTH_MULTIPLIER=0.9 # Factor by which colour bar is squeezed compared to panel width.


COLORBAR_HEIGHT=0.02
COLORBAR_VERTICAL_SHIFT=-0.11 # Move colour bar up and down
    
# Shift individual panels to allow for different shapes and cbars (positive : up, negative: down)
PANEL_A_VERTICAL_SHIFT=0.04 # Move panels a), b) and c) up and down relative to default position in figure
PANEL_B_VERTICAL_SHIFT=0.06 # Move panels b) and c) up and down, applied after previous shift
PANEL_C_VERTICAL_SHIFT=-0.15 # Move panel c) up and down, applied after previous two shifts



DRAW_GRIDLINES=False # Set to True to add overlay gridlines
GRIDLINE_WIDTH=0.25


#################### QUIVER PROPERTIES

# Manually tweak to deal with problematic arrows (i.e. big values on coasts)
MASK_N_BIGGEST_PLOT_ARROWS=0
#MASK_N_BIGGEST_PLOT_ARROWS=1


#### Step size for sampling data in order to draw velocity arrows
X_QUIVER_STEP=15
#X_QUIVER_STEP=80


#Y_QUIVER_STEP=4
Y_QUIVER_STEP=6

NORMALISE_TO_UNIT_ARROWS_BOOL=False   # True makes all arrows same length
#NORMALISE_TO_UNIT_ARROWS_BOOL=True   # True makes all arrows same length

ARROW_SCALE_FACTOR=3 # Multiplier to all quiver arrows

QUIVER_KEY_EXAMPLE_MAGNITUDE=1
QUIVER_KEY_EXAMPLE_X=0.85
QUIVER_KEY_EXAMPLE_Y=1.3

###########################
###########################





def get_cbar_labels(var_name):
    # Build the colour bar label string
    if var_name=='swtheta':
        return 'Potential temperature ($^\circ$C)'
    elif var_name=='swsal':
        return 'Practical salinity (g kg$^{-1}$)'
    elif var_name=='ucur':
        return 'Zonal velocity (m s$^{-1}$)'
    elif var_name=='vcur':
        return 'Meridional velocity (m s$^{-1}$)'
    elif var_name=='swpd':
        return 'Potential density (kg m$^{-3}$)'
    else:
        warnings.warn("VAR not recognised for generating label, please check what you are plotting.")
        return ''



#
###
###############################
###############################  Run some initial checks on the settings so that if it's definitely going to break you don't wait as long to find out. 




if not(type(SPLIT_DEPTH_SCALES_1_BOOL)==bool):
    raise Exception("SPLIT_DEPTH_SCALES_1_BOOL must be a Boolean")
if not(type(SPLIT_DEPTH_SCALES_2_BOOL)==bool):
    raise Exception("SPLIT_DEPTH_SCALES_2_BOOL must be a Boolean")
if SPLIT_DEPTH_SCALES_2_BOOL and not SPLIT_DEPTH_SCALES_1_BOOL:
    raise Exception("SPLIT_DEPTH_SCALES_2_BOOL must not be True if SPLIT_DEPTH_SCALES_1_BOOL is False. If trying to split on one level use SPLIT_DEPTH_SCALES_1 variables not SPLIT_DEPTH_SCALES_2.")
if SPLIT_DEPTH_SCALES_1_DEPTH > SPLIT_DEPTH_SCALES_2_DEPTH:
    raise Exception("SPLIT_DEPTH_SCALES_DEPTH_1 must be less than SPLIT_DEPTH_SCALES_DEPTH_2.")

if not(type(SHARE_X_TICKS_BOOL)==bool):
    raise Exception("SHARE_X_TICKS_BOOL must be a Boolean")


###  Check that the code will behave given the choice of longitudes

if LONG_BEG > LONG_END:
    raise Exception("Ensure LONG_BEG is less than LONG_END")
elif abs(LONG_END-LONG_BEG) > 360:
    raise Exception("Ensure the difference between LONG_BEG and LONG_END does not exceed 360 degrees")




###############################
###############################    
### 
# 









#
###
###############################
############################### Make the longitude ticks now so that if they fail you don't bother loading the data first



long_beg_major_round=LONG_BEG
long_end_major_round=LONG_END
long_beg_minor_round=LONG_BEG
long_end_minor_round=LONG_END
# Round the values for making ticks

## Longitude
long_beg_major_round=LONG_MAJOR_TICK_STEP*int(np.ceil(long_beg_major_round/LONG_MAJOR_TICK_STEP))
long_end_major_round=LONG_MAJOR_TICK_STEP*int(np.floor(long_end_major_round/LONG_MAJOR_TICK_STEP))
if long_beg_major_round == long_end_major_round:
    raise Exception("LONG_MAJOR_TICK_STEP too large for longitude range; rounded start and end values are equal")
    
long_beg_minor_round=LONG_MINOR_TICK_STEP*int(np.ceil(long_beg_minor_round/LONG_MINOR_TICK_STEP))
long_end_minor_round=LONG_MINOR_TICK_STEP*int(np.floor(long_end_minor_round/LONG_MINOR_TICK_STEP))
if long_beg_minor_round == long_end_minor_round:
    raise Exception("LONG_MINOR_TICK_STEP too large for longitude range; rounded start and end values are equal")  
    



# Make the longitude ticks
long_ticks_major=np.arange(long_beg_major_round,long_end_major_round+1,LONG_MAJOR_TICK_STEP)
long_ticks_minor=np.arange(long_beg_minor_round,long_end_minor_round+1,LONG_MINOR_TICK_STEP)


long_ticks_labels_major=MFF.Make_Tick_Labels(long_ticks_major,'longitude')


## Latitude


lat_beg_major_round=LAT_BEG
lat_end_major_round=LAT_END
lat_beg_minor_round=LAT_BEG
lat_end_minor_round=LAT_END
# Round the values for making ticks


lat_beg_major_round=LAT_MAJOR_TICK_STEP*int(np.ceil(lat_beg_major_round/LAT_MAJOR_TICK_STEP))
lat_end_major_round=LAT_MAJOR_TICK_STEP*int(np.floor(lat_end_major_round/LAT_MAJOR_TICK_STEP))
if lat_beg_major_round == lat_end_major_round:
    raise Exception("LAT_MAJOR_TICK_STEP too large for latitude range; rounded start and end values are equal")
    
lat_beg_minor_round=LAT_MINOR_TICK_STEP*int(np.ceil(lat_beg_minor_round/LAT_MINOR_TICK_STEP))
lat_end_minor_round=LAT_MINOR_TICK_STEP*int(np.floor(lat_end_minor_round/LAT_MINOR_TICK_STEP))
if lat_beg_minor_round == lat_end_minor_round:
    raise Exception("LAT_MINOR_TICK_STEP too large for latitude range; rounded start and end values are equal")  
    

# Make the latitude ticks
lat_ticks_major=np.arange(lat_beg_major_round,lat_end_major_round+1,LAT_MAJOR_TICK_STEP)
lat_ticks_minor=np.arange(lat_beg_minor_round,lat_end_minor_round+1,LAT_MINOR_TICK_STEP)
#
lat_ticks_labels_major=MFF.Make_Tick_Labels(lat_ticks_major,'latitude')


###############################
###############################    
### 
# 









#
###
###############################
###############################  Load the data and package it up ready for the plotting, find extreme values while there

PANEL_B_MEAN_STATE_VAR_NAME=PANEL_A_CONTOUR_VAR_NAME; PANEL_B_CONTOUR_LEVELS=PANEL_A_CONTOUR_LEVELS

### Load the data, making a list of the cubes and work out the extreme data values to set the contour levels 


#### Panel a) data

# Load contour var data

filename= PANEL_A_CONTOUR_VAR_NAME + '_' + LEVEL + '_' + TDOMAINID + FILE_SUFFIX
file1=os.path.join(DATADIR,filename)
print('Plotting variable data: {0!s}'.format(file1))
cubelist=iris.load(file1)   # Loads in a Cubelist of cubes
cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist

panel_a_contour_var_cube=MFF.MFF_Cube_Circular_Spatial_Subset(cube, [LAT_BEG,LAT_END], [LONG_BEG,LONG_END])

# load u and v data

u_filename='ucur' + '_' + LEVEL + '_' + TDOMAINID + FILE_SUFFIX
u_file=os.path.join(DATADIR,u_filename)
print('ucur data: {0!s}'.format(u_file))
cubelist=iris.load(u_file)   # Loads in a Cubelist of cubes
panel_a_u_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist
panel_a_u_cube=MFF.MFF_Cube_Circular_Spatial_Subset(panel_a_u_cube, [LAT_BEG,LAT_END], [LONG_BEG,LONG_END])

v_filename='vcur' + '_' + LEVEL + '_' + TDOMAINID + FILE_SUFFIX
v_file=os.path.join(DATADIR,v_filename)
print('vcur data: {0!s}'.format(v_file))
cubelist=iris.load(v_file)   # Loads in a Cubelist of cubes
panel_a_v_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist
panel_a_v_cube=MFF.MFF_Cube_Circular_Spatial_Subset(panel_a_v_cube, [LAT_BEG,LAT_END], [LONG_BEG,LONG_END])




#### Panel b) data

file_prefix=PANEL_B_MEAN_STATE_VAR_NAME+FILEPRE




panel_b_filename=file_prefix+TDOMAINID+FILE_SUFFIX
panel_b_file1=os.path.join(DATADIR,panel_b_filename)
print('file1: {0!s}'.format(panel_b_file1))
cubelist=iris.load(panel_b_file1)   # Loads in a Cubelist of cubes
panel_b_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist

# Extract data above the maximum depth
cube_depth_Constraints=iris.Constraint(level=lambda cell: cell < MAXIMUM_DEPTH) 
panel_b_cube=panel_b_cube.extract(cube_depth_Constraints)


#Extract data for correct latitude value
latIndex=panel_b_cube.coord('latitude').nearest_neighbour_index(LAT_VALUE)
latCoord=panel_b_cube.coord('latitude')[latIndex]
latValue=latCoord.cell(0)[0]
cube_lat_Constraints=iris.Constraint(latitude=latValue)
panel_b_cube=panel_b_cube.extract(cube_lat_Constraints)





#Extract data for correct longitudes and shuffle the cube around for circular plotting, jump over 180 degree data point
panel_b_cube.coord('longitude').attributes['modulo']=360
cube_west_longs=panel_b_cube.extract(iris.Constraint(longitude=lambda cell: (180 < cell) and (cell < 360)))
cube_east_longs=panel_b_cube.extract(iris.Constraint(longitude=lambda cell: (0 <= cell) and (cell < 180)))
cube_west_longs.coord('longitude').bounds=cube_west_longs.coord('longitude').bounds-360
cube_west_longs.coord('longitude').points=cube_west_longs.coord('longitude').points-360
panel_b_cube=iris.cube.CubeList([cube_west_longs,cube_east_longs]).concatenate()[0]
panel_b_cube.coord('longitude').circular=True
panel_b_cube=panel_b_cube.intersection(longitude=(LONG_BEG,LONG_END))





























#### Panel c) data

file_prefix=PANEL_C_MEAN_STATE_VAR_NAME+FILEPRE




panel_c_filename=file_prefix+TDOMAINID+FILE_SUFFIX
panel_c_file1=os.path.join(DATADIR,panel_c_filename)
print('file1: {0!s}'.format(panel_c_file1))
cubelist=iris.load(panel_c_file1)   # Loads in a Cubelist of cubes
panel_c_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist

# Extract data above the maximum depth
cube_depth_Constraints=iris.Constraint(level=lambda cell: cell < MAXIMUM_DEPTH) 
panel_c_cube=panel_c_cube.extract(cube_depth_Constraints)


#Extract data for correct latitude value
latIndex=panel_c_cube.coord('latitude').nearest_neighbour_index(LAT_VALUE)
latCoord=panel_c_cube.coord('latitude')[latIndex]
latValue=latCoord.cell(0)[0]
cube_lat_Constraints=iris.Constraint(latitude=latValue)
panel_c_cube=panel_c_cube.extract(cube_lat_Constraints)





#Extract data for correct longitudes and shuffle the cube around for circular plotting, jump over 180 degree data point
panel_c_cube.coord('longitude').attributes['modulo']=360
cube_west_longs=panel_c_cube.extract(iris.Constraint(longitude=lambda cell: (180 < cell) and (cell < 360)))
cube_east_longs=panel_c_cube.extract(iris.Constraint(longitude=lambda cell: (0 <= cell) and (cell < 180)))
cube_west_longs.coord('longitude').bounds=cube_west_longs.coord('longitude').bounds-360
cube_west_longs.coord('longitude').points=cube_west_longs.coord('longitude').points-360
panel_c_cube=iris.cube.CubeList([cube_west_longs,cube_east_longs]).concatenate()[0]
panel_c_cube.coord('longitude').circular=True
panel_c_cube=panel_c_cube.intersection(longitude=(LONG_BEG,LONG_END))












###############################
###############################    
### 
# 






#
###
###############################
###############################  Make the major depth ticks and split y axis


try:
    depth_ticks_major=MANUAL_DEPTH_TICKS_OVERRIDE
except:
    deepest_depth=cube.coord('level').cell(-1)[0]
    if SPLIT_DEPTH_SCALES_1_BOOL == False: #normal ticks if not splitting
        depth_ticks_major=np.arange(0, deepest_depth+1, DEPTH_MAJOR_TICK_STEP)
    elif SPLIT_DEPTH_SCALES_2_BOOL == False : #must be one split, make ticks in two parts and then append 
        depth_ticks_major=np.arange(0,SPLIT_DEPTH_SCALES_1_DEPTH,DEPTH_MAJOR_TICK_STEP)
        depth_ticks_major=np.append(depth_ticks_major,np.arange(SPLIT_DEPTH_SCALES_1_DEPTH,deepest_depth+1,SPLIT_DEPTH_SCALES_1_MAJOR_TICK_STEP))
    else: #must be three splits, make ticks in three parts and then append
        depth_ticks_major=np.arange(0,SPLIT_DEPTH_SCALES_1_DEPTH,DEPTH_MAJOR_TICK_STEP)
        depth_ticks_major=np.append(depth_ticks_major,np.arange(SPLIT_DEPTH_SCALES_1_DEPTH,SPLIT_DEPTH_SCALES_2_DEPTH+1,SPLIT_DEPTH_SCALES_1_MAJOR_TICK_STEP))
        depth_ticks_major=np.append(depth_ticks_major,np.arange(SPLIT_DEPTH_SCALES_2_DEPTH,deepest_depth+1,SPLIT_DEPTH_SCALES_2_MAJOR_TICK_STEP))


print("Depth major tick values:",depth_ticks_major)


depth_ticks_labels_major=MFF.Make_Tick_Labels(depth_ticks_major,"depth")





[forward_depth_fun , inverse_depth_fun]=MFF.Assign_Piecewise_Linear_Yaxis_Scaling_Functions(SPLIT_DEPTH_SCALES_1_BOOL, SPLIT_DEPTH_SCALES_1_DEPTH, SPLIT_DEPTH_SCALES_1_YSCALING_FACTOR,SPLIT_DEPTH_SCALES_2_BOOL,SPLIT_DEPTH_SCALES_2_DEPTH, SPLIT_DEPTH_SCALES_2_YSCALING_FACTOR)




## Latitude

lat_ticks_major=np.arange(LAT_BEG,LAT_END+1,LAT_MAJOR_TICK_STEP)
lat_ticks_minor=np.arange(LAT_BEG,LAT_END+1,LAT_MINOR_TICK_STEP)

#
lat_ticks_labels_major=MFF.Make_Tick_Labels(lat_ticks_major,'latitude')







###############################
###############################    
### 
# 




## Set up the figure and panel locations

panel_ratio=3.2

number_of_rows=3
number_of_columns=1




figure_width_in_mm=(TEX_FIGURE_WIDTH_IN_PTS/72.27)*25.4
left_padding=1.5*figure_width_in_mm/10
right_padding=figure_width_in_mm/20
top_padding=right_padding/5
#bottom_padding=right_padding*6
bottom_padding=right_padding*5
horizontal_sep=right_padding/1.3
vertical_sep=8







locat=FigureSizeLocator(rows=number_of_rows, columns=number_of_columns, figwidth=figure_width_in_mm, panelratio=panel_ratio, hsep=horizontal_sep, vsep=vertical_sep, padleft=left_padding, padright=right_padding, padtop=top_padding, padbottom=bottom_padding, units='mm')


fig=plt.figure(figsize=locat.figsize)



centre_longitude=((LONG_BEG+LONG_END)/2)
axes_projection=ccrs.PlateCarree(central_longitude=centre_longitude)
tick_projection=ccrs.PlateCarree(central_longitude=centre_longitude)







#
###
###############################
############################### Plotting







## First plot panel a)

pos=locat.panel_position(0,0)
shifted_pos=(pos[0], pos[1] + PANEL_A_VERTICAL_SHIFT, pos[2], pos[3])
panel=fig.add_axes(shifted_pos,projection=axes_projection)
plt.axes(panel)


panel_a_cmap=MFF.MFF_Assign_Variable_Colourmaps(PANEL_A_CONTOUR_VAR_NAME,False) # False means not diverging colours
panel_a_with_plot=iplt.contourf(panel_a_contour_var_cube, levels=PANEL_A_CONTOUR_LEVELS, coords=['longitude','latitude'], extend='both',cmap=panel_a_cmap)

# Quiver plot over the top of the contour plot


panel_a_longitudes=panel_a_u_cube.coord('longitude').points
panel_a_latitudes=panel_a_u_cube.coord('latitude').points

panel_a_longitudes=panel_a_longitudes[::X_QUIVER_STEP]-centre_longitude
panel_a_latitudes=panel_a_latitudes[::Y_QUIVER_STEP]


panel_a_plot_x, panel_a_plot_y=np.meshgrid(panel_a_longitudes,panel_a_latitudes)

panel_a_plot_u = panel_a_u_cube[::Y_QUIVER_STEP,::X_QUIVER_STEP].data
panel_a_plot_v = panel_a_v_cube[::Y_QUIVER_STEP,::X_QUIVER_STEP].data


for i in range(MASK_N_BIGGEST_PLOT_ARROWS):
    ind=np.unravel_index(np.argmax(np.sqrt(panel_a_plot_u**2 + panel_a_plot_v**2)), panel_a_plot_u.shape)
    panel_a_plot_u.mask[ind]=True
    panel_a_plot_v.mask[ind]=True


print(panel_a_plot_u.max())
print(panel_a_plot_v.max())

normalisation=np.sqrt(panel_a_plot_u**2 + panel_a_plot_v**2)

if not NORMALISE_TO_UNIT_ARROWS_BOOL: 
    normalisation=normalisation.max()

panel_a_plot_u = panel_a_plot_u/normalisation
panel_a_plot_v = panel_a_plot_v/normalisation

quiver_key_string = str(QUIVER_KEY_EXAMPLE_MAGNITUDE) + r' m s$^{-1}$'


panel_with_quiver=plt.quiver(panel_a_plot_x, panel_a_plot_y, panel_a_plot_u, panel_a_plot_v, angles='uv', pivot='middle', scale=len(panel_a_latitudes)/ARROW_SCALE_FACTOR, minlength=0.5, scale_units='height',units='height',minshaft=2)



if not NORMALISE_TO_UNIT_ARROWS_BOOL: 
    plt.quiverkey(Q=panel_with_quiver, X=QUIVER_KEY_EXAMPLE_X, Y=QUIVER_KEY_EXAMPLE_Y, U=QUIVER_KEY_EXAMPLE_MAGNITUDE/normalisation, label=quiver_key_string, labelpos='E', angle=0, coordinates='axes')


plt.gca().coastlines()
#
panel.set_xticks(long_ticks_major-centre_longitude, crs=tick_projection, minor=False) # Set major x-ticks positions
panel.set_xticks(long_ticks_minor-centre_longitude, crs=tick_projection, minor=True) # Set minor x-ticks positions
#panel.set_xticklabels(long_ticks_labels_major, minor=False) # Set major x-ticks labels
panel.set_xticklabels([], minor=False) # Set major x-ticks labels
#
panel.set_yticks(lat_ticks_major, crs=tick_projection, minor=False) # Set major y-ticks positions
panel.set_yticklabels(lat_ticks_labels_major, minor=False) # Set major y-ticks labels
panel.set_yticks(lat_ticks_minor, crs=tick_projection, minor=True) # Set minor y-ticks positions
#
panel.tick_params(which='major',axis='both',direction='out',length=MAJOR_TICK_LENGTH, width=MAJOR_TICK_WIDTH)
panel.tick_params(which='minor',axis='both',direction='out',length=MINOR_TICK_LENGTH, width=MINOR_TICK_WIDTH)
#
panel.tick_params(axis='x', rotation=X_AXIS_TICK_ROTATION, labelsize=X_TICK_FONT_SIZE)
panel.tick_params(axis='y', rotation=Y_AXIS_TICK_ROTATION, labelsize=Y_TICK_FONT_SIZE)


panel.set_title('(a)',loc='left',fontsize=PANEL_LABEL_FONT_SIZE)














############################### Second plot panel b)


pos=locat.panel_position(1,0)
shifted_pos=(pos[0], pos[1] + PANEL_A_VERTICAL_SHIFT+PANEL_B_VERTICAL_SHIFT, pos[2], pos[3])
panel=fig.add_axes(shifted_pos)
plt.axes(panel)
plt.gca().patch.set_color('.3') # Dark grey
plt.gca().patch.set_edgecolor('k')
plt.gca().patch.set_hatch('++') 
# If var is a velocity apply a diverging colourscheme centred at 0. Otherwise apply designated cmap.
if PANEL_B_MEAN_STATE_VAR_NAME in ['ucur','vcur']:
    panel_b_colours=MFF.MFF_Get_Diverging_Colours(PANEL_B_MEAN_STATE_VAR_NAME, PANEL_B_CONTOUR_LEVELS)
    panel_with_colourbar=iplt.contourf(panel_b_cube, levels=PANEL_B_CONTOUR_LEVELS, coords=['longitude','level'], extend='both',colors=panel_b_colours)
else:
    panel_b_cmap=MFF.MFF_Assign_Variable_Colourmaps(PANEL_B_MEAN_STATE_VAR_NAME,False)
    panel_with_colourbar=iplt.contourf(panel_b_cube, levels=PANEL_B_CONTOUR_LEVELS, coords=['longitude','level'], extend='both',cmap=panel_b_cmap)
#
plt.gca().set_yscale('function', functions=(forward_depth_fun,inverse_depth_fun))
if SPLIT_DEPTH_SCALES_1_BOOL==True:
    plt.hlines(SPLIT_DEPTH_SCALES_1_DEPTH,LONG_BEG,LONG_END,colors='k')
if SPLIT_DEPTH_SCALES_2_BOOL==True:
    plt.hlines(SPLIT_DEPTH_SCALES_2_DEPTH,LONG_BEG,LONG_END,colors='k')
    #    
plt.xlim(LONG_BEG,LONG_END)
#
panel.set_xticks(long_ticks_major, minor=False) # Set major x-ticks positions
panel.set_xticks(long_ticks_minor, minor=True) # Set minor x-ticks positions
panel.set_xticklabels(long_ticks_labels_major, minor=False) # Set major x-ticks labels
panel.set_yticks(depth_ticks_major,  minor=False) # Set major y-ticks positions
panel.set_yticklabels(depth_ticks_labels_major, minor=False) # Set major y-ticks labels
# panel.set_yticks(depth_ticks_minor, minor=True) # Set minor y-ticks positions
#
plt.gca().invert_yaxis()
#
panel.tick_params(which='major',axis='both',direction='out',length=MAJOR_TICK_LENGTH, width=MAJOR_TICK_WIDTH)
panel.tick_params(which='minor',axis='both',direction='out',length=MINOR_TICK_LENGTH, width=MINOR_TICK_WIDTH)
#
panel.tick_params(axis='x', rotation=X_AXIS_TICK_ROTATION, labelsize=X_TICK_FONT_SIZE)
panel.tick_params(axis='y', rotation=Y_AXIS_TICK_ROTATION, labelsize=Y_TICK_FONT_SIZE)
#
panel.set_ylabel(r'Depth (m)',fontsize=Y_AXIS_LABEL_FONT_SIZE)
#
panel.set_title('(b)',loc='left',fontsize=PANEL_LABEL_FONT_SIZE)
#


#
#if DRAW_GRIDLINES:
#    panel.grid(which='both', color='k', linewidth=GRIDLINE_WIDTH)








 
#
## Put shared color bar under first two panels 
# 

color_bar_label=get_cbar_labels(PANEL_B_MEAN_STATE_VAR_NAME)

[lowest_panel_left,lowest_panel_bottom,lowest_panel_width,lowest_panel_height]=shifted_pos
lowest_panel_right= lowest_panel_left + lowest_panel_width


middle=0.5*(lowest_panel_right+lowest_panel_left)
width=COLORBAR_WIDTH_MULTIPLIER*(lowest_panel_right-lowest_panel_left)
shared_cbar_bottom=lowest_panel_bottom+COLORBAR_VERTICAL_SHIFT
left=middle-0.5*width


color_bar_ax=fig.add_axes([left,shared_cbar_bottom,width,COLORBAR_HEIGHT])
fig.colorbar(panel_with_colourbar, cax=color_bar_ax, orientation='horizontal')
color_bar_ax.set_title(color_bar_label,fontsize=COLORBAR_TITLE_FONT_SIZE)
if PANEL_A_CONTOUR_VAR_NAME == 'swpd':
    color_bar_ax.set_xticklabels(PANEL_B_CONTOUR_LEVELS+1000)
color_bar_ax.tick_params(labelsize=COLORBAR_TICK_FONT_SIZE)

 
















################################# Third plot panel c)


pos=locat.panel_position(2,0)
# Offset to allow for shared cbar above
shifted_pos=(pos[0], pos[1]  + PANEL_A_VERTICAL_SHIFT + PANEL_B_VERTICAL_SHIFT + PANEL_C_VERTICAL_SHIFT, pos[2], pos[3])
panel=fig.add_axes(shifted_pos)
plt.axes(panel)
plt.gca().patch.set_color('.3') # Dark grey
plt.gca().patch.set_edgecolor('k')
plt.gca().patch.set_hatch('++') 
# If var is a velocity apply a diverging colourscheme centred at 0. Otherwise apply designated cmap.
if PANEL_C_MEAN_STATE_VAR_NAME in ['ucur','vcur']:
    panel_c_colours=MFF.MFF_Get_Diverging_Colours(PANEL_C_MEAN_STATE_VAR_NAME, PANEL_C_CONTOUR_LEVELS)
    second_panel_with_colourbar=iplt.contourf(panel_c_cube, levels=PANEL_C_CONTOUR_LEVELS, coords=['longitude','level'], extend='both',colors=panel_c_colours)
else:
    panel_c_cmap=MFF.MFF_Assign_Variable_Colourmaps(PANEL_C_MEAN_STATE_VAR_NAME,False)
    second_panel_with_colourbar=iplt.contourf(panel_c_cube, levels=PANEL_C_CONTOUR_LEVELS, coords=['longitude','level'], extend='both',cmap=panel_c_cmap)
#
plt.gca().set_yscale('function', functions=(forward_depth_fun,inverse_depth_fun))
if SPLIT_DEPTH_SCALES_1_BOOL==True:
    plt.hlines(SPLIT_DEPTH_SCALES_1_DEPTH,LONG_BEG,LONG_END,colors='k')
if SPLIT_DEPTH_SCALES_2_BOOL==True:
    plt.hlines(SPLIT_DEPTH_SCALES_2_DEPTH,LONG_BEG,LONG_END,colors='k')
    #    
plt.xlim(LONG_BEG,LONG_END)
#
panel.set_xticks(long_ticks_major, minor=False) # Set major x-ticks positions
panel.set_xticks(long_ticks_minor, minor=True) # Set minor x-ticks positions
panel.set_xticklabels(long_ticks_labels_major, minor=False) # Set major x-ticks labels
panel.set_yticks(depth_ticks_major,  minor=False) # Set major y-ticks positions
panel.set_yticklabels(depth_ticks_labels_major, minor=False) # Set major y-ticks labels
# panel.set_yticks(depth_ticks_minor, minor=True) # Set minor y-ticks positions
#
plt.gca().invert_yaxis()
#
panel.tick_params(which='major',axis='both',direction='out',length=MAJOR_TICK_LENGTH, width=MAJOR_TICK_WIDTH)
panel.tick_params(which='minor',axis='both',direction='out',length=MINOR_TICK_LENGTH, width=MINOR_TICK_WIDTH)
#
panel.tick_params(axis='x', rotation=X_AXIS_TICK_ROTATION, labelsize=X_TICK_FONT_SIZE)
panel.tick_params(axis='y', rotation=Y_AXIS_TICK_ROTATION, labelsize=Y_TICK_FONT_SIZE)
#
panel.set_ylabel(r'Depth (m)',fontsize=Y_AXIS_LABEL_FONT_SIZE)
#
panel.set_title('(c)',loc='left',fontsize=PANEL_LABEL_FONT_SIZE)

#
#if DRAW_GRIDLINES:
#    panel.grid(which='both', color='k', linewidth=GRIDLINE_WIDTH)






#
## Put color bar under panel c
# 

color_bar_label=get_cbar_labels(PANEL_C_MEAN_STATE_VAR_NAME)

[lowest_panel_left,lowest_panel_bottom,lowest_panel_width,lowest_panel_height]=shifted_pos
lowest_panel_right= lowest_panel_left + lowest_panel_width


middle=0.5*(lowest_panel_right+lowest_panel_left)
width=COLORBAR_WIDTH_MULTIPLIER*(lowest_panel_right-lowest_panel_left)
shared_cbar_bottom=lowest_panel_bottom+COLORBAR_VERTICAL_SHIFT
left=middle-0.5*width


color_bar_ax=fig.add_axes([left,shared_cbar_bottom,width,COLORBAR_HEIGHT])
fig.colorbar(second_panel_with_colourbar, cax=color_bar_ax, orientation='horizontal')
color_bar_ax.set_title(color_bar_label,fontsize=COLORBAR_TITLE_FONT_SIZE)
color_bar_ax.tick_params(labelsize=COLORBAR_TICK_FONT_SIZE)

 
 
 
 
 
 
 
 
 
 
 



















#############################
#############################
#


########### Save the figure
IMAGEFILE=os.path.join(PLOTDIR,'mean_states.png')

if SAVE_HIGH_RES_BOOL:
    plt.savefig(IMAGEFILE,dpi=300)
else:
    plt.savefig(IMAGEFILE)
    
print('Figure saved to: '+IMAGEFILE)






