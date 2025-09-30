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
#PLOTDIR=os.path.join(os.path.sep,'gpfs','home','rgq13jzu','MJO_scripts','Plotting_Scripts','Paper_Figures','tmp')

# Uni - local
#DATADIR=os.path.join(os.path.sep,'home','stusci1','rgq13jzu','Documents','MJO_WORK','data','glorys12v1eq1erai_zlev_d','processed'); PLOTDIR=os.path.join(os.path.sep,'home','stusci1','rgq13jzu','Documents','MJO_WORK','MJO_scripts','Plotting_Scripts','tmp')

###########
#
# Choose what data to plot



VAR='swpd'; contour_levels=np.array([-0.04,-0.01,-0.005,-0.001,0.001,0.005,0.01,0.04])


SWPD_ANOMALIES_FILENAME='swpd_all_rac_b20_200_n241_rmm008FS-all3_lag.nc'

SWPD_MODES_FILENAME='rmodes_normalised_5m_all_2003-to-2020_ss_lat_-1.5_1.5.nc'
SWPD_PROJECTION_COEFFICIENTS_FILENAME='swpd_all_rac_b20_200_n241_rmm008FS-all3_lag_ss_lat_-1.5_1.5_projected_onto_rmodes_normalised_5m_all_2003-to-2020_ss_lat_-1.5_1.5.nc'
CE_FILENAME='ce_5m_all_2003-to-2020_ss_lat_-1.5_1.5.nc'










LAGGED_MEAN_DAYS=0 # Lag of lagged_means to be plotted

NUMBER_OF_MODES=3



LAT_BEG=-10; LAT_END=10

PLOT_LONGITUDE=150








############
# Plotting options

SAVE_HIGH_RES_BOOL=True

NUMBER_OF_COLUMNS=2

LONG_MAJOR_TICK_STEP=30; LONG_MINOR_TICK_STEP=10


TEX_FIGURE_WIDTH_IN_PTS=397.48499



########################
# y axis options





MAXIMUM_DEPTH=2000

SPLIT_DEPTH_SCALES_1_BOOL=True
SPLIT_DEPTH_SCALES_1_DEPTH=50
SPLIT_DEPTH_SCALES_1_YSCALING_FACTOR=2 # Factor of compression of y axis

SPLIT_DEPTH_SCALES_2_BOOL=True
SPLIT_DEPTH_SCALES_2_DEPTH=200
SPLIT_DEPTH_SCALES_2_YSCALING_FACTOR=17.5 # Factor of compression of y axis



y_ticks_major=[0, 25, 50, 100, 150, 200, 1000,2000]






#########




X_AXIS_LABEL_FONT_SIZE=10
Y_AXIS_LABEL_FONT_SIZE=10

X_AXIS_TICK_ROTATION=90
Y_AXIS_TICK_ROTATION=0

PANEL_LABEL_FONT_SIZE=9
# only if labels put inside figures
#PANEL_LABEL_X_POSITION=0.90 #  In figure units
#PANEL_LABEL_Y_POSITION=0.10 #  In figure units


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


COLORBAR_HEIGHT=0.040
COLORBAR_VERTICAL_SHIFT=-0.16 # Move colour bar up and down
    





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


###  Check that the code will behave given the choice of latitudes

if LAT_BEG > LAT_END:
    raise Exception("Ensure LAT_BEG is less than LAT_END")
elif abs(LAT_END)> 15 or abs(LAT_BEG) > 15:
    raise Exception("Ensure that (absolute) LAT_BEG and LAT_END do not exceed 15 degrees")

if (not(type(NUMBER_OF_MODES)==int)) or (NUMBER_OF_MODES <= 0) :
    raise Exception("NUMBER_OF_MODES must be a positive integer.")


###############################
###############################    
### 
# 









#
###
###############################
############################### Make ticks


# x ticks
x_ticks_major = [int(i) for i in np.linspace(LAT_BEG, LAT_END, 21)]
x_ticks_labels_major=MFF.Make_Tick_Labels(x_ticks_major,'latitude',False)

# y ticks
y_ticks_labels_major=MFF.Make_Tick_Labels(y_ticks_major,"depth")

###############################
###############################    
### 
# 









#
###
###############################
###############################  Load the data 

