#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 12:00:00 2024

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
WIND_DATADIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data','era5gloerai_sfc_d','processed'); 

PLOTDIR=os.path.join(os.path.sep,'gpfs','home','rgq13jzu','MJO_scripts','Plotting_Scripts','Paper_Figures','Plotting_Scripts','Figures')


###########
#
# Choose what data to plot



#
#
VAR='swtheta'; contour_levels=np.array([-0.1, -0.05, -0.02, -0.01, 0.01, 0.02, 0.05, 0.1]) # Sets levels for SWTHETA

#WIND_U_VAR= 'uwnd' ; WIND_V_VAR= 'vwnd'      # uwnd and vwnd for wind speed 
WIND_U_VAR= 'taux' ; WIND_V_VAR= 'tauy'      # taux and tauy for wind stress




LEVEL='0.494'
WIND_LEVEL='1'

TDOMAIN_WITHOUT_PHASE='rmm008FS-all'
#TDOMAIN_WITHOUT_PHASE='rmm008FS-PATAMA-all'
#TDOMAIN_WITHOUT_PHASE='rmm008FS-PATAMARECENT-all'



FILEPRE='_rac_b20_200_n241_'  # e.g. '_rac_'
PHASES_TO_PLOT=[1,2,3,4,5,6,7,8]






#MJO_OLR_CENTRE_LONGITUDES_BY_PHASE = [ 70, 85, 90, 105, 120, 155, 170, 190 ]  
MJO_OLR_CENTRE_LONGITUDES_BY_PHASE = [69, 84, 90, 103, 122, 160, 177, 196]




LAGGED_MEAN_DAYS=0 # Lag of lagged_means to be plotted


FILE_SUFFIX = '_lag.nc'			#'_lag.nc' for no averaging.





#LONG_BEG=-180; LONG_END=180 # Longitude plotting range (Default to -180:180, global)
LONG_BEG=30; LONG_END=390


LAT_BEG=-15; LAT_END=15 # Longitude values between which to plot

LAT_VALUE=0









############
# Plotting options

SAVE_HIGH_RES_BOOL=True


LONG_MAJOR_TICK_STEP=30; LONG_MINOR_TICK_STEP=10
LAT_MAJOR_TICK_STEP=15; LAT_MINOR_TICK_STEP=5  

TEX_FIGURE_WIDTH_IN_PTS=397.48499




#########





X_AXIS_LABEL_FONT_SIZE=10
Y_AXIS_LABEL_FONT_SIZE=10

X_AXIS_TICK_ROTATION=90
Y_AXIS_TICK_ROTATION=0

PANEL_LABEL_FONT_SIZE=7
PANEL_LABEL_X_POSITION=0.887 #  In figure units
PANEL_LABEL_Y_POSITION=0.15 #  In figure units

PHASE_LABEL_X_OFFSET=-0.05 # In figure units, measured from RHS of tick bbox

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
COLORBAR_VERTICAL_SHIFT=-0.13 # Move colour bar up and down
COLORBAR_HORIZONTAL_SHIFT=-0.025 # Move colour bar left and right

DRAW_GRIDLINES=False # Set to True to add overlay gridlines
GRIDLINE_WIDTH=0.5


# Step size for sampling data in order to draw velocity arrows
X_QUIVER_STEP=10
Y_QUIVER_STEP=6

NORMALISE_TO_UNIT_ARROWS_BOOL=False   # True makes all arrows same length
ARROW_SCALE_FACTOR=3

QUIVER_KEY_EXAMPLE_MAGNITUDE=0.025
QUIVER_KEY_EXAMPLE_X=0.7
QUIVER_KEY_EXAMPLE_Y=1.3




###########################
###########################
###########################
###########################





#
###
###############################
###############################  Run some initial checks on the settings so that if it's definitely going to break you don't wait as long to find out. 




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

## Longitude

# Round the values for making ticks
long_beg_major_round=LONG_BEG
long_end_major_round=LONG_END
long_beg_minor_round=LONG_BEG
long_end_minor_round=LONG_END

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

# Round the values for making ticks
lat_beg_major_round=LAT_BEG
lat_end_major_round=LAT_END
lat_beg_minor_round=LAT_BEG
lat_end_minor_round=LAT_END

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


### Load the data, making a list of the cubes and work out the extreme data values 

