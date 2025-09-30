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

# Uni - local
#DATADIR=os.path.join(os.path.sep,'home','stusci1','rgq13jzu','Documents','MJO_WORK','data','glorys12v1eq1erai_zlev_d','processed'); PLOTDIR=os.path.join(os.path.sep,'home','stusci1','rgq13jzu','Documents','MJO_WORK','MJO_scripts','Plotting_Scripts','tmp')

###########
#
# Choose what data to plot


NSQUARED_FILENAME='smoothed_nsquared_all_2003-to-2020_ss_lat_-1.5_1.5.nc' # 



#
#
VAR='inferred_displacement'; contour_levels=np.array([-5,-1,-0.5,-0.1,0.1,0.5,1,5])  


TDOMAIN_WITHOUT_PHASE='rmm008FS-all'
#TDOMAIN_WITHOUT_PHASE='rmm008FS-PATAMA-all'
#TDOMAIN_WITHOUT_PHASE='rmm008FS-PATAMARECENT-all'



FILEPRE='_all_rac_b20_200_n241_'  # e.g. '_rac_'
PHASES_TO_PLOT=[1,2,3,4,5,6,7,8]
#PHASES_TO_PLOT=[1,2,3,4]
#PHASES_TO_PLOT=[5,6,7,8]
#PHASES_TO_PLOT=[5]
#PHASES_TO_PLOT=[1,3,5,7]



# Coastal and non-coastal ray start points are separated as coastal ones will be drawn with a thicker line
# Coastal start points are repeated for each phase (list of points)
COASTAL_RAY_START_POINTS = [(43,50), (118,50),  (312,50)]
# Non-coastal start points are individual for each phase (list of lists of points)
NONCOASTAL_RAY_START_POINTS_BY_PHASE = [  [(142,50),  (230,50)],  # Phase 1
                                          [(153,50),  (255,50)],  # Phase 2
                                          [(165,50),  (265,50)],  # Phase 3
                                          [(190,50),  (272,50)],  # Phase 4
                                          [(142,50),  (220,50)],  # Phase 5
                                          [(160,50),  (235,50)],  # Phase 6
                                          [(165,50),  (265,50)],  # Phase 7
                                          [(180,50),  (265,50)]   # Phase 8
                                        ]  





RAY_TIME_PERIOD_1_DAYS_LENGTH=30
RAY_TIME_PERIOD_2_DAYS_LENGTH=60 


LAGGED_MEAN_DAYS=0 # Lag of lagged_means to be plotted


FILE_SUFFIX = '_lag_ss_lat_-1.5_1.5.nc' 	# '_lag_ss_lat_-1.5_1.5.nc' for latitude averaged; 
#FILE_SUFFIX = '_lag.nc'			#'_lag.nc' for no averaging.





#LONG_BEG=-180; LONG_END=180 # Longitude plotting range (Default to -180:180, global)
LONG_BEG=30; LONG_END=390


LAT_VALUE=0









############
# Plotting options

SAVE_HIGH_RES_BOOL=True


LONG_MAJOR_TICK_STEP=30; LONG_MINOR_TICK_STEP=10


TEX_FIGURE_WIDTH_IN_PTS=397.48499


RAY_LINE_COLOUR = 'darkblue' 

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
PANEL_LABEL_X_POSITION=0.95 #  In figure units
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


COLORBAR_HEIGHT=0.021
COLORBAR_VERTICAL_SHIFT=-0.11 # Move colour bar up and down


DRAW_GRIDLINES=False # Set to True to add overlay gridlines
GRIDLINE_WIDTH=0.5


COASTAL_TRAJECTORY_LINEWIDTH=3



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

list_of_cubes=[]
data_max=[]
data_min=[]
panel_labels=[]
file_prefix=VAR+FILEPRE+TDOMAIN_WITHOUT_PHASE


for phase in PHASES_TO_PLOT:
    filename=file_prefix+str(phase)+FILE_SUFFIX
    file1=os.path.join(DATADIR,filename)
    #print('file1: {0!s}'.format(file1))
    panel_label="MJO Phase: "+str(phase)
    panel_labels.append(panel_label)
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
    list_of_cubes.append(cube)
    data_max.append(cube.data.max()) # List of all cubes maxs
    data_min.append(cube.data.min()) # List of all cubes mins   



print('Phase maxima:', data_max)
print('Phase minima:', data_min)







# Load Nsquared
nsquared_file=os.path.join(DATADIR,NSQUARED_FILENAME)
print('file1: {0!s}'.format(nsquared_file))
cubelist=iris.load(nsquared_file)   # Loads in a Cubelist of cubes
Nsquared=cubelist.concatenate_cube() #This line makes a cube from the cubelist
# point at 180 contains no data so remove it
longsCoord = Nsquared.coord('longitude')
lon_con=iris.Constraint(longitude = lambda cell:  (180-0.01 < cell) or (180+0.01) > cell)
Nsquared2=Nsquared.extract(lon_con)
Nsquared=Nsquared2.interpolate( [('longitude', longsCoord.points)], iris.analysis.Linear())



