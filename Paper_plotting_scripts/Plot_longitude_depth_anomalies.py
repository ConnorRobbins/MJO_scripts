#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 11:48:31 2023

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
#PLOTDIR=os.path.join(os.path.sep,'gpfs','home','rgq13jzu','MJO_scripts','Plotting_Scripts','Paper_Figures')



###########
#
# Choose what data to plot



VAR_1='swpd'; contour_levels_1=np.array([-0.04,-0.01,-0.005,-0.001,0.001,0.005,0.01,0.04])
VAR_2='ucur'; contour_levels_2=np.array([-0.04,-0.01,-0.001,0.001,0.01,0.04])



TDOMAIN_WITHOUT_PHASE='rmm008FS-all'
#TDOMAIN_WITHOUT_PHASE='rmm008FS-PATAMA-all'
#TDOMAIN_WITHOUT_PHASE='rmm008FS-PATAMARECENT-all'



FILEPRE='_all_rac_b20_200_n241_'  # e.g. '_rac_'
PHASES_TO_PLOT=[1,2,3,4,5,6,7,8]
#PHASES_TO_PLOT=[1,2,3,4]


LAGGED_MEAN_DAYS=0 # Lag of lagged_means to be plotted


FILE_SUFFIX = '_lag_ss_lat_-1.5_1.5.nc' 	# '_lag_ss_lat_-1.5_1.5.nc' for latitude averaged; 
#FILE_SUFFIX = '_lag.nc'			#'_lag.nc' for no averaging.





#LONG_BEG=-180; LONG_END=180 # Longitude plotting range (Default to -180:180, global)
#LONG_BEG=40; LONG_END=280 # Matches Patama's plots
LONG_BEG=30; LONG_END=390


LAT_VALUE=0



MJO_OLR_CENTRE_LONGITUDES_BY_PHASE = [69, 84, 90, 103, 122, 160, 177, 196]
MJO_OLR_CENTRE_VERTICAL_SHIFT=-10
MJO_OLR_CENTRE_CIRCLE_SIZE = 5 # Font size for the "space" that creates the circles



############
# Plotting options

SAVE_HIGH_RES_BOOL=True

NUMBER_OF_COLUMNS=2

LONG_MAJOR_TICK_STEP=30; LONG_MINOR_TICK_STEP=10


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

X_AXIS_TICK_ROTATION=90
Y_AXIS_TICK_ROTATION=0

PANEL_LABEL_FONT_SIZE=7
PANEL_LABEL_X_POSITION=0.90 #  In figure units
PANEL_LABEL_Y_POSITION=0.10 #  In figure units


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


COLORBAR_HEIGHT=0.014
COLORBAR_VERTICAL_SHIFT=-0.11 # Move colour bar up and down
    





DRAW_GRIDLINES=False # Set to True to add overlay gridlines
GRIDLINE_WIDTH=0.5





###########################
###########################
###########################
###########################





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



###############################
###############################    
### 
# 









#
###
###############################
###############################  Load the data and package it up ready for the plotting, find extreme values while there


### Load the data, making a list of the cubes and work out the extreme data values to set the contour levels 





## First for VAR_1

list_of_cubes_1=[]
data_max_1=[]
data_min_1=[]
panel_labels_1=[]
file_prefix_1=VAR_1+FILEPRE+TDOMAIN_WITHOUT_PHASE