centre_longitude=((LONG_BEG+LONG_END)/2)


list_of_cubes=[]
data_max=[]
data_min=[]
panel_labels=[]
file_prefix=VAR+'_'+LEVEL+FILEPRE+TDOMAIN_WITHOUT_PHASE

wind_u_file_prefix = WIND_U_VAR+'_'+WIND_LEVEL+FILEPRE+TDOMAIN_WITHOUT_PHASE
wind_v_file_prefix = WIND_V_VAR+'_'+WIND_LEVEL+FILEPRE+TDOMAIN_WITHOUT_PHASE
vector_u_data_unnormalised_list=[]
vector_v_data_unnormalised_list=[]
vector_u_data_list=[]
vector_v_data_list=[]



# Load wind data, extract and normalise
for phase in PHASES_TO_PLOT:
    #
    #### load data
    #
    # u data
    u_filename=wind_u_file_prefix+str(phase)+FILE_SUFFIX
    u_file=os.path.join(WIND_DATADIR,u_filename)
    #print('u data: {0!s}'.format(u_file))
    cubelist=iris.load(u_file)   # Loads in a Cubelist of cubes
    u_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist
    u_cube=MFF.MFF_Cube_Extract_Lagged_Mean_Days_Data(u_cube, LAGGED_MEAN_DAYS)
    u_cube=MFF.MFF_Cube_Circular_Spatial_Subset(u_cube, [LAT_BEG,LAT_END], [LONG_BEG,LONG_END])
    #
    # v data
    v_filename=wind_v_file_prefix+str(phase)+FILE_SUFFIX
    v_file=os.path.join(WIND_DATADIR,v_filename)
    #print('v data: {0!s}'.format(v_file))
    cubelist=iris.load(v_file)   # Loads in a Cubelist of cubes
    v_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist
    v_cube=MFF.MFF_Cube_Extract_Lagged_Mean_Days_Data(v_cube, LAGGED_MEAN_DAYS)
    v_cube=MFF.MFF_Cube_Circular_Spatial_Subset(v_cube, [LAT_BEG,LAT_END], [LONG_BEG,LONG_END])
    #
    ### Extract data
    u_data = u_cube[::Y_QUIVER_STEP,::X_QUIVER_STEP].data
    v_data = v_cube[::Y_QUIVER_STEP,::X_QUIVER_STEP].data
    #
    ## Store
    vector_u_data_unnormalised_list.append(u_data)
    vector_v_data_unnormalised_list.append(v_data)
    
# Store sampled longitudes and latitudes and then calculate scalings for the plot
vector_longitudes = u_cube.coord('longitude').points[::X_QUIVER_STEP]-centre_longitude
vector_latitudes = u_cube.coord('latitude').points[::Y_QUIVER_STEP]
vector_x, vector_y=np.meshgrid(vector_longitudes,vector_latitudes)

long_per_plot_index=abs((vector_longitudes[-1]-vector_longitudes[0])/len(vector_longitudes))
lat_per_plot_index=abs((vector_latitudes[-1]-vector_latitudes[0])/len(vector_latitudes))
arrow_scaling= 1/(  2* min(lat_per_plot_index,long_per_plot_index))


# Loop over wind data again to apply normalisation
# must loop twice if not unit arrows to find max abs value
if NORMALISE_TO_UNIT_ARROWS_BOOL:
    for u_tmp, v_tmp in zip(vector_u_data_unnormalised_list,vector_v_data_unnormalised_list):
        normalisation=np.sqrt(u_tmp**2 + v_tmp**2)
        vector_u_data_list.append(u_tmp/normalisation)
        vector_v_data_list.append(v_tmp/normalisation)
else:
    norm_list=[]
    for u_tmp, v_tmp in zip(vector_u_data_unnormalised_list,vector_v_data_unnormalised_list):
        norm_list.append(np.sqrt(u_tmp**2 + v_tmp**2).max())
    print('Largest absolute wind variable magnitudes:', norm_list)
    normalisation=np.max(norm_list)
    for u_tmp, v_tmp in zip(vector_u_data_unnormalised_list,vector_v_data_unnormalised_list):
        vector_u_data_list.append(u_tmp/normalisation)
        vector_v_data_list.append(v_tmp/normalisation)










