#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plots first 'NMODES' of density modes and then horizontal velocity modes side by side at two longitudes 
in order :

densitylong1, densitylong2, horizontallong1,horizontallong2


@author: rgq13jzu
"""



import os

import iris
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import pdb
import numpy as np

from panels import FigureSizeLocator
import functions_dynmodes as fdyn
import MyPaperFigureFunctions as MFF




BASEDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data','glorys12v1aeq1erai_zlev_d','processed')
#BASEDIR=os.path.join(os.path.sep,'gpfs','afm','matthews','robbins','data','glorys12v1aeq1erai_zlev_d','processed')



PLOTDIR=os.path.join(os.path.sep,'gpfs','home','rgq13jzu','MJO_scripts','Plotting_Scripts','Paper_Figures','Plotting_Scripts','Figures')


DENSITY_MODES_FILE='rmodes_normalised_5m_all_2003-to-2020_ss_lat_-1.5_1.5.nc'
HORIZONTAL_MODES_FILE='pmodes_normalised_5m_all_2003-to-2020_ss_lat_-1.5_1.5.nc'





#BATHYMETRY_FILENAME='deptho_ss_lat_-1.5_1.5.nc'
#NSQUARED_FILENAME='smoothed_nsquared_all_2003-to-2020_ss_lat_-1.5_1.5.nc' # Required for wmodes and rmodes



LONGITUDES=[150, 240]


NMODES=3
##















############## PLOTTING OPTIONS

SAVE_HIGH_RES_BOOL=True


TEX_FIGURE_WIDTH_IN_PTS=397.48499

X_AXIS_LABEL_FONT_SIZE=10
Y_AXIS_LABEL_FONT_SIZE=10

LEGEND_FONT_SIZE=9

PANEL_LABEL_FONT_SIZE=9

TICK_FONT_SIZE=8

MAJOR_TICK_LENGTH=6
MAJOR_TICK_WIDTH=1.3
MINOR_TICK_LENGTH=3
MINOR_TICK_WIDTH=1.

DRAW_GRIDLINES=True # Set to True to add overlay gridlines
GRIDLINE_WIDTH=0.3





DEGREE_SYMBOL_IN_LABELS_BOOL=False
#DEGREE_SYMBOL_IN_LABELS_BOOL=True





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




























# Load density modes
file1=os.path.join(BASEDIR,DENSITY_MODES_FILE)
print('file1: {0!s}'.format(file1))
cubelist=iris.load(file1)   # Loads in a Cubelist of cubes
density_modes_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist


# Load horizontal velocity modes
file2=os.path.join(BASEDIR,HORIZONTAL_MODES_FILE)
print('file1: {0!s}'.format(file2))
cubelist=iris.load(file2)   # Loads in a Cubelist of cubes
velocity_modes_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist



##### Extract data
actual_longitudes=[] # track closest longitudes to those requested


#density at long1
long_index=density_modes_cube.coord('longitude').nearest_neighbour_index(LONGITUDES[0])
long_value=density_modes_cube.coord('longitude')[long_index].cell(0)[0]
cubeConstraints=iris.Constraint(longitude=long_value)
density_modes_long1=density_modes_cube.extract(cubeConstraints)
actual_longitudes.append(long_value)

#density at long2
long_index=density_modes_cube.coord('longitude').nearest_neighbour_index(LONGITUDES[1])
long_value=density_modes_cube.coord('longitude')[long_index].cell(0)[0]
cubeConstraints=iris.Constraint(longitude=long_value)
density_modes_long2=density_modes_cube.extract(cubeConstraints)
actual_longitudes.append(long_value)

#velocity at long1
long_index=velocity_modes_cube.coord('longitude').nearest_neighbour_index(LONGITUDES[0])
long_value=velocity_modes_cube.coord('longitude')[long_index].cell(0)[0]
cubeConstraints=iris.Constraint(longitude=long_value)
velocity_modes_long1=velocity_modes_cube.extract(cubeConstraints)
actual_longitudes.append(long_value)

#velocity at long2
long_index=velocity_modes_cube.coord('longitude').nearest_neighbour_index(LONGITUDES[1])
long_value=velocity_modes_cube.coord('longitude')[long_index].cell(0)[0]
cubeConstraints=iris.Constraint(longitude=long_value)
velocity_modes_long2=velocity_modes_cube.extract(cubeConstraints)
actual_longitudes.append(long_value)


# Put extracted cubes into list
plot_data=[density_modes_long1, density_modes_long2, velocity_modes_long1, velocity_modes_long2]










xlimit_scaling=1.2

## Calculate good x-limits
density_max=xlimit_scaling*max(density_modes_long1.data.max(), density_modes_long2.data.max())
density_min=xlimit_scaling*min(density_modes_long1.data.min(), density_modes_long2.data.min())
velocity_max=xlimit_scaling*max(velocity_modes_long1.data.max(), velocity_modes_long2.data.max())
velocity_min=xlimit_scaling*min(velocity_modes_long1.data.min(), velocity_modes_long2.data.min())


## Even x limits
density_max=np.max([abs(density_min),abs(density_max)]); velocity_max=np.max([abs(velocity_min),abs(velocity_max)]); xlimits_list=[ [-density_max, density_max], [-density_max, density_max], [-velocity_max, velocity_max], [-velocity_max, velocity_max] ]

## Uneven xlimits
#xlimits_list=[ [density_min, density_max], [density_min, density_max], [velocity_min, velocity_max], [velocity_min, velocity_max] ]






# Account for stupid floating point junk in labels
DECIMAL_PLACES=1
modulo_longitudes=[longitude%360 for longitude in actual_longitudes]



modulo_longitudes=[longitude -360 if longitude>180 else longitude for longitude in modulo_longitudes]
rounded_absolute_modulo_longitudes=[round(abs(longitude),1) for longitude in modulo_longitudes]

if DEGREE_SYMBOL_IN_LABELS_BOOL:
    circ='$^\circ$'
else:
    circ=''

#

letters=['a','b','c','d','e','f','g','h','i','j','k','l', 'm','n','o','p','q','r','s','t','u','v','w','x','y','z']

rounded_panel_labels=[]
for abs_longitude, signed_longitude, panel_letter in zip(rounded_absolute_modulo_longitudes, modulo_longitudes, letters):
    if signed_longitude<0:    
        direction_letter='W'
    elif signed_longitude>0:
        direction_letter='E'
    else:
        direction_letter=''
    rounded_panel_labels.append(r''+'(' + panel_letter + ') ' + str(abs_longitude) + circ + direction_letter)








## Set up the figure and panel locations

number_of_columns=4
panel_ratio=1


figure_width_in_mm=(TEX_FIGURE_WIDTH_IN_PTS/72.27)*25.4
left_padding=1.5*figure_width_in_mm/10
right_padding=figure_width_in_mm/20
top_padding=right_padding*1
bottom_padding=right_padding*3.2
horizontal_sep=right_padding/1.3
#vertical_sep=


locat=FigureSizeLocator(rows=1, columns=number_of_columns, figwidth=figure_width_in_mm, panelratio=panel_ratio, hsep=horizontal_sep, vsep=18, padleft=left_padding, padright=right_padding, padtop=top_padding, padbottom=bottom_padding, units='mm')

fig=plt.figure(figsize=locat.figsize)




#Loop over panels






for icol, cube, panel_label, panel_xlimits in zip(range(4), plot_data, rounded_panel_labels, xlimits_list):
    pos=locat.panel_position(0,icol)
    panel=fig.add_axes(pos)

    plt.axes(panel)

    #plt.plot(np.transpose(cube.data[0:NMODES,:]),cube.coord('level').points)
    panel.plot(np.transpose(cube.data[0:NMODES,:]),cube.coord('level').points)

    # set yscaling
    plt.gca().set_yscale('function', functions=(forward_depth_fun,inverse_depth_fun))
    if SPLIT_DEPTH_SCALES_1_BOOL==True:
        plt.hlines(SPLIT_DEPTH_SCALES_1_DEPTH,panel_xlimits[0],panel_xlimits[1],colors='k')
    if SPLIT_DEPTH_SCALES_2_BOOL==True:
        plt.hlines(SPLIT_DEPTH_SCALES_2_DEPTH,panel_xlimits[0],panel_xlimits[1],colors='k')
    
    # Add zero line
    plt.vlines(x=0, ymin=0, ymax=MAXIMUM_DEPTH, colors='k')
    
    
    # set yticks
    panel.set_yticks(depth_ticks_major,  minor=False) # Set major y-ticks positions
    #
    plt.ylim(0,MAXIMUM_DEPTH)
    #
    plt.gca().invert_yaxis()
    #
    panel.tick_params(which='major',axis='both',direction='out',length=MAJOR_TICK_LENGTH, width=MAJOR_TICK_WIDTH, labelsize=TICK_FONT_SIZE)
    panel.tick_params(which='minor',axis='both',direction='out',length=MINOR_TICK_LENGTH, width=MINOR_TICK_WIDTH)
    #
    
    # Turn on minor ticks, before turning back off for y
    panel.minorticks_on()
    panel.tick_params(axis='y',which='minor', left=False)
    
    
    panel.set_title(panel_label, loc='left', fontsize=PANEL_LABEL_FONT_SIZE)
    #
    if icol ==0:
        plt.ylabel('Depth (m)', fontsize=Y_AXIS_LABEL_FONT_SIZE)
        panel.set_yticklabels(depth_ticks_labels_major, minor=False) # Set major y-ticks labels
    else:
        panel.set_yticklabels([], minor=False) # Set major y-ticks labels
    #
    if DRAW_GRIDLINES:
        # Don't draw gridlines on yaxis minor ticks as they are too dense.
        panel.grid(axis='both', which='major', color='k', linewidth=GRIDLINE_WIDTH)
        panel.grid(axis='x', which='minor', color='k', linewidth=GRIDLINE_WIDTH)
    
    plt.xlim(panel_xlimits[0],panel_xlimits[1])
    







############### Add shared x-axis labels

[first_density_left,first_density_bottom,first_density_width,first_density_height]=locat.panel_position(0,0)
[second_density_left,second_density_bottom,second_density_width,second_density_height]=locat.panel_position(0,1) 
second_density_right = second_density_left + second_density_width
total_density_width = second_density_right-first_density_left

density_label_ax=fig.add_axes([first_density_left, 0.7*first_density_bottom, total_density_width, 0.4*first_density_bottom])

density_label_ax.set_xlabel(r'Potential density mode' 
                            '\n'
                            #r'(nondimensional)',
                            r'(s$^{-1}$)',
                            fontsize=X_AXIS_LABEL_FONT_SIZE)
                            
density_label_ax.set_xticks([])
density_label_ax.set_yticks([])
density_label_ax.set_frame_on(False)





[first_velocity_left,first_velocity_bottom,first_velocity_width,first_velocity_height]=locat.panel_position(0,2)
[second_velocity_left,second_velocity_bottom,second_velocity_width,second_velocity_height]=locat.panel_position(0,3) 
second_velocity_right = second_velocity_left + second_velocity_width
total_velocity_width = second_velocity_right-first_velocity_left

velocity_label_ax=fig.add_axes([first_velocity_left, 0.7*first_velocity_bottom, total_velocity_width, 0.4*first_velocity_bottom])

velocity_label_ax.set_xlabel(r'Velocity mode' 
                            '\n'
                            r'(nondimensional)',
                            fontsize=X_AXIS_LABEL_FONT_SIZE)

velocity_label_ax.set_xticks([])
velocity_label_ax.set_yticks([])
velocity_label_ax.set_frame_on(False)







############# Add a shared legend below

fake_figure = plt.figure()
fake_ax=fake_figure.add_subplot(111)
for mode_i in range(0,NMODES):
    mode_label_string="Mode " + str(mode_i+1)
    fake_ax.plot([1,2,3],[1,2,3], label=mode_label_string)




total_panels_width=second_velocity_right - first_density_left

#legend_ax=fig.add_axes([first_density_left, 0.02*first_density_bottom, total_panels_width, 0.3*first_density_bottom])
legend_ax=fig.add_axes([first_density_left, 0.01*first_density_bottom, total_panels_width, 0.3*first_density_bottom])
legend_ax.legend(*fake_ax.get_legend_handles_labels(), fontsize=LEGEND_FONT_SIZE, ncol=number_of_columns, loc='center', frameon=False)

legend_ax.axis("off")









########### Save the figure
IMAGEFILE=os.path.join(PLOTDIR,'example_mode_structure_profiles.png')

if SAVE_HIGH_RES_BOOL:
    fig.savefig(IMAGEFILE,dpi=300)
else:
    fig.savefig(IMAGEFILE)
    
print('Figure saved to: '+IMAGEFILE)





