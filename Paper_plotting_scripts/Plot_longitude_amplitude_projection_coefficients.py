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


PROJECTIONS_FILENAME_1='swpd_all_rac_b20_200_n241_rmm008FS-all{PHASE_NUMBER}_lag_ss_lat_-1.5_1.5_projected_onto_rmodes_normalised_5m_all_2003-to-2020_ss_lat_-1.5_1.5.nc'; YLIMS_1=[-2,2]; 
#Y_AXIS_1_LABEL=r'Potential density (kg m$^{-3}$)'
Y_AXIS_1_LABEL=r'Density coefficient (kg m$^{-3}$ s)'
Y_AXIS_1_MINOR_TICKS=np.linspace(-2,2,5)


PROJECTIONS_FILENAME_2='ucur_all_rac_b20_200_n241_rmm008FS-all{PHASE_NUMBER}_lag_ss_lat_-1.5_1.5_projected_onto_pmodes_normalised_5m_all_2003-to-2020_ss_lat_-1.5_1.5.nc'; YLIMS_2=[-0.02,0.02]
#Y_AXIS_2_LABEL=r'Velocity (m s$^{-1}$)'
Y_AXIS_2_LABEL=r'Velocity coefficient (m s$^{-1}$)'
Y_AXIS_2_MINOR_TICKS=np.linspace(-0.02,0.02,5)



PLOT_N_MODES=[1,2,3] # list of the mode numbers to be plotted

PHASE_NUMBERS_TO_PLOT=[3,5]

LAGGED_MEAN_DAYS=0 # Lag of lagged_means to be plotted







#LONG_BEG=-180; LONG_END=180 # Longitude plotting range (Default to -180:180, global)
#LONG_BEG=40; LONG_END=280 # Matches Patama's plots
LONG_BEG=30; LONG_END=390









############
# Plotting options

SAVE_HIGH_RES_BOOL=True

NUMBER_OF_COLUMNS=2

LONG_MAJOR_TICK_STEP=30; LONG_MINOR_TICK_STEP=10


TEX_FIGURE_WIDTH_IN_PTS=397.48499



Y_AXIS_1_LABEL_HORIZONTAL_OFFSET=0.02 # Use to shift first axis label left and right (to uncouple spacing from the extra d.p. on second axis)

Y_AXIS_1_LABEL_VERTICAL_OFFSET=-0.08 # Use to shift y axis labels up and down
Y_AXIS_2_LABEL_VERTICAL_OFFSET=Y_AXIS_1_LABEL_VERTICAL_OFFSET




#########


LEGEND_FONT_SIZE=9

X_AXIS_LABEL_FONT_SIZE=10
Y_AXIS_LABEL_FONT_SIZE=10

X_AXIS_TICK_ROTATION=90
Y_AXIS_TICK_ROTATION=0

PANEL_LABEL_FONT_SIZE=9

PHASE_LABEL_FONT_SIZE=8

X_TICK_FONT_SIZE=7
Y_TICK_FONT_SIZE=7

MAJOR_TICK_LENGTH=6
MAJOR_TICK_WIDTH=1.3
MINOR_TICK_LENGTH=3
MINOR_TICK_WIDTH=1.

SHARE_X_TICKS_BOOL=True # If true only the lowest row will have the xticks labelled, otherwise all labelled individually.







DRAW_GRIDLINES=True # Set to True to add overlay gridlines
GRIDLINE_WIDTH=0.5





###########################
###########################
###########################
###########################





#
###
###############################
###############################  Run some initial checks on the settings so that if it's definitely going to break you don't wait as long to find out. 







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


for PHASE_NUMBER in PHASE_NUMBERS_TO_PLOT:
    projections_filename=PROJECTIONS_FILENAME_1.replace("{PHASE_NUMBER}",str(PHASE_NUMBER))
    projections_filepath=os.path.join(DATADIR,projections_filename)
    print('projections_filepath: {0!s}'.format(projections_filepath))
    cubelist=iris.load(projections_filepath)   # Loads in a Cubelist of cubes
    projections_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist
    # Extract data for correct lagged mean
    projections_cube=MFF.MFF_Cube_Extract_Lagged_Mean_Days_Data(projections_cube,LAGGED_MEAN_DAYS)
    # Extract data for correct mode_numbers
    mode_con=iris.Constraint(mode_number=lambda cell: cell in PLOT_N_MODES)
    projections_cube=projections_cube.extract(mode_con)
    projections_cube=MFF.MFF_Cube_Circular_Spatial_Subset(projections_cube, longitude_range=[LONG_BEG,LONG_END])
    list_of_cubes_1.append(projections_cube)
  