for phase in PHASES_TO_PLOT:
    filename=file_prefix_1+str(phase)+FILE_SUFFIX
    file1=os.path.join(DATADIR,filename)
    #print('file1: {0!s}'.format(file1))
    cubelist=iris.load(file1)   # Loads in a Cubelist of cubes
    cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist
    #Extract data for correct latitude value
    latIndex=cube.coord('latitude').nearest_neighbour_index(LAT_VALUE)
    latCoord=cube.coord('latitude')[latIndex]
    latValue=latCoord.cell(0)[0]
    cubeConstraints=iris.Constraint(latitude=latValue)
    cube=cube.extract(cubeConstraints)
    #Extract data for correct length lag on lagged mean
    tcoord=cube.coord('time')
    tn=tcoord.units.num2date(tcoord.points[tcoord.points==LAGGED_MEAN_DAYS*24.0])
    timecon=iris.Constraint(time=tn)
    with warnings.catch_warnings(): # Iris will print a deprecation warning every time otherwise
        warnings.simplefilter("ignore")
        with iris.FUTURE.context(cell_datetime_objects=True):
            cube=cube.extract(timecon) # Extract data with correct lag
    # Extract data above the maximum depth
    cubeConstraints=iris.Constraint(level=lambda cell: cell < MAXIMUM_DEPTH) 
    cube=cube.extract(cubeConstraints)
    #Extract data for correct longitudes and shuffle the cube around for circular plotting, jump over 180 degree data point
    cube.coord('longitude').attributes['modulo']=360
    cube_west_longs=cube.extract(iris.Constraint(longitude=lambda cell: (180 < cell) and (cell < 360)))
    cube_east_longs=cube.extract(iris.Constraint(longitude=lambda cell: (0 <= cell) and (cell < 180)))
    cube_west_longs.coord('longitude').bounds=cube_west_longs.coord('longitude').bounds-360
    cube_west_longs.coord('longitude').points=cube_west_longs.coord('longitude').points-360
    cube=iris.cube.CubeList([cube_west_longs,cube_east_longs]).concatenate()[0]
    cube.coord('longitude').circular=True
    cube=cube.intersection(longitude=(LONG_BEG,LONG_END))
    list_of_cubes_1.append(cube)
    data_max_1.append(cube.data.max()) # List of all cubes maxs
    data_min_1.append(cube.data.min()) # List of all cubes mins   



## Then for VAR_2

list_of_cubes_2=[]
data_max_2=[]
data_min_2=[]
panel_labels_2=[]
file_prefix_2=VAR_2+FILEPRE+TDOMAIN_WITHOUT_PHASE


for phase in PHASES_TO_PLOT:
    filename=file_prefix_2+str(phase)+FILE_SUFFIX
    file1=os.path.join(DATADIR,filename)
    #print('file1: {0!s}'.format(file1))
    panel_label="MJO Phase: "+str(phase)
    panel_labels_2.append(panel_label)
    cubelist=iris.load(file1)   # Loads in a Cubelist of cubes
    cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist
    #Extract data for correct latitude value
    latIndex=cube.coord('latitude').nearest_neighbour_index(LAT_VALUE)
    latCoord=cube.coord('latitude')[latIndex]
    latValue=latCoord.cell(0)[0]
    cubeConstraints=iris.Constraint(latitude=latValue)
    cube=cube.extract(cubeConstraints)
    #Extract data for correct length lag on lagged mean
    tcoord=cube.coord('time')
    tn=tcoord.units.num2date(tcoord.points[tcoord.points==LAGGED_MEAN_DAYS*24.0])
    timecon=iris.Constraint(time=tn)
    with warnings.catch_warnings(): # Iris will print a deprecation warning every time otherwise
        warnings.simplefilter("ignore")
        with iris.FUTURE.context(cell_datetime_objects=True):
            cube=cube.extract(timecon) # Extract data with correct lag
    # Extract data above the maximum depth
    cubeConstraints=iris.Constraint(level=lambda cell: cell < MAXIMUM_DEPTH) 
    cube=cube.extract(cubeConstraints)
    #Extract data for correct longitudes and shuffle the cube around for circular plotting, jump over 180 degree data point
    cube.coord('longitude').attributes['modulo']=360
    cube_west_longs=cube.extract(iris.Constraint(longitude=lambda cell: (180 < cell) and (cell < 360)))
    cube_east_longs=cube.extract(iris.Constraint(longitude=lambda cell: (0 <= cell) and (cell < 180)))
    cube_west_longs.coord('longitude').bounds=cube_west_longs.coord('longitude').bounds-360
    cube_west_longs.coord('longitude').points=cube_west_longs.coord('longitude').points-360
    cube=iris.cube.CubeList([cube_west_longs,cube_east_longs]).concatenate()[0]
    cube.coord('longitude').circular=True
    cube=cube.intersection(longitude=(LONG_BEG,LONG_END))
    list_of_cubes_2.append(cube)
    data_max_2.append(cube.data.max()) # List of all cubes maxs
    data_min_2.append(cube.data.min()) # List of all cubes mins   








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










