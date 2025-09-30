#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 11:48:31 2023

@author: rgq13jzu
"""



import os
import iris
import iris.quickplot as qplt
import iris.plot as iplt
import matplotlib.pyplot as plt
import pdb
import numpy as np
import numpy.ma as ma
import warnings
import functions_dynmodes as fdyn


from panels import FigureSizeLocator
import MyPaperFigureFunctions as MFF




PROJECTION_BASEDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data','glorys12v1aeq1erai_zlev_d','processed')
WIND_BASEDIR=os.path.join(os.path.sep,'gpfs','scratch','rgq13jzu','data','era5gloerai_sfc_d','processed')



PLOTDIR=os.path.join(os.path.sep,'gpfs','home','rgq13jzu','MJO_scripts','Plotting_Scripts','Paper_Figures','Plotting_Scripts','Figures')



VAR_NAME='projection_coefficient'

## The string component "{PHASE_NUMBER}" in XXX_TEMPLATE_FILENAME will be replaced by the numbers 1-8
PROJECTIONS_TEMPLATE_FILENAME='swpd_all_rac_b20_200_n241_rmm008FS-all{PHASE_NUMBER}_lag_ss_lat_-1.5_1.5_projected_onto_rmodes_normalised_5m_all_2003-to-2020_ss_lat_-1.5_1.5.nc' ; 
ZONAL_WIND_ANOMALY_TEMPLATE_FILENAME='uwnd_1_rac_b20_200_n241_rmm008FS-all{PHASE_NUMBER}_lag_ss_lat_5_5.nc' # Use wind velocity anomalies
ZONAL_WIND_ANOMALY_TEMPLATE_FILENAME='taux_1_rac_b20_200_n241_rmm008FS-all{PHASE_NUMBER}_lag_ss_lat_5_5.nc' # Use wind stress anomalies


PLOT_MODE_NUMBERS=[1,2,3] # length is number of panels
#PLOT_MODE_NUMBERS=[4,5,6]
#PLOT_MODE_NUMBERS=[1] # length is number of panels

#PLOT_PHASE_NUMBERS=range(1,8+1)
PLOT_PHASE_NUMBERS=[1,2,3,4,5,6,7,8,9] # Will be plotted in order given! Set to be circular with mod 8: if you want to loop top of plot back to bottom keep counting up i.e. [...,7,8,9] will show [...,7,8,1]

LAGGED_MEAN_DAYS=0




LONG_BEG=30
LONG_END=390



CONTOUR_LEVELS=np.array([-0.9,-0.6,-0.3,-0.05,0.05,0.3,0.6,0.9]) 



#ZONAL_WIND_CONTOUR_LEVELS=np.array([-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2]) # contours for wind velocity
ZONAL_WIND_CONTOUR_LEVELS=np.array([-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2])/100 # wind stress


# example velocity line parameters
PLOT_EXAMPLE_VELOCITY_BOOL=True
EXAMPLE_VELOCITY=3.4 # in ms^-1
DAYS_PER_MJO_CYCLE = 56 # Controls how velocity is fit to the "Phase" axis. (7 days per phase)
EXAMPLE_LONGITUDE_START=150


############
# Plotting options

SAVE_HIGH_RES_BOOL=True

X_MAJOR_TICK_STEP=30; X_MINOR_TICK_STEP=10

TEX_FIGURE_WIDTH_IN_PTS=397.48499



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
COLORBAR_VERTICAL_SHIFT=-0.15 # Move colour bar up and down
    



DRAW_GRIDLINES=False # Set to True to add overlay gridlines
GRIDLINE_WIDTH=0.5


ZONAL_WIND_CONTOUR_COLOURS='k'

ZONAL_WIND_NONZERO_CONTOUR_LINEWIDTH=1
ZONAL_WIND_ZERO_CONTOUR_LINEWIDTH=1.5

EXAMPLE_VELOCITY_LINE_COLOUR = 'm'
EXAMPLE_VELOCITY_LINE_WIDTH = 1.5 







#################




plot_cube_list=[]

# This is a filthy way of looping, if you do this again loop over PHASE first so you can load all mode data at once
for mode_number in PLOT_MODE_NUMBERS:
    phase_cube_list=[]
    #
    for PHASE_NUMBER in PLOT_PHASE_NUMBERS:
        phase_mod_8 = PHASE_NUMBER % 8 
        load_phase = phase_mod_8 if phase_mod_8 != 0 else 8
        PROJECTIONS_FILENAME=PROJECTIONS_TEMPLATE_FILENAME.replace("{PHASE_NUMBER}", str(load_phase))
        # Load projections data for this phase
        projections_filepath=os.path.join(PROJECTION_BASEDIR,PROJECTIONS_FILENAME)
        #print('projections_filepath: {0!s}'.format(projections_filepath))
        cubelist=iris.load(projections_filepath)   # Loads in a Cubelist of cubes
        phase_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist
    
        # Extract sub-cubes needed for plotting, in order: mode number, spatial subset, lag days (no particular reason for this)
        ## mode number
        modecon=iris.Constraint(mode_number=mode_number)
        phase_cube=phase_cube.extract(modecon)
        # spatial subset
        phase_cube=MFF.MFF_Cube_Circular_Spatial_Subset(phase_cube, longitude_range=[LONG_BEG,LONG_END])
        # Extract data for correct length lag on lagged mean
        tcoord=phase_cube.coord('time')
        tn=tcoord.units.num2date(tcoord.points[tcoord.points==LAGGED_MEAN_DAYS*24.0])
        timecon=iris.Constraint(time=tn)
        with warnings.catch_warnings(): # Iris will print a deprecation warning every time otherwise
            warnings.simplefilter("ignore")
            with iris.FUTURE.context(cell_datetime_objects=True):
                phase_cube=phase_cube.extract(timecon) # Extract data with correct lag
    
        # Strip time auxillary coordinate from cube
        phase_cube.remove_coord('time')
        # Add an auxillary coord for Phase number, cubes will be merged along this coord
        phase_cube.add_aux_coord(iris.coords.AuxCoord(PHASE_NUMBER, long_name='phase_number'))    
    
        # Add data for current phase to cube list
        phase_cube_list.append(phase_cube)
    #
    plot_cube = iris.cube.CubeList(phase_cube_list).merge_cube()
    plot_cube_list.append(plot_cube)






wind_cube_list=[]

# Loop over phases for wind data
for phase_number in PLOT_PHASE_NUMBERS:
    
    phase_mod_8 = phase_number % 8 
    load_phase = phase_mod_8 if phase_mod_8 != 0 else 8
    
    wind_filename = ZONAL_WIND_ANOMALY_TEMPLATE_FILENAME.replace("{PHASE_NUMBER}", str(load_phase))
    # Load wind anomaly data for this phase
    wind_filepath = os.path.join(WIND_BASEDIR, wind_filename)
    cubelist = iris.load(wind_filepath)
    wind_cube = cubelist.concatenate_cube()
    # 
    wind_cube = MFF.MFF_Cube_Circular_Spatial_Subset(wind_cube, longitude_range=[LONG_BEG,LONG_END])
    #
    wind_cube = MFF.MFF_Cube_Extract_Lagged_Mean_Days_Data(wind_cube, LAGGED_MEAN_DAYS)
    #
    wind_cube.add_aux_coord(iris.coords.AuxCoord(phase_number, long_name='phase_number'))
    # Strip cell methods as these prevent cube being merged into one plotting cube
    wind_cube.cell_methods=None
    #
    wind_cube_list.append(wind_cube)
    
# Merge cubes into one cube for plotting
wind_plot_cube = iris.cube.CubeList(wind_cube_list).merge_cube()



# Calculate example velocity line (if needed)
if PLOT_EXAMPLE_VELOCITY_BOOL:
    days_per_MJO_phase = DAYS_PER_MJO_CYCLE/8
    earth_radius = 6378000
    one_metre_in_degrees = 360/(2*np.pi*earth_radius)
    one_second_in_phases = 1/(86400*days_per_MJO_phase)
    velocity_in_degrees_per_phase = EXAMPLE_VELOCITY * one_metre_in_degrees / one_second_in_phases
    #
    example_velocity_longitudes = [EXAMPLE_LONGITUDE_START + (phase - 1)*velocity_in_degrees_per_phase for phase in PLOT_PHASE_NUMBERS]






#################
#################
#################
#################













########


x_ticks_major=np.arange(LONG_BEG, LONG_END +1, X_MAJOR_TICK_STEP)
x_ticks_minor=np.arange(LONG_BEG, LONG_END +1, X_MAJOR_TICK_STEP)


y_ticks_major = [str(phase % 8) if phase % 8 != 0 else str(8) for phase in PLOT_PHASE_NUMBERS]


COLOURS=MFF.MFF_Get_Diverging_Colours(VAR_NAME,CONTOUR_LEVELS)




x_ticks_major_labels=MFF.Make_Tick_Labels(x_ticks_major,'longitude')



zonal_contour_linewidths=[ZONAL_WIND_NONZERO_CONTOUR_LINEWIDTH if contour_level != 0 else ZONAL_WIND_ZERO_CONTOUR_LINEWIDTH for contour_level in ZONAL_WIND_CONTOUR_LEVELS]



## Set up the figure and panel locations

panel_ratio=3.2


figure_width_in_mm=(TEX_FIGURE_WIDTH_IN_PTS/72.27)*25.4
left_padding=1.5*figure_width_in_mm/10
right_padding=figure_width_in_mm/20
top_padding=right_padding*1.
bottom_padding=right_padding*4.5
horizontal_sep=right_padding/1.3
vertical_sep=8



number_of_rows=len(plot_cube_list)
number_of_columns=1



locat=FigureSizeLocator(rows=number_of_rows, columns=number_of_columns, figwidth=figure_width_in_mm, panelratio=panel_ratio, hsep=horizontal_sep, vsep=vertical_sep, padleft=left_padding, padright=right_padding, padtop=top_padding, padbottom=bottom_padding, units='mm')


fig=plt.figure(figsize=locat.figsize)



letters=['a','b','c','d','e','f','g','h','i','j','k','l', 'm','n','o','p','q','r','s','t','u','v','w','x','y','z']










icol=0
for ipanel, cube, panel_letter in zip(range(number_of_rows), plot_cube_list, letters[:number_of_rows]):
    irow=ipanel
    pos=locat.panel_position(irow,icol)
    panel=fig.add_axes(pos)

    plt.axes(panel)
    plt.gca().patch.set_color('.3') # Dark grey
    plt.gca().patch.set_edgecolor('k')
    plt.gca().patch.set_hatch('++') 
    #
    panel_with_plot=iplt.contourf(cube, levels=CONTOUR_LEVELS, coords=['longitude','phase_number'], extend='both',colors=COLOURS)
    panel_with_wind=iplt.contour(wind_plot_cube, levels=ZONAL_WIND_CONTOUR_LEVELS, coords=['longitude','phase_number'], colors=ZONAL_WIND_CONTOUR_COLOURS, linewidths = zonal_contour_linewidths)
    #panel_with_wind=iplt.contour(wind_plot_cube, levels=ZONAL_WIND_CONTOUR_LEVELS, coords=['longitude','phase_number'], colors=ZONAL_WIND_CONTOUR_COLOURS, linestyles='solid', negative_linestyles='dashed')
    if PLOT_EXAMPLE_VELOCITY_BOOL:
        panel_with_example_velocity=plt.plot(example_velocity_longitudes,PLOT_PHASE_NUMBERS, linewidth=EXAMPLE_VELOCITY_LINE_WIDTH, color=EXAMPLE_VELOCITY_LINE_COLOUR)
    #
    plt.xlim(LONG_BEG,LONG_END)
    #
    panel.set_xticks(x_ticks_major, minor=False) # Set major x-ticks positions
    panel.set_xticks(x_ticks_minor, minor=True) # Set minor x-ticks positions
    if (irow==number_of_rows-1) or not SHARE_X_TICKS_BOOL:
        panel.set_xticklabels(x_ticks_major_labels, minor=False) # Set major x-ticks labels
    else:
        panel.set_xticklabels([],minor=False)
    #
    plt.gca().set_yticks(PLOT_PHASE_NUMBERS,minor=False)
    plt.gca().set_yticklabels(y_ticks_major, minor=False)
    

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








# Add the color bar underneath
                # 
[lowest_panel_left,lowest_panel_bottom,lowest_panel_width,lowest_panel_height]=locat.panel_position( number_of_rows-1 , 0) 
lowest_panel_right= lowest_panel_left + lowest_panel_width
                #
middle=0.5*(lowest_panel_right+lowest_panel_left)
width=COLORBAR_WIDTH_MULTIPLIER*(lowest_panel_right-lowest_panel_left)
bottom=lowest_panel_bottom+COLORBAR_VERTICAL_SHIFT
left=middle-0.5*width
                #
color_bar_ax=fig.add_axes([left,bottom,width,COLORBAR_HEIGHT])
fig.colorbar(panel_with_plot, cax=color_bar_ax, orientation='horizontal')
color_bar_ax.set_title('Projection coefficient amplitude',fontsize=COLORBAR_TITLE_FONT_SIZE)
color_bar_ax.tick_params(labelsize=COLORBAR_TICK_FONT_SIZE)








#
## Add shared y axis label on

# Calculate positions
[highest_panel_left,highest_panel_bottom,highest_panel_width,highest_panel_height]=locat.panel_position(0, 0) 
all_panel_height=highest_panel_bottom + highest_panel_height - lowest_panel_bottom
# Add the labels and hide the axes edges tick marks
shared_ylabel_ax=fig.add_axes([0.4*lowest_panel_left, lowest_panel_bottom, lowest_panel_left/10, all_panel_height] )
shared_ylabel_ax.set_ylabel('MJO phase',fontsize=Y_AXIS_LABEL_FONT_SIZE)
shared_ylabel_ax.set_xticks([])
shared_ylabel_ax.set_yticks([])
shared_ylabel_ax.set_frame_on(False)




















image_file_name="swpd_Hovmoller_projection_coefficient_amplitude_by_phase" + ".png"
#image_file_name="tmp" + ".png"


IMAGEFILE=os.path.join(PLOTDIR,image_file_name)


if SAVE_HIGH_RES_BOOL:
    plt.savefig(IMAGEFILE,dpi=300)
else:
    plt.savefig(IMAGEFILE)
    
print('Figure saved to: '+IMAGEFILE)