## Then for VAR_2

list_of_cubes_2=[]


for PHASE_NUMBER in PHASE_NUMBERS_TO_PLOT:
    projections_filename=PROJECTIONS_FILENAME_2.replace("{PHASE_NUMBER}",str(PHASE_NUMBER))
    projections_filepath=os.path.join(DATADIR,projections_filename)
    print('projections_filepath: {0!s}'.format(projections_filepath))
    cubelist=iris.load(projections_filepath)   # Loads in a Cubelist of cubes
    projections_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist
    # Extract data for correct lagged mean
    projections_cube=MFF.MFF_Cube_Extract_Lagged_Mean_Days_Data(projections_cube,LAGGED_MEAN_DAYS)
    # Extract data for correct mode_numbers
    mode_con=iris.Constraint(mode_number=lambda cell: cell in PLOT_N_MODES)
    projections_cube=projections_cube.extract(mode_con)
    projections_cube=MFF.MFF_Cube_Circular_Spatial_Subset(projections_cube, longitude_range=[LONG_BEG,LONG_END])
    list_of_cubes_2.append(projections_cube)











###############################
###############################    
### 
# 




## Set up the figure and panel locations

panel_ratio=3.2

number_of_rows=len(PHASE_NUMBERS_TO_PLOT)
number_of_columns=2




figure_width_in_mm=(TEX_FIGURE_WIDTH_IN_PTS/72.27)*25.4
left_padding=1.5*figure_width_in_mm/13
right_padding=figure_width_in_mm/20
top_padding=right_padding*1.2
bottom_padding=right_padding*3
horizontal_sep=1.3*left_padding
vertical_sep=8







locat=FigureSizeLocator(rows=number_of_rows, columns=number_of_columns, figwidth=figure_width_in_mm, panelratio=panel_ratio, hsep=horizontal_sep, vsep=vertical_sep, padleft=left_padding, padright=right_padding, padtop=top_padding, padbottom=bottom_padding, units='mm')


fig=plt.figure(figsize=locat.figsize)












#
###
###############################
############################### Plot the lagged mean contour panels

centre_longitude=((LONG_BEG+LONG_END)/2)
axes_projection=None



letters=['a','b','c','d','e','f','g','h','i','j','k','l', 'm','n','o','p','q','r','s','t','u','v','w','x','y','z']


## Loop over first column and plot



