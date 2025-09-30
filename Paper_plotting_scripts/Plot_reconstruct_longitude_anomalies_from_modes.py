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
DATADIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data','glorys12v1aeq1erai_zlev_d','processed')

PLOTDIR=os.path.join(os.path.sep,'gpfs','home','rgq13jzu','MJO_scripts','Plotting_Scripts','Paper_Figures','Plotting_Scripts','Figures')


###########
#
# Choose what data to plot



VAR_1='swpd'; contour_levels_1=np.array([-0.04,-0.01,-0.005,-0.001,0.001,0.005,0.01,0.04]);
MODES_FILENAME_1='rmodes_normalised_5m_all_2003-to-2020_ss_lat_-1.5_1.5.nc'; PROJECTIONS_FILENAME_1='swpd_all_rac_b20_200_n241_rmm008FS-all3_lag_ss_lat_-1.5_1.5_projected_onto_rmodes_normalised_5m_all_2003-to-2020_ss_lat_-1.5_1.5.nc'; 


VAR_2='ucur'; contour_levels_2=np.array([-0.04,-0.01,-0.001,0.001,0.01,0.04])
MODES_FILENAME_2='pmodes_normalised_5m_all_2003-to-2020_ss_lat_-1.5_1.5.nc'; PROJECTIONS_FILENAME_2='ucur_all_rac_b20_200_n241_rmm008FS-all3_lag_ss_lat_-1.5_1.5_projected_onto_pmodes_normalised_5m_all_2003-to-2020_ss_lat_-1.5_1.5.nc'; 



MODES_TO_PLOT=[3,10]


LAGGED_MEAN_DAYS=0 # Lag of lagged_means to be plotted




















LONG_BEG=30; LONG_END=390


LAT_VALUE=0







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


COLORBAR_HEIGHT=0.035
COLORBAR_VERTICAL_SHIFT=-0.25 # Move colour bar up and down
    





DRAW_GRIDLINES=False # Set to True to add overlay gridlines
GRIDLINE_WIDTH=0.5





###########################
###########################
###########################
###########################


###################
## Functions
###################



# For turning the np arrays into cubes
def f_mode_cube_packager(data_array,var_name):
    data_cube=iris.cube.Cube(data_array)
    # Add axes
    if data_array.ndim==3: # data reconstructed anomalies has shape (time,level,log)
        data_cube.add_dim_coord(projections_cube.coord('time'),0)
        data_cube.add_dim_coord(modes_cube.coord('level'),1)
        data_cube.add_dim_coord(projections_cube.coord('longitude'),2)
    else:
        raise Exception("Something fishy is happening, there should only 3 dimensions to output data (time,level,longitude).")
    # Apply the mask to the data
    data_cube=iris.util.mask_cube(data_cube,broadcast_mask)
    data_cube.var_name=var_name
    #fileout=file1.replace('nsquared',var_name)
    #print(var_name, ':', fileout)
    #iris.save(data_cube,fileout)
    return data_cube



##########################################
##########################################



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
###############################  Load the data and package it up ready for the plotting, 


### Load the data, making a list of the cubes





## First for VAR_1

list_of_cubes_1=[]


# Load modes data
mode_filepath=os.path.join(DATADIR,MODES_FILENAME_1)
print('mode_filepath: {0!s}'.format(mode_filepath))
cubelist=iris.load(mode_filepath)   # Loads in a Cubelist of cubes
modes_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist


# Load projections data
projections_filepath=os.path.join(DATADIR,PROJECTIONS_FILENAME_1)
print('projections_filepath: {0!s}'.format(projections_filepath))
cubelist=iris.load(projections_filepath)   # Loads in a Cubelist of cubes
projections_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist



for nmodes in MODES_TO_PLOT:
    #
    reconstruction=np.einsum('ijk,ilk->jlk', projections_cube.data[0:nmodes],modes_cube.data[0:nmodes])
    the_mask=modes_cube.data.mask[0,:,:]
    ntimes=len(projections_cube.coord('time').points)
    broadcast_mask=np.repeat(the_mask[np.newaxis,:,:],ntimes,0)
    reconstruction_cube=f_mode_cube_packager(reconstruction,'reconstructed_var')
    tcoord=reconstruction_cube.coord('time')
    tn=tcoord.units.num2date(tcoord.points[tcoord.points==LAGGED_MEAN_DAYS*24.0])
    timecon=iris.Constraint(time=tn)
    with warnings.catch_warnings(): # Iris will print a deprecation warning every time otherwise
        warnings.simplefilter("ignore")
        with iris.FUTURE.context(cell_datetime_objects=True):
            plot_cube=reconstruction_cube.extract(timecon) # Extract data with correct lag
    #
    plot_cube=MFF.MFF_Cube_Circular_Spatial_Subset(plot_cube, longitude_range=[LONG_BEG,LONG_END])
    list_of_cubes_1.append(plot_cube)
    