###############################
###############################    
### 
# 




## Set up the figure and panel locations

panel_ratio=3.2

number_of_rows=len(PHASES_TO_PLOT)
number_of_columns=2




figure_width_in_mm=(TEX_FIGURE_WIDTH_IN_PTS/72.27)*25.4
left_padding=1.5*figure_width_in_mm/10
right_padding=figure_width_in_mm/20
top_padding=right_padding*0.8
bottom_padding=right_padding*5
horizontal_sep=right_padding/1.3
vertical_sep=4







locat=FigureSizeLocator(rows=number_of_rows, columns=number_of_columns, figwidth=figure_width_in_mm, panelratio=panel_ratio, hsep=horizontal_sep, vsep=vertical_sep, padleft=left_padding, padright=right_padding, padtop=top_padding, padbottom=bottom_padding, units='mm')


fig=plt.figure(figsize=locat.figsize)












#
###
###############################
############################### Plot the lagged mean contour panels

centre_longitude=((LONG_BEG+LONG_END)/2)
axes_projection=None



letters=['a','b','c','d','e','f','g','h','i','j','k','l', 'm','n','o','p','q','r','s','t','u','v','w','x','y','z']


row_labels=["Phase "+ str(phase) for phase in PHASES_TO_PLOT]





## Loop over first column and plot


COLOURS=MFF.MFF_Get_Diverging_Colours(VAR_1,contour_levels_1)



icol=0
for ipanel, cube, panel_letter, MJO_centre_x_coord in zip(range(number_of_rows), list_of_cubes_1, letters[0:number_of_rows+1], MJO_OLR_CENTRE_LONGITUDES_BY_PHASE):
    irow=ipanel
    pos=locat.panel_position(irow,icol)
    panel=fig.add_axes(pos)

    plt.axes(panel)
    plt.gca().patch.set_color('.3') # Dark grey
    plt.gca().patch.set_edgecolor('k')
    plt.gca().patch.set_hatch('++') 
    #
    panel_with_plot_1=iplt.contourf(cube, levels=contour_levels_1, coords=['longitude','level'], extend='both',colors=COLOURS)
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
    if (irow==number_of_rows-1) or not SHARE_X_TICKS_BOOL:
        panel.set_xticklabels(long_ticks_labels_major, minor=False) # Set major x-ticks labels
    else:
        panel.set_xticklabels([],minor=False)
    ####### you were here ####
    #
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
    panel_label_string = "(" + panel_letter + ")"
    panel.text(PANEL_LABEL_X_POSITION, PANEL_LABEL_Y_POSITION,panel_label_string,transform=panel.transAxes,bbox=dict(boxstyle='square,pad=0.2',facecolor='white', alpha=1),fontsize=PANEL_LABEL_FONT_SIZE)
    #
    if DRAW_GRIDLINES:
        panel.grid(which='both', color='k', linewidth=GRIDLINE_WIDTH)
    # Add circle above plot for MJO OLR centre
    panel.text(MJO_centre_x_coord, MJO_OLR_CENTRE_VERTICAL_SHIFT ,' ',bbox=dict(boxstyle='circle,pad=0.05',facecolor='red', alpha=1), fontsize=MJO_OLR_CENTRE_CIRCLE_SIZE)
