# Panel 1
anomalies_cube = MFF.MFF_Quick_Cube_Load( DATADIR, SWPD_ANOMALIES_FILENAME)

# Panel 2
ce_cube = MFF.MFF_Quick_Cube_Load( DATADIR, CE_FILENAME)
modes_cube = MFF.MFF_Quick_Cube_Load( DATADIR, SWPD_MODES_FILENAME)
projections_cube = MFF.MFF_Quick_Cube_Load( DATADIR, SWPD_PROJECTION_COEFFICIENTS_FILENAME)




# Extract only required data

long_con=anomalies_cube.coord('longitude')[anomalies_cube.coord('longitude').nearest_neighbour_index(PLOT_LONGITUDE)].cell(0)[0]
print("")
print("The closest longitude value to PLOT_LONGITUDE is:", long_con)
print("")
long_con=iris.Constraint(longitude = long_con)
mode_con=iris.Constraint( mode_number = lambda cell: cell <= NUMBER_OF_MODES)


anomalies_cube = anomalies_cube.extract(long_con)
anomalies_cube = MFF.MFF_Cube_Extract_Lagged_Mean_Days_Data(anomalies_cube,LAGGED_MEAN_DAYS)

projections_cube = projections_cube.extract( mode_con & long_con )
projections_cube = MFF.MFF_Cube_Extract_Lagged_Mean_Days_Data(projections_cube,LAGGED_MEAN_DAYS)

ce_cube = ce_cube.extract( mode_con & long_con )

modes_cube = modes_cube.extract( mode_con & long_con )



###############################
###############################    
### 
# 

#----------------------------------

#
###
###############################
###############################  Convert data to form required for panel 2

equatorial_beta=2*(7.292E-5)/6371000 # 2 * \Omega / R_Earth

latitudes=anomalies_cube.coord('latitude').points
depths=modes_cube.coord('level').points

N_levels=len(depths)
N_latitudes=len(latitudes)

latitudes_in_metres=latitudes*110000
reconstruction=np.zeros([N_levels,N_latitudes])




# loop over modes, calculate contribution and add to total
# If only one mode handle separately as zip doesn't work 
if NUMBER_OF_MODES == 1:
    ce, z_structure, amplitude = ce_cube.data, modes_cube.data, projections_cube.data
    # Calculate z structure and broadcast to size of reconstruction (nlevels, nlatitudes)
    z_structure = np.repeat(z_structure[:,np.newaxis], N_latitudes, axis=1) # broadcast to (nlevels, nlatitudes)
    # Calculate y structure and broadcast to size of reconstruction (nlevels, nlatitudes)
    y0 = np.sqrt(2*ce/equatorial_beta)
    y_structure = np.exp(-(latitudes_in_metres/y0)**2)
    y_structure = np.repeat(y_structure[np.newaxis,:], N_levels, axis=0)# broadcast to (nlevels, nlatitudes)
    # add contribution to total structure
    reconstruction += amplitude * y_structure * z_structure
else:
    for ce, z_structure, amplitude in zip(ce_cube.data, modes_cube.data, projections_cube.data):
        # Calculate z structure and broadcast to size of reconstruction (nlevels, nlatitudes)
        z_structure = np.repeat(z_structure[:,np.newaxis], N_latitudes, axis=1) # broadcast to (nlevels, nlatitudes)
        # Calculate y structure and broadcast to size of reconstruction (nlevels, nlatitudes)
        y0 = np.sqrt(2*ce/equatorial_beta)
        y_structure = np.exp(-(latitudes_in_metres/y0)**2)
        y_structure = np.repeat(y_structure[np.newaxis,:], N_levels, axis=0)# broadcast to (nlevels, nlatitudes)
        # add contribution to total structure
        reconstruction += amplitude * y_structure * z_structure
        print("Phase speed: ", ce, ". Trapping scale: ", y0)
        






###############################
###############################    
### 
# 

#-----------------------------------------

#
###
###############################
###############################  Make the major depth ticks and split y axis