list_of_cubes_2=[]


# Load modes data
mode_filepath=os.path.join(DATADIR,MODES_FILENAME_2)
print('mode_filepath: {0!s}'.format(mode_filepath))
cubelist=iris.load(mode_filepath)   # Loads in a Cubelist of cubes
modes_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist


# Load projections data
projections_filepath=os.path.join(DATADIR,PROJECTIONS_FILENAME_2)
print('projections_filepath: {0!s}'.format(projections_filepath))
cubelist=iris.load(projections_filepath)   # Loads in a Cubelist of cubes
projections_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist



for nmodes in MODES_TO_PLOT:
    #
    reconstruction=np.einsum('ijk,ilk->jlk', projections_cube.data[0:nmodes],modes_cube.data[0:nmodes])
    the_mask=modes_cube.data.mask[0,:,:]
    ntimes=len(projections_cube.coord('time').points)
    broadcast_mask=np.repeat(the_mask[np.newaxis,:,:],ntimes,0)
    reconstruction_cube=f_mode_cube_packager(reconstruction,'reconstructed_var')
    tcoord=reconstruction_cube.coord('time')
    tn=tcoord.units.num2date(tcoord.points[tcoord.points==LAGGED_MEAN_DAYS*24.0])
    timecon=iris.Constraint(time=tn)
    with warnings.catch_warnings(): # Iris will print a deprecation warning every time otherwise
        warnings.simplefilter("ignore")
        with iris.FUTURE.context(cell_datetime_objects=True):
            plot_cube=reconstruction_cube.extract(timecon) # Extract data with correct lag
    #
    plot_cube=MFF.MFF_Cube_Circular_Spatial_Subset(plot_cube, longitude_range=[LONG_BEG,LONG_END])
    list_of_cubes_2.append(plot_cube) 








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

number_of_rows=len(MODES_TO_PLOT)
number_of_columns=2




figure_width_in_mm=(TEX_FIGURE_WIDTH_IN_PTS/72.27)*25.4
left_padding=1.5*figure_width_in_mm/10
right_padding=figure_width_in_mm/20
top_padding=right_padding*1.
bottom_padding=right_padding*4.5
horizontal_sep=right_padding/1.3
vertical_sep=8







locat=FigureSizeLocator(rows=number_of_rows, columns=number_of_columns, figwidth=figure_width_in_mm, panelratio=panel_ratio, hsep=horizontal_sep, vsep=vertical_sep, padleft=left_padding, padright=right_padding, padtop=top_padding, padbottom=bottom_padding, units='mm')


fig=plt.figure(figsize=locat.figsize)



letters=['a','b','c','d','e','f','g','h','i','j','k','l', 'm','n','o','p','q','r','s','t','u','v','w','x','y','z']








#
###
###############################
############################### Plot the lagged mean contour panels

centre_longitude=((LONG_BEG+LONG_END)/2)
axes_projection=None





## Loop over first column and plot


COLOURS=MFF.MFF_Get_Diverging_Colours(VAR_1,contour_levels_1)



icol=0
for ipanel, cube, panel_letter in zip(range(number_of_rows), list_of_cubes_1, letters[:number_of_rows]):
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
    if DRAW_GRIDLINES:
        panel.grid(which='both', color='k', linewidth=GRIDLINE_WIDTH)
    #
    panel_label_string = "(" + panel_letter + ") "
    panel.set_title(panel_label_string,loc='left',fontsize=PANEL_LABEL_FONT_SIZE)













## Loop over second column and plot


COLOURS=MFF.MFF_Get_Diverging_Colours(VAR_2,contour_levels_2)

icol=1
for ipanel, cube, panel_letter in zip(range(number_of_rows), list_of_cubes_2, letters[number_of_rows:2*number_of_rows]):
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
    if DRAW_GRIDLINES:
        panel.grid(which='both', color='k', linewidth=GRIDLINE_WIDTH)
    #
    panel_label_string = "(" + panel_letter + ") "
    panel.set_title(panel_label_string,loc='left',fontsize=PANEL_LABEL_FONT_SIZE)









 
  
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
IMAGEFILE=os.path.join(PLOTDIR,'reconstruct_longitude_anomalies_from_modes.png')

if SAVE_HIGH_RES_BOOL:
    plt.savefig(IMAGEFILE,dpi=300)
else:
    plt.savefig(IMAGEFILE)
    
print('Figure saved to: '+IMAGEFILE)