## Loop over second column and plot


COLOURS=MFF.MFF_Get_Diverging_Colours(VAR_2,contour_levels_2)

icol=1
for ipanel, cube, row_label, panel_letter, MJO_centre_x_coord  in zip(range(number_of_rows), list_of_cubes_2, row_labels, letters[number_of_rows : 2*number_of_rows], MJO_OLR_CENTRE_LONGITUDES_BY_PHASE):
    irow=ipanel
    pos=locat.panel_position(irow,icol)
    panel=fig.add_axes(pos)

    plt.axes(panel)
    plt.gca().patch.set_color('.3') # Dark grey
    plt.gca().patch.set_edgecolor('k')
    plt.gca().patch.set_hatch('++') 
    #
    panel_with_plot_2=iplt.contourf(cube, levels=contour_levels_2, coords=['longitude','level'], extend='both',colors=COLOURS)
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
    if (irow==number_of_rows-1) or not SHARE_X_TICKS_BOOL:
        panel.set_xticklabels(long_ticks_labels_major, minor=False) # Set major x-ticks labels
    else:
        panel.set_xticklabels([],minor=False)
    #
    panel.set_yticks(depth_ticks_major,  minor=False) # Set major y-ticks positions
    panel.set_yticklabels([], minor=False) # Set major y-ticks labels
    # panel.set_yticks(depth_ticks_minor, minor=True) # Set minor y-ticks positions
    #
    plt.gca().invert_yaxis()
    #
    panel.tick_params(which='major',axis='both',direction='out',length=MAJOR_TICK_LENGTH, width=MAJOR_TICK_WIDTH)
    panel.tick_params(which='minor',axis='both',direction='out',length=MINOR_TICK_LENGTH, width=MINOR_TICK_WIDTH)
    #
    panel.tick_params(axis='x', rotation=X_AXIS_TICK_ROTATION, labelsize=X_TICK_FONT_SIZE)
    #
    panel_label_string = "(" + panel_letter + ")"
    panel.text(PANEL_LABEL_X_POSITION, PANEL_LABEL_Y_POSITION,panel_label_string,transform=panel.transAxes,bbox=dict(boxstyle='square,pad=0.2',facecolor='white', alpha=1),fontsize=PANEL_LABEL_FONT_SIZE)
    #
    if DRAW_GRIDLINES:
        panel.grid(which='both', color='k', linewidth=GRIDLINE_WIDTH)
    # Add circle above plot for MJO OLR centre
    panel.text(MJO_centre_x_coord, MJO_OLR_CENTRE_VERTICAL_SHIFT ,' ',bbox=dict(boxstyle='circle,pad=0.05',facecolor='red', alpha=1), fontsize=MJO_OLR_CENTRE_CIRCLE_SIZE)
    #
    # Add Phase label on right
    panel.yaxis.set_label_position('right')
    panel.set_ylabel(row_label, rotation=270, va='bottom')
    











 
  
#
###############################
############################### Add the colourbars 



def cbar_label_assigner(var_name):
    if var_name=='swtheta':
        color_bar_label = 'Potential temperature anomaly ($^\circ$C)'
    elif var_name=='swsal':
        color_bar_label = 'Absolute salinity anomaly (g kg$^{-1}$)'
    elif var_name=='ucur':
        color_bar_label = 'Zonal velocity anomaly (m s$^{-1}$)'
    elif var_name=='vcur':
        color_bar_label = 'Meridional velocity anomaly (m s$^{-1}$)'
    elif var_name=='swpd':
        color_bar_label = 'Potential density anomaly (kg m$^{-3}$)'
    else:
        color_bar_label = ''
        warnings.warn("VAR not recognised for generating label, please check what you are plotting.")
    return color_bar_label
    
#
## Build the colour bar label string
#