[forward_depth_fun , inverse_depth_fun]=MFF.Assign_Piecewise_Linear_Yaxis_Scaling_Functions(SPLIT_DEPTH_SCALES_1_BOOL, SPLIT_DEPTH_SCALES_1_DEPTH, SPLIT_DEPTH_SCALES_1_YSCALING_FACTOR,SPLIT_DEPTH_SCALES_2_BOOL,SPLIT_DEPTH_SCALES_2_DEPTH, SPLIT_DEPTH_SCALES_2_YSCALING_FACTOR)










###############################
###############################    
### 
# 




## Set up the figure and panel locations

panel_ratio=3.2

number_of_rows=2
number_of_columns=1




figure_width_in_mm=(TEX_FIGURE_WIDTH_IN_PTS/72.27)*25.4
left_padding=1.5*figure_width_in_mm/10
right_padding=figure_width_in_mm/25
top_padding=8
bottom_padding=32
horizontal_sep=right_padding/1.3
vertical_sep=8







locat=FigureSizeLocator(rows=number_of_rows, columns=number_of_columns, figwidth=figure_width_in_mm, panelratio=panel_ratio, hsep=horizontal_sep, vsep=vertical_sep, padleft=left_padding, padright=right_padding, padtop=top_padding, padbottom=bottom_padding, units='mm')


fig=plt.figure(figsize=locat.figsize)












#
###
###############################
############################### Plot the lagged mean contour panels


axes_projection=None



letters=['a','b','c','d','e','f','g','h','i','j','k','l', 'm','n','o','p','q','r','s','t','u','v','w','x','y','z']








COLOURS=MFF.MFF_Get_Diverging_Colours(VAR,contour_levels)



# Plot the first panel
irow=0; icol=0;
pos=locat.panel_position(irow,icol)
panel=fig.add_axes(pos)
plt.axes(panel)
plt.gca().patch.set_color('.3') # Dark grey
plt.gca().patch.set_edgecolor('k')
plt.gca().patch.set_hatch('++') 
#
panel_with_plot=iplt.contourf(anomalies_cube, levels=contour_levels, coords=['latitude','level'], extend='both',colors=COLOURS)
#
plt.gca().set_yscale('function', functions=(forward_depth_fun,inverse_depth_fun))
if SPLIT_DEPTH_SCALES_1_BOOL==True:
    plt.hlines(SPLIT_DEPTH_SCALES_1_DEPTH,LAT_BEG,LAT_END,colors='k')
if SPLIT_DEPTH_SCALES_2_BOOL==True:
    plt.hlines(SPLIT_DEPTH_SCALES_2_DEPTH,LAT_BEG,LAT_END,colors='k')
#    
plt.xlim(LAT_BEG,LAT_END)
#
panel.set_xticks(x_ticks_major, minor=False) # Set major x-ticks positions
#panel.set_xticks(x_ticks_minor, minor=True) # Set minor x-ticks positions
if (irow==number_of_rows-1) or not SHARE_X_TICKS_BOOL:
    panel.set_xticklabels(x_ticks_labels_major, minor=False) # Set major x-ticks labels
else:
    panel.set_xticklabels([],minor=False)
#
panel.set_yticks(y_ticks_major,  minor=False) # Set major y-ticks positions
panel.set_yticklabels(y_ticks_labels_major, minor=False) # Set major y-ticks labels
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
panel_label_string = "(a)"
panel.set_title(panel_label_string, loc='left', fontsize=PANEL_LABEL_FONT_SIZE)
#panel.text(PANEL_LABEL_X_POSITION, PANEL_LABEL_Y_POSITION,panel_label_string,transform=panel.transAxes,bbox=dict(boxstyle='square,pad=0.2',facecolor='white', alpha=1),fontsize=PANEL_LABEL_FONT_SIZE)
#
if DRAW_GRIDLINES:
    panel.grid(which='both', color='k', linewidth=GRIDLINE_WIDTH)



# Plot the second panel
irow=1; icol=0;
pos=locat.panel_position(irow,icol)
panel=fig.add_axes(pos)
plt.axes(panel)
plt.gca().patch.set_color('.3') # Dark grey
plt.gca().patch.set_edgecolor('k')
plt.gca().patch.set_hatch('++') 
#
panel_with_plot=plt.contourf(latitudes, depths, reconstruction, levels=contour_levels,  extend='both',colors=COLOURS)
#
plt.gca().set_yscale('function', functions=(forward_depth_fun,inverse_depth_fun))
if SPLIT_DEPTH_SCALES_1_BOOL==True:
    plt.hlines(SPLIT_DEPTH_SCALES_1_DEPTH,LAT_BEG,LAT_END,colors='k')