icol=0
for ipanel, cube, panel_letter in zip(range(number_of_rows), list_of_cubes_1, letters[:number_of_rows]):
    irow=ipanel
    pos=locat.panel_position(irow,icol)
    panel=fig.add_axes(pos)

    plt.axes(panel)
    for mode_slice in cube.slices('longitude'):
        plot_mode_number=mode_slice.coord('mode_number').points[0]
        plot_mode_label="Mode "+ str(plot_mode_number)
        iplt.plot(mode_slice, label=plot_mode_label)
    #    
    plt.hlines(0, LONG_BEG, LONG_END, colors='black', linestyles='dashed')
    plt.xlim(LONG_BEG,LONG_END)
    plt.ylim(YLIMS_1)
    #
    panel.set_xticks(long_ticks_major, minor=False) # Set major x-ticks positions
    panel.set_xticks(long_ticks_minor, minor=True) # Set minor x-ticks positions
    if (irow==number_of_rows-1) or not SHARE_X_TICKS_BOOL:
        panel.set_xticklabels(long_ticks_labels_major, minor=False) # Set major x-ticks labels
    else:
        panel.set_xticklabels([],minor=False)
    #
    #panel.set_yticks(depth_ticks_major,  minor=False) # Set major y-ticks positions
    #panel.set_yticklabels(depth_ticks_labels_major, minor=False) # Set major y-ticks labels
    panel.set_yticks(Y_AXIS_1_MINOR_TICKS, minor=True) # Set minor y-ticks positions
    #
    #
    panel.tick_params(which='major',axis='both',direction='out',length=MAJOR_TICK_LENGTH, width=MAJOR_TICK_WIDTH)
    panel.tick_params(which='minor',axis='both',direction='out',length=MINOR_TICK_LENGTH, width=MINOR_TICK_WIDTH)
    #
    panel.tick_params(axis='x', rotation=X_AXIS_TICK_ROTATION, labelsize=X_TICK_FONT_SIZE)
    panel.tick_params(axis='y', rotation=Y_AXIS_TICK_ROTATION, labelsize=Y_TICK_FONT_SIZE)
    #
    #
    if DRAW_GRIDLINES:
        panel.grid(which='major', axis='x', color='gray', linewidth=GRIDLINE_WIDTH)
        panel.grid(which='minor', axis='y', color='gray', linewidth=GRIDLINE_WIDTH)
    #
    panel_label_string = "(" + panel_letter + ") "
    panel.set_title(panel_label_string,loc='left',fontsize=PANEL_LABEL_FONT_SIZE)
    #
    # Add phase label in top right of panel
    phase_label_string='Phase ' + str(PHASE_NUMBERS_TO_PLOT[ipanel])
    panel.text(0.99, 0.97, phase_label_string, transform=panel.transAxes, horizontalalignment='right', verticalalignment='top', alpha=1, fontsize=PHASE_LABEL_FONT_SIZE, bbox=dict(boxstyle='square, pad=0.1', facecolor='white', alpha=1, linewidth=0))











## Loop over second column and plot


icol=1
for ipanel, cube, panel_letter in zip(range(number_of_rows), list_of_cubes_2, letters[number_of_rows:2*number_of_rows]):
    irow=ipanel
    pos=locat.panel_position(irow,icol)
    panel=fig.add_axes(pos)

    plt.axes(panel)
    for mode_slice in cube.slices('longitude'):
        plot_mode_number=mode_slice.coord('mode_number').points[0]
        plot_mode_label="Mode "+ str(plot_mode_number)
        iplt.plot(mode_slice, label=plot_mode_label)
    #    
    plt.hlines(0, LONG_BEG, LONG_END, colors='black', linestyles='dashed')
    plt.xlim(LONG_BEG,LONG_END)
    plt.ylim(YLIMS_2)
    #
    panel.set_xticks(long_ticks_major, minor=False) # Set major x-ticks positions
    panel.set_xticks(long_ticks_minor, minor=True) # Set minor x-ticks positions
    if (irow==number_of_rows-1) or not SHARE_X_TICKS_BOOL:
        panel.set_xticklabels(long_ticks_labels_major, minor=False) # Set major x-ticks labels
    else:
        panel.set_xticklabels([],minor=False)
    ####### you were here ####
    #
    #panel.set_yticks(depth_ticks_major,  minor=False) # Set major y-ticks positions
    #panel.set_yticklabels(depth_ticks_labels_major, minor=False) # Set major y-ticks labels
    panel.set_yticks(Y_AXIS_2_MINOR_TICKS, minor=True) # Set minor y-ticks positions
    #
    #
    panel.tick_params(which='major',axis='both',direction='out',length=MAJOR_TICK_LENGTH, width=MAJOR_TICK_WIDTH)
    panel.tick_params(which='minor',axis='both',direction='out',length=MINOR_TICK_LENGTH, width=MINOR_TICK_WIDTH)
    #
    panel.tick_params(axis='x', rotation=X_AXIS_TICK_ROTATION, labelsize=X_TICK_FONT_SIZE)
    panel.tick_params(axis='y', rotation=Y_AXIS_TICK_ROTATION, labelsize=Y_TICK_FONT_SIZE)
    #
    #
    if DRAW_GRIDLINES:
        panel.grid(which='major', axis='x', color='gray', linewidth=GRIDLINE_WIDTH)
        panel.grid(which='minor', axis='y', color='gray', linewidth=GRIDLINE_WIDTH)
    panel_label_string = "(" + panel_letter + ") "
    panel.set_title(panel_label_string,loc='left',fontsize=PANEL_LABEL_FONT_SIZE)
    #
    # Add phase label in top right of panel
    phase_label_string='Phase ' + str(PHASE_NUMBERS_TO_PLOT[ipanel])
    panel.text(0.99, 0.97, phase_label_string, transform=panel.transAxes, horizontalalignment='right', verticalalignment='top', alpha=1, fontsize=PHASE_LABEL_FONT_SIZE, bbox=dict(boxstyle='square, pad=0.1', facecolor='white', alpha=1, linewidth=0))










 
  