# Load VAR data and make some labels
for phase in PHASES_TO_PLOT:
    panel_label="MJO Phase: "+str(phase)
    panel_labels.append(panel_label)
    #
    filename=file_prefix+str(phase)+FILE_SUFFIX
    file1=os.path.join(DATADIR,filename)
    #print('file1: {0!s}'.format(file1))
    cubelist=iris.load(file1)   # Loads in a Cubelist of cubes
    cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist
    tcoord=cube.coord('time')
    tn=tcoord.units.num2date(tcoord.points[tcoord.points==LAGGED_MEAN_DAYS*24.0])
    timecon=iris.Constraint(time=tn)
    with warnings.catch_warnings(): # Iris will print a deprecation warning every time otherwise
        warnings.simplefilter("ignore")
        with iris.FUTURE.context(cell_datetime_objects=True):
            cube=cube.extract(timecon) # Extract data with correct lag
    data_cube_at_phase=MFF.MFF_Cube_Circular_Spatial_Subset(cube, [LAT_BEG,LAT_END], [LONG_BEG,LONG_END])
    data_max.append(data_cube_at_phase.data.max()) # List of all cubes maxs
    data_min.append(data_cube_at_phase.data.min()) # List of all cubes mins   
    list_of_cubes.append(data_cube_at_phase)







print('Contour variable phase maxima:', data_max)
print('Contour variable phase minima:', data_min)























###############################
###############################    
### 
# 








###############################
###############################    
### 
# 

## Set up the figure and panel locations

#panel_ratio=6
panel_ratio=(LONG_END-LONG_BEG)/(LAT_END-LAT_BEG)

number_of_rows=len(PHASES_TO_PLOT)
number_of_columns=1




figure_width_in_mm=(TEX_FIGURE_WIDTH_IN_PTS/72.27)*25.4
left_padding_in_mm=15
right_padding_in_mm=1
bottom_padding_in_mm=30
vertical_sep_in_mm=6
top_padding_in_mm=8
horizontal_sep_in_mm=1







locat=FigureSizeLocator(rows=number_of_rows, columns=number_of_columns, figwidth=figure_width_in_mm, panelratio=panel_ratio, hsep=horizontal_sep_in_mm, vsep=vertical_sep_in_mm, padleft=left_padding_in_mm, padright=right_padding_in_mm, padtop=top_padding_in_mm, padbottom=bottom_padding_in_mm, units='mm')


fig=plt.figure(figsize=locat.figsize)
















#
###
###############################
############################### Plot the lagged mean contour panels


axes_projection=ccrs.PlateCarree(central_longitude=centre_longitude)
tick_projection=ccrs.PlateCarree(central_longitude=centre_longitude)


letters=['a','b','c','d','e','f','g','h','i','j','k','l', 'm','n','o','p','q','r','s','t','u','v','w','x','y','z']


row_labels=["Phase "+ str(phase) for phase in PHASES_TO_PLOT]


COLOURS=MFF.MFF_Get_Diverging_Colours(VAR,contour_levels)





## Loop over rows and plot
if WIND_U_VAR=='taux':
    quiver_key_string = str(QUIVER_KEY_EXAMPLE_MAGNITUDE) + r' N m$^{-2}$'
elif WIND_U_VAR=='uwnd':
    quiver_key_string = str(QUIVER_KEY_EXAMPLE_MAGNITUDE) + r' m s$^{-1}$'
else:
    quiver_key_string ='Check quiver variable'