# Calculate ray paths
#
# Coastal first
coastal_trajectories_for_time_period_1 = MFF.MFF_ray_slope_from_Nsquared(Nsquared, COASTAL_RAY_START_POINTS, RAY_TIME_PERIOD_1_DAYS_LENGTH)
coastal_trajectories_for_time_period_2 = MFF.MFF_ray_slope_from_Nsquared(Nsquared, COASTAL_RAY_START_POINTS, RAY_TIME_PERIOD_2_DAYS_LENGTH)
#
# Now loop over noncoastal start points
noncoastal_trajectories_for_time_period_1_by_phase=[]
noncoastal_trajectories_for_time_period_2_by_phase=[]
for start_point_list in NONCOASTAL_RAY_START_POINTS_BY_PHASE:
    #
    trajectories_for_time_period_1 = MFF.MFF_ray_slope_from_Nsquared(Nsquared, start_point_list, RAY_TIME_PERIOD_1_DAYS_LENGTH)
    noncoastal_trajectories_for_time_period_1_by_phase.append(trajectories_for_time_period_1)
    #
    trajectories_for_time_period_2 = MFF.MFF_ray_slope_from_Nsquared(Nsquared, start_point_list, RAY_TIME_PERIOD_2_DAYS_LENGTH)
    noncoastal_trajectories_for_time_period_2_by_phase.append(trajectories_for_time_period_2)






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










###############################
###############################    
### 
# 

## Set up the figure and panel locations

panel_ratio=6

number_of_rows=len(PHASES_TO_PLOT)
number_of_columns=1




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


COLOURS=MFF.MFF_Get_Diverging_Colours(VAR,contour_levels)



icol=0
for ipanel, cube, panel_letter, row_label, trajectory_list_1, trajectory_list_2 in zip(range(number_of_rows), list_of_cubes, letters[0:number_of_rows+1], row_labels, noncoastal_trajectories_for_time_period_1_by_phase, noncoastal_trajectories_for_time_period_2_by_phase):
    irow=ipanel
    pos=locat.panel_position(irow,icol)
    panel=fig.add_axes(pos)

    plt.axes(panel)
    plt.gca().patch.set_color('.3') # Dark grey
    plt.gca().patch.set_edgecolor('k')
    plt.gca().patch.set_hatch('++') 
    #
    panel_with_plot=iplt.contourf(cube, levels=contour_levels, coords=['longitude','level'], extend='both',colors=COLOURS)
    # plot noncoastal ray trajectories
    for trajectory in trajectory_list_1:
        x=trajectory[0]
        z=trajectory[1]
        plt.plot(x,z,color=RAY_LINE_COLOUR, linestyle='--')        
    for trajectory in trajectory_list_2:
        x=trajectory[0]
        z=trajectory[1]
        plt.plot(x,z,color=RAY_LINE_COLOUR, linestyle='-')        
    # plot coastal trajectories
    for trajectory in coastal_trajectories_for_time_period_1:
        x=trajectory[0]
        z=trajectory[1]
        plt.plot(x,z,color=RAY_LINE_COLOUR, linestyle='--')
    for trajectory in coastal_trajectories_for_time_period_2:
        x=trajectory[0]
        z=trajectory[1]
        plt.plot(x,z,color=RAY_LINE_COLOUR, linestyle='-',linewidth=COASTAL_TRAJECTORY_LINEWIDTH)              
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
    plt.ylim(0,MAXIMUM_DEPTH)
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
    # Add Phase label on right
    panel.yaxis.set_label_position('right')
    panel.set_ylabel(row_label, rotation=270, va='bottom')





 
  
#
###############################
############################### Add the colourbar 

#
## Build the colour bar label string

color_bar_label = 'Vertical displacement (m)'
#

    



#
## Put the color bar under final panels 
# 


[lowest_panel_left, lowest_panel_bottom, lowest_panel_width, lowest_panel_height] = locat.panel_position( number_of_rows-1 , 0) 

lowest_panel_right = lowest_panel_left + lowest_panel_width


middle=0.5*(lowest_panel_right+lowest_panel_left)
width=COLORBAR_WIDTH_MULTIPLIER*(lowest_panel_right-lowest_panel_left)
bottom=lowest_panel_bottom+COLORBAR_VERTICAL_SHIFT
left=middle-0.5*width


color_bar_ax=fig.add_axes([left,bottom,width,COLORBAR_HEIGHT])
#fig.colorbar(panel_with_plot, cax=color_bar_ax, orientation='horizontal', label=color_bar_label)
fig.colorbar(panel_with_plot, cax=color_bar_ax, orientation='horizontal')
color_bar_ax.set_title(color_bar_label,fontsize=COLORBAR_TITLE_FONT_SIZE)
color_bar_ax.tick_params(labelsize=COLORBAR_TICK_FONT_SIZE)












#
## Put the y axis label on

# Calculate positions
[highest_panel_left,highest_panel_bottom,highest_panel_width,highest_panel_height]=locat.panel_position(0, 0) 
all_panel_height=highest_panel_bottom + highest_panel_height - lowest_panel_bottom
# Add the labels and hide the axes edges tick marks
shared_ylabel_ax=fig.add_axes([0.4*lowest_panel_left, lowest_panel_bottom, lowest_panel_left/4, all_panel_height] )
#shared_ylabel_ax=fig.add_axes([0.1*lowest_panel_left, lowest_panel_bottom, lowest_panel_left/10, all_panel_height] )
shared_ylabel_ax.set_ylabel('Depth (m)',fontsize=Y_AXIS_LABEL_FONT_SIZE)
shared_ylabel_ax.set_xticks([])
shared_ylabel_ax.set_yticks([])
shared_ylabel_ax.set_frame_on(False)


















#############################
#############################
#


########### Save the figure
IMAGEFILE=os.path.join(PLOTDIR,'depth_longitude_'+VAR+'_anomalies.png')
#IMAGEFILE=os.path.join(PLOTDIR,'tmp.png')

if SAVE_HIGH_RES_BOOL:
    plt.savefig(IMAGEFILE,dpi=300)
else:
    plt.savefig(IMAGEFILE)
    
print('Figure saved to: '+IMAGEFILE)