if SPLIT_DEPTH_SCALES_2_BOOL==True:
    plt.hlines(SPLIT_DEPTH_SCALES_2_DEPTH,LAT_BEG,LAT_END,colors='k')
#    
plt.xlim(LAT_BEG,LAT_END)
#
panel.set_xticks(x_ticks_major, minor=False) # Set major x-ticks positions
#panel.set_xticks(x_ticks_minor, minor=True) # Set minor x-ticks positions
if (irow==number_of_rows-1) or not SHARE_X_TICKS_BOOL:
    panel.set_xticklabels(x_ticks_labels_major, minor=False) # Set major x-ticks labels
else:
    panel.set_xticklabels([],minor=False)
#
panel.set_yticks(y_ticks_major,  minor=False) # Set major y-ticks positions
panel.set_yticklabels(y_ticks_labels_major, minor=False) # Set major y-ticks labels
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
panel_label_string = "(b)"
panel.set_title(panel_label_string, loc='left', fontsize=PANEL_LABEL_FONT_SIZE)
#panel.text(PANEL_LABEL_X_POSITION, PANEL_LABEL_Y_POSITION,panel_label_string,transform=panel.transAxes,bbox=dict(boxstyle='square,pad=0.2',facecolor='white', alpha=1),fontsize=PANEL_LABEL_FONT_SIZE)
#
if DRAW_GRIDLINES:
    panel.grid(which='both', color='k', linewidth=GRIDLINE_WIDTH)






















 
  
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

color_bar_label=cbar_label_assigner(VAR)



#
## Put the color bar under final panels 
# 


[lowest_panel_left, lowest_panel_bottom, lowest_panel_width, lowest_panel_height]=locat.panel_position( number_of_rows-1 , 0) 
lowest_panel_right= lowest_panel_left + lowest_panel_width


middle=0.5*(lowest_panel_right+lowest_panel_left)
width=COLORBAR_WIDTH_MULTIPLIER*(lowest_panel_right-lowest_panel_left)
bottom=lowest_panel_bottom+COLORBAR_VERTICAL_SHIFT
left=middle-0.5*width


color_bar_ax=fig.add_axes([left,bottom,width,COLORBAR_HEIGHT])
fig.colorbar(panel_with_plot, cax=color_bar_ax, orientation='horizontal', label=color_bar_label)
fig.colorbar(panel_with_plot, cax=color_bar_ax, orientation='horizontal')
color_bar_ax.set_title(color_bar_label, fontsize=COLORBAR_TITLE_FONT_SIZE)
color_bar_ax.tick_params(labelsize=COLORBAR_TICK_FONT_SIZE, rotation=COLORBAR_TICK_LABEL_ROTATION)














#
## Put the y axis label on

# Calculate positions
[highest_panel_left,highest_panel_bottom,highest_panel_width,highest_panel_height]=locat.panel_position(0, 0) 
all_panel_height=highest_panel_bottom + highest_panel_height - lowest_panel_bottom
# Add the labels and hide the axes edges tick marks
#shared_ylabel_ax=fig.add_axes([0.4*lowest_panel_left, lowest_panel_bottom, lowest_panel_left/4, all_panel_height] )
shared_ylabel_ax=fig.add_axes([0.3*lowest_panel_left, lowest_panel_bottom, lowest_panel_left/10, all_panel_height] )
shared_ylabel_ax.set_ylabel('Depth (m)',fontsize=Y_AXIS_LABEL_FONT_SIZE)
shared_ylabel_ax.set_xticks([])
shared_ylabel_ax.set_yticks([])
shared_ylabel_ax.set_frame_on(False)







#############################
#############################
#


########### Save the figure
IMAGEFILE=os.path.join(PLOTDIR,'reconstruct_latitude_anomalies_from_modes.png')

if SAVE_HIGH_RES_BOOL:
    plt.savefig(IMAGEFILE,dpi=300)
else:
    plt.savefig(IMAGEFILE)
    
print('Figure saved to: '+IMAGEFILE)