icol=0
for ipanel, cube, panel_letter, row_label, vector_u, vector_v, MJO_centre_x_coord in zip(range(number_of_rows), list_of_cubes, letters[0:number_of_rows+1], row_labels, vector_u_data_list, vector_v_data_list, MJO_OLR_CENTRE_LONGITUDES_BY_PHASE):
    # Create axes for next plot in loop
    #
    irow=ipanel
    pos=locat.panel_position(irow,icol)
    panel=fig.add_axes(pos,projection=axes_projection)
    plt.axes(panel)
    #
    # Contour plot
    panel_with_plot=iplt.contourf(cube, levels=contour_levels, coords=['longitude','latitude'], extend='both',colors=COLOURS)
    #
    # Quiver plot
    panel_with_quiver=plt.quiver(vector_x, vector_y, vector_u, vector_v, angles='uv', pivot='middle', scale=len(vector_latitudes)/ARROW_SCALE_FACTOR, minlength=0.5, scale_units='height',units='height',minshaft=2)
    if irow==0 and not NORMALISE_TO_UNIT_ARROWS_BOOL:
        plt.quiverkey(Q=panel_with_quiver, X=QUIVER_KEY_EXAMPLE_X, Y=QUIVER_KEY_EXAMPLE_Y, U=QUIVER_KEY_EXAMPLE_MAGNITUDE/normalisation, angle=0 ,label=quiver_key_string, labelpos='E')
    #
    plt.xlim(LONG_BEG,LONG_END-180)
    #
    plt.gca().coastlines()
    #
    panel.set_xticks(long_ticks_major-centre_longitude, crs=tick_projection, minor=False) # Set major x-ticks positions
    panel.set_xticks(long_ticks_minor-centre_longitude, crs=tick_projection, minor=True) # Set minor x-ticks positions
    if (irow==number_of_rows-1) or not SHARE_X_TICKS_BOOL:
        panel.set_xticklabels(long_ticks_labels_major, minor=False) # Set major x-ticks labels
    else:
        panel.set_xticklabels([],minor=False)
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
    #
    panel_label_string = "(" + panel_letter + ")"
    panel.text(PANEL_LABEL_X_POSITION, PANEL_LABEL_Y_POSITION,panel_label_string,transform=panel.transAxes,bbox=dict(boxstyle='square,pad=0.2',facecolor='white', alpha=1),fontsize=PANEL_LABEL_FONT_SIZE)
    #
    if DRAW_GRIDLINES:
        panel.grid(which='both', color='k', linewidth=GRIDLINE_WIDTH)
    # Add Phase label on right
    panel.yaxis.set_label_position('right')
    panel.set_ylabel(row_label, rotation=270, va='bottom')
    panel.yaxis.set_label_coords(1+PHASE_LABEL_X_OFFSET, 0.5)
    # Add circle for MJO OLR centre
    # panel.text(MJO_centre_x_coord-centre_longitude, LAT_END+4 ,' ',bbox=dict(boxstyle='circle,pad=0.05',facecolor='red', alpha=1),fontsize=PANEL_LABEL_FONT_SIZE) # above plots
    panel.text(MJO_centre_x_coord-centre_longitude, 0 ,' ',bbox=dict(boxstyle='circle,pad=0.05',facecolor='red', alpha=1),fontsize=PANEL_LABEL_FONT_SIZE, verticalalignment='center',) # on equator




 
  
#
###############################
############################### Add the colourbar 
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

#color_bar_label = cbar_label_assigner(VAR)
color_bar_label = 'SST anomaly ($^\circ$C)'
#

    



#
## Put the color bar under final panels 
# 


[lowest_panel_left, lowest_panel_bottom, lowest_panel_width, lowest_panel_height] = locat.panel_position( number_of_rows-1 , 0) 

lowest_panel_right = lowest_panel_left + lowest_panel_width


middle=0.5*(lowest_panel_right+lowest_panel_left)
width=COLORBAR_WIDTH_MULTIPLIER*(lowest_panel_right-lowest_panel_left)
bottom=lowest_panel_bottom+COLORBAR_VERTICAL_SHIFT
left=middle-0.5*width+COLORBAR_HORIZONTAL_SHIFT


color_bar_ax=fig.add_axes([left,bottom,width,COLORBAR_HEIGHT])
#fig.colorbar(panel_with_plot, cax=color_bar_ax, orientation='horizontal', label=color_bar_label)
fig.colorbar(panel_with_plot, cax=color_bar_ax, orientation='horizontal')
color_bar_ax.set_title(color_bar_label,fontsize=COLORBAR_TITLE_FONT_SIZE)
color_bar_ax.tick_params(labelsize=COLORBAR_TICK_FONT_SIZE)

















#############################
#############################
#


########### Save the figure
IMAGEFILE=os.path.join(PLOTDIR,'SST_and_wind_stress_anomalies_by_phase.png')


if SAVE_HIGH_RES_BOOL:
    plt.savefig(IMAGEFILE,dpi=300)
else:
    plt.savefig(IMAGEFILE)
    
print('Figure saved to: '+IMAGEFILE)