#
###############################
############################### Add the colourbars 













#
## Put the y axis labels on

# first axis


# Calculate positions
[highest__left_panel_left,highest_left_panel_bottom,highest_left_panel_width,highest_left_panel_height]=locat.panel_position(0, 0) 
[lowest_left_panel_left,lowest_left_panel_bottom,lowest_left_panel_width,lowest_left_panel_height]=locat.panel_position(number_of_rows-1, 0) 
all_panel_height=highest_left_panel_bottom + highest_left_panel_height - lowest_left_panel_bottom
# Add the labels and hide the axes edges tick marks
#
Y_axis_label_offset=0.6*lowest_left_panel_left
Y_axis_1_label_start=lowest_left_panel_left-Y_axis_label_offset+Y_AXIS_1_LABEL_HORIZONTAL_OFFSET
Y_axis_label_width=lowest_left_panel_left/4
#
shared_ylabel_ax=fig.add_axes([Y_axis_1_label_start, lowest_left_panel_bottom + Y_AXIS_1_LABEL_VERTICAL_OFFSET, Y_axis_label_width, all_panel_height] )
shared_ylabel_ax.set_ylabel(Y_AXIS_1_LABEL,fontsize=Y_AXIS_LABEL_FONT_SIZE)
shared_ylabel_ax.set_xticks([])
shared_ylabel_ax.set_yticks([])
shared_ylabel_ax.set_frame_on(False)
#shared_ylabel_ax.axis('off')




# second axis

# Calculate positions
[highest_right_panel_left,highest_right_panel_bottom,highest_right_panel_width,highest_right_panel_height]=locat.panel_position(0, 1) 
[lowest_right_panel_left,lowest_right_panel_bottom,lowest_right_panel_width,lowest_right_panel_height]=locat.panel_position(number_of_rows-1, 1) 
# Add the labels and hide the axes edges tick marks
#
Y_axis_2_label_start=lowest_right_panel_left-Y_axis_label_offset
#
shared_ylabel_ax=fig.add_axes([Y_axis_2_label_start, lowest_right_panel_bottom + Y_AXIS_2_LABEL_VERTICAL_OFFSET, Y_axis_label_width, all_panel_height] )
shared_ylabel_ax.set_ylabel(Y_AXIS_2_LABEL,fontsize=Y_AXIS_LABEL_FONT_SIZE)
shared_ylabel_ax.set_xticks([])
shared_ylabel_ax.set_yticks([])
shared_ylabel_ax.set_frame_on(False)
#shared_ylabel_ax.axis('off')




#############################
#############################
#





############# Add a shared legend below

fake_figure = plt.figure()
fake_ax=fake_figure.add_subplot(111)
for mode_i in PLOT_N_MODES:
    mode_label_string="Mode " + str(mode_i)
    fake_ax.plot([1,2,3],[1,2,3], label=mode_label_string)




total_panels_width=lowest_right_panel_left + lowest_right_panel_width - lowest_left_panel_left

legend_ax=fig.add_axes([lowest_left_panel_left, 0.05*lowest_left_panel_bottom, total_panels_width, 0.3*lowest_left_panel_bottom])
legend_ax.legend(*fake_ax.get_legend_handles_labels(), fontsize=LEGEND_FONT_SIZE, ncol=len(PLOT_N_MODES), loc='center', frameon=False)

legend_ax.axis("off")










########### Save the figure
IMAGEFILE=os.path.join(PLOTDIR,'longitude_amplitude_projection_coefficients.png')
#IMAGEFILE=os.path.join(PLOTDIR,'tmp.png')

if SAVE_HIGH_RES_BOOL:
    fig.savefig(IMAGEFILE,dpi=300)
else:
   fig.savefig(IMAGEFILE)
    
print('Figure saved to: '+IMAGEFILE)