color_bar_label_1=cbar_label_assigner(VAR_1)
color_bar_label_2=cbar_label_assigner(VAR_2)


#
## Put the color bar under final panels  on column 1
# 


[lowest_panel_left, lowest_panel_bottom, lowest_panel_width, lowest_panel_height]=locat.panel_position( number_of_rows-1 , 0) 
lowest_panel_right= lowest_panel_left + lowest_panel_width


middle=0.5*(lowest_panel_right+lowest_panel_left)
width=COLORBAR_WIDTH_MULTIPLIER*(lowest_panel_right-lowest_panel_left)
bottom=lowest_panel_bottom+COLORBAR_VERTICAL_SHIFT
left=middle-0.5*width


color_bar_ax_1=fig.add_axes([left,bottom,width,COLORBAR_HEIGHT])
fig.colorbar(panel_with_plot_1, cax=color_bar_ax_1, orientation='horizontal', label=color_bar_label_1)
fig.colorbar(panel_with_plot_1, cax=color_bar_ax_1, orientation='horizontal')
color_bar_ax_1.set_title(color_bar_label_1, fontsize=COLORBAR_TITLE_FONT_SIZE)
color_bar_ax_1.tick_params(labelsize=COLORBAR_TICK_FONT_SIZE, rotation=COLORBAR_TICK_LABEL_ROTATION)



#
## Put the color bar under final panels  on column 2
# 


[lowest_panel_left, lowest_panel_bottom, lowest_panel_width, lowest_panel_height]=locat.panel_position( number_of_rows-1 , 1) 
lowest_panel_right= lowest_panel_left + lowest_panel_width


middle=0.5*(lowest_panel_right+lowest_panel_left)
width=COLORBAR_WIDTH_MULTIPLIER*(lowest_panel_right-lowest_panel_left)
bottom=lowest_panel_bottom+COLORBAR_VERTICAL_SHIFT
left=middle-0.5*width


color_bar_ax_2=fig.add_axes([left,bottom,width,COLORBAR_HEIGHT])
fig.colorbar(panel_with_plot_2, cax=color_bar_ax_2, orientation='horizontal', label=color_bar_label_2)
fig.colorbar(panel_with_plot_2, cax=color_bar_ax_2, orientation='horizontal')
color_bar_ax_2.set_title(color_bar_label_2, fontsize=COLORBAR_TITLE_FONT_SIZE)
color_bar_ax_2.tick_params(labelsize=COLORBAR_TICK_FONT_SIZE, rotation=COLORBAR_TICK_LABEL_ROTATION)














#
## Put the y axis label on

# Calculate positions
[highest_panel_left,highest_panel_bottom,highest_panel_width,highest_panel_height]=locat.panel_position(0, 0) 
all_panel_height=highest_panel_bottom + highest_panel_height - lowest_panel_bottom
# Add the labels and hide the axes edges tick marks
#shared_ylabel_ax=fig.add_axes([0.4*lowest_panel_left, lowest_panel_bottom, lowest_panel_left/4, all_panel_height] )
shared_ylabel_ax=fig.add_axes([0.1*lowest_panel_left, lowest_panel_bottom, lowest_panel_left/10, all_panel_height] )
shared_ylabel_ax.set_ylabel('Depth (m)',fontsize=Y_AXIS_LABEL_FONT_SIZE)
shared_ylabel_ax.set_xticks([])
shared_ylabel_ax.set_yticks([])
shared_ylabel_ax.set_frame_on(False)







#############################
#############################
#


########### Save the figure
IMAGEFILE=os.path.join(PLOTDIR,'longitude_depth_anomalies.png')
#IMAGEFILE=os.path.join(PLOTDIR,'tmp.png')

if SAVE_HIGH_RES_BOOL:
    plt.savefig(IMAGEFILE,dpi=300)
else:
    plt.savefig(IMAGEFILE)
    
print('Figure saved to: '+IMAGEFILE)






