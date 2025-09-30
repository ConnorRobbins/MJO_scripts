#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 11:48:31 2023

@author: rgq13jzu
"""





import iris
import warnings
import matplotlib
import matplotlib.colors as colors
import cmocean
import seaborn
import os
import numpy as np



def MFF_Assign_Variable_Colourmaps(var_name,diverging_bool):
    """ Returns a consistently specified colourmap based on 'var_name' and 'diverging_bool'.
        
        Keyword arguments:
        var_name -- string - name of variable to be plotted,
        diverging_bool -- bool - True: return diverging colourmap. False: Return non-diverging colourmap.
        """
    if not type(diverging_bool) == bool:
        raise Exception("'diverging_bool' must be set as a Boolean.")
    #
    if diverging_bool: # Assign diverging colour schemes
        if var_name == 'swsal':
            return cmocean.cm.curl
        elif var_name == 'swtheta':
            return cmocean.cm.balance
        elif var_name == 'ucur':
            return cmocean.cm.delta
        elif var_name == 'vcur':
            return cmocean.cm.tarn_r
        elif var_name == 'swpd':
            return seaborn.color_palette("PuOr",as_cmap=True)
        elif var_name == 'inferred_displacement':
            return seaborn.color_palette("RdGy_r",as_cmap=True)
        elif var_name == 'projection_coefficient':
            return seaborn.color_palette("RdBu_r",as_cmap=True)
        else:
            warnings.warn("The variable string doesn't have a colourmap associated with it.")
            return matplotlib.cm.get_cmap('rainbow')          
        #
    else: # Assign non-diverging colour schemes
        if var_name == 'ucur':
            return matplotlib.cm.get_cmap('rainbow')        
        elif var_name == 'swpd':
            return cmocean.cm.deep
        else:
            warnings.warn("The variable string doesn't have a colourmap associated with it.")
            return matplotlib.cm.get_cmap('rainbow')    










def MFF_Get_Diverging_Colours(var_name,contour_values,contour_centre=0):
    """ Returns a list of colours for a diverging colour bar based on 'var_name'.
        Colours will be centred on 'contour_centre' and depend on values 'contour_values'.
        If 'contour_centre' is not an element of 'contour_values' then the interval containing it will be coloured white.
        
        Keyword arguments:
        var_name -- string - name of variable to be plotted,
        contour_values -- list of int/float (increasing, in order) - values at which contours will be plotted
        contour_centre -- int/float - value away from which colours diverge
        """
    # First split the contour values around the centre value
    less_than_centre_contours=[contour_value for contour_value in contour_values if contour_value < contour_centre]
    greater_than_centre_contours=[contour_value for contour_value in contour_values if contour_value > contour_centre]
    # Now count the number of colours needed for this many contours. In order to preserve similarity in colour gradient if the number of contours less/greater than centre vary we calculate colours as though contours were evenly distributed (with the larger number of contours occuring either side of centre). 
    Ngreater=len(greater_than_centre_contours)
    Nless=len(less_than_centre_contours)
    N_even_contours=max(Nless,Ngreater)
    Ncolours=2*N_even_contours +1 # M contours require M+1 colours
    # Add contour occurring exactly at contour_centre if necessary 
    if contour_centre in contour_values: 
        Ncolours+=1 
        whitening_needed_bool=False
    else:
        whitening_needed_bool=True
    #
    my_colourmap=MFF_Assign_Variable_Colourmaps(var_name,True)
    #
    cmap_clip=0.1 # Skip this much of the cmap on each side before sampling to avoid really dark bits
    sampled_colours= [my_colourmap(cmap_clip + (1-2*cmap_clip)*x/(Ncolours-1) ) for x in range(0,Ncolours)]
    if whitening_needed_bool:# Make middle colour actually white if it should be white
        sampled_colours[N_even_contours]=(1,1,1) 
    # Crop out the extra un-needed colours made from temporarily expanding the number of contours to be even around 'contour_centre'.
    Ncrop=Ngreater-Nless
    if Ncrop > 0: # throw away unneeded colours at beginning of list
        sampled_colours=sampled_colours[Ncrop:]
    elif Ncrop<0: # throw away unneeded colours at end of list
        sampled_colours=sampled_colours[:Ncrop]
    return sampled_colours

        
        








def MFF_Quick_Cube_Load(directory,filename):
    """
    Loads cube from file into cubelist, concatenates then returns cube.
    """
    filepath=os.path.join(directory, filename)
    print('Loading cube from: {0!s}'.format(filepath))
    cubelist=iris.load(filepath)   # Loads in a Cubelist of cubes
    loaded_cube=cubelist.concatenate_cube() #This line makes a cube from the cubelist
    return loaded_cube






















def MFF_Cube_Circular_Spatial_Subset(cube, latitude_range=None, longitude_range=None):
    #
    def range_input_check(input_range):
        if (not isinstance(input_range,list)) or (not len(input_range) == 2) :
            raise Exception("Ranges should be given as a list of length 2.")
    #
    if (latitude_range is None) and (longitude_range is None):
        raise Exception("At least one valid input for either 'longitude_range' or 'latitude_range' must be given.")
    #
    if latitude_range is not None:
        range_input_check(latitude_range)
        cube=cube.intersection(latitude=(latitude_range[0],latitude_range[1]))
    #
    if longitude_range is not None:
        range_input_check(longitude_range)
        # Extract data for correct longitudes and shuffle the cube around for circular plotting, jump over 180 degree data point
        cube.coord('longitude').attributes['modulo']=360
        cube_west_longs=cube.extract(iris.Constraint(longitude=lambda cell: (180 < cell) and (cell < 360)))
        cube_east_longs=cube.extract(iris.Constraint(longitude=lambda cell: (0 <= cell) and (cell < 180)))
        cube_west_longs.coord('longitude').bounds=cube_west_longs.coord('longitude').bounds-360
        cube_west_longs.coord('longitude').points=cube_west_longs.coord('longitude').points-360
        cube=iris.cube.CubeList([cube_west_longs,cube_east_longs]).concatenate()[0]
        cube.coord('longitude').circular=True
        cube=cube.intersection(longitude=(longitude_range[0],longitude_range[1]))
    #
    return cube    





def MFF_Cube_Extract_Lagged_Mean_Days_Data(cube,n_days):
    #
    #
    tcoord=cube.coord('time')
    tn=tcoord.units.num2date(tcoord.points[tcoord.points==n_days*24.0])
    timecon=iris.Constraint(time=tn)
    with warnings.catch_warnings(): # Iris will print a deprecation warning every time otherwise
        warnings.simplefilter("ignore")
        with iris.FUTURE.context(cell_datetime_objects=True):
            return cube.extract(timecon) # Extract data with correct lag
            












def Make_Tick_Labels(ticks,coord,degree_symbol=False):
    #
    # Given the tick positions and the co-ordinate to which they refer (i.e. latitude/longitude,depth), typeset tick labels with units and to be in the correct range for that co-ordinate.
    #
    # "ticks" is expected to be an array of the numerical values for the positions of the ticks.
    # "coord" is expected to be one of the three strings: {"longitude", "latitude", "depth"}.
    #
    labels=[]
    if degree_symbol:
        circ="$^\circ$"
    else:
        circ=""
    if coord == "longitude":
        for longitude in ticks:
            long_tick=longitude%360
            if long_tick == 180:
                labels.append("180"+ circ)
            elif long_tick == 0:
                labels.append("0"+ circ)
            elif long_tick < 180:
                labels.append( str(long_tick)+ circ + "E")
            elif long_tick > 180:
                labels.append( str(abs(long_tick-360))+ circ + "W")
            else:
                raise Exception("Something fishy is happening with labelling the longitude ticks")
        return labels
    #
    elif coord == "latitude":
        for latitude in ticks:
            if latitude == 90:
                labels.append("90"+ circ)
            elif latitude == 0:
                labels.append("0"+ circ)
            elif latitude < 0:
                labels.append(str(abs(latitude))+ circ+"S")
            elif latitude < 90:
                labels.append( str(latitude)+ circ + "N")
            else:
                raise Exception("Something fishy is happening with labelling the major ticks") 
        return labels
    #
    elif coord == "depth":
        for depth in ticks:
            #labels.append(str(int(depth))+"m")
            labels.append(str(int(depth)))
        return labels
    #
    else:
        raise Exception("The string \"coord\" has not been recognised as a co-ordinate.")




















def Assign_Piecewise_Linear_Yaxis_Scaling_Functions(split1_bool,split1_yval,split1_ycompression_factor,split2_bool,split2_yval,split2_ycompression_factor):
    #
    # Split the y axis into upto three sections, with each section able to take a different piecewise linear y-axis scaling.
    # "split1_bool" and "split2_bool" should be Booleans, with values depending on how many times y-axis scale is split.
    # "split1_yval" and "split2_yval" should be numeric, with values corresponding to the y-value at which the y-axis  is split.
    # "split1_ycompression_factor" and "split2_ycompression_factor" should be numeric, with values corresponding to the factor by which each vertical section will be compressed compared to its default scaling.
    #
    # Note: If only splitting once an error will be thrown when split2 variables are used instead of split1 variables.
    #
    #
    # First check that the inputs are sensible
    if not(type(split1_bool)==bool):
        raise Exception("\"split1_bool\" must be a Boolean")
    if not(type(split2_bool)==bool):
        raise Exception("\"split2_bool\" must be a Boolean")
    if split2_bool and not split1_bool:
        raise Exception("\"split2_bool\" must not be True if \"split1_bool\" is False. If trying to split on one level use \'split1\' variables not \'split2\'.")
    if split1_yval > split2_yval:
        raise Exception("\"split1_yval\" must be less than \"split2_yval\".")
    #
    #
    #
    #
    def forward_depth_fun_0_splits(h_orig):
        h=h_orig.copy()
        return h
    #
    def inverse_depth_fun_0_splits(h_orig):
        h=h_orig.copy()
        return h
    #
    #
    #
    def forward_depth_fun_1_splits(h_orig):
        h=h_orig.copy()
        for fi in range(len(h)):
            h_i=h[fi]
            if h_i > split1_yval:
                h[fi]=split1_yval + ((h_i-split1_yval)/split1_ycompression_factor)
        return h
     #
    def inverse_depth_fun_1_splits(h_orig):
        h=h_orig.copy()
        for fi in range(len(h)):
            h_i=h[fi]
            if h_i > split1_yval:
                h[fi]= split1_yval + split1_ycompression_factor*(h_i-split1_yval)
        return h
    #
    #
    #
    def forward_depth_fun_2_splits(h_orig):
        h=h_orig.copy()
        transformed_split_depth_2 = split1_yval + ((split2_yval-split1_yval)/split1_ycompression_factor)
        for fi in range(len(h)):
            h_i=h[fi]
            if h_i > split2_yval:
                h[fi]= transformed_split_depth_2 + ((h_i-split2_yval)/split2_ycompression_factor)
            elif h_i > split1_yval:
                h[fi]=split1_yval + ((h_i-split1_yval)/split1_ycompression_factor)
        return h
    #
    def inverse_depth_fun_2_splits(h_orig):
        h=h_orig.copy()
        transformed_split_depth_2 = split1_yval + ((split2_yval-split1_yval)/split1_ycompression_factor)
        for fi in range(len(h)):
            h_i=h[fi]
            if h_i > transformed_split_depth_2:
                h[fi]= split2_yval + split2_ycompression_factor*(h_i - transformed_split_depth_2)
            elif h_i > split1_yval:
                h[fi]= split1_yval + split1_ycompression_factor*(h_i-split1_yval)
        return h
    #
    #
    #
    if split1_bool == False : # If not splitting top level then no splits
        forward_depth_fun = forward_depth_fun_0_splits
        inverse_depth_fun = inverse_depth_fun_0_splits
    elif split2_bool == False : # If not then splitting lower level only one split
        forward_depth_fun = forward_depth_fun_1_splits
        inverse_depth_fun = inverse_depth_fun_1_splits
    else: # Otherwise there is two splits
        forward_depth_fun = forward_depth_fun_2_splits
        inverse_depth_fun = inverse_depth_fun_2_splits
    #
    #
    #
    return forward_depth_fun, inverse_depth_fun



def MFF_ray_slope_from_Nsquared(Nsquared, start_points, time_period_in_days = 48):
    '''
    Inputs:
        Nsquared: iris cube of Nsquared
        start_points: list of start points as tuples (x,z)
        
    Outputs:
        ray_trajectories: list of trajectories as tuples, each tuple contain lists of ([xi],[zi]) for that trajectory
    '''
    
    # Constants
    #time_period_in_days = 48 # use to calculate omega (angular frequency)
    earth_radius = 6378000  # (metres)
    omega = 2*np.pi / (time_period_in_days*86400) # angular frequency in seconds for time period


    depthsCoord = Nsquared.coord('level')
    n_depths = depthsCoord.points
    max_depth = depthsCoord.points.max()

    longsCoord = Nsquared.coord('longitude')
    

    # slope_cube is calculated to be equivalent to dz/dx in metres
    slope_cube = ((omega**2) * ((Nsquared - omega**2)**(-1)))**(0.5)
    # convert from dz/dx (x in m) to dz/dlon
    slope_cube = slope_cube * np.pi * earth_radius / 180 
    
    
    
    # Initialise storage for all trajectories
    ray_trajectories=[]
    
    for start_point in start_points:
        # Assign start points, snapping x to grid
        x_start=start_point[0]
        x_index=longsCoord.nearest_neighbour_index(x_start)
        x=longsCoord[x_index].cell(0)[0]
        
        z=start_point[1]
        
        # Initialise storage for  individual trajctory
        x_store=[]
        z_store=[] 


        # Calculate until a point with masked slope is encountered or until you exceed model depth
        while True:

            # Store
            x_store.append(x)
            z_store.append(z)
      
            # Get ready to interpolate to find next point
            z_index=slope_cube.coord('level').nearest_neighbour_index(z)
            closest_z = depthsCoord[z_index].cell(0)[0] 
    
            # Establish in which interval our z point lies
            if closest_z < z: # z is in interval with min closest_z
                z1 = closest_z 
                z2 = depthsCoord[z_index+1].cell(0)[0] 
                slope_z1 = slope_cube.data[z_index, x_index]
                slope_z2 = slope_cube.data[z_index+1, x_index]
            elif closest_z > z: # z is in interval with max closest_z
                z1 = depthsCoord[z_index-1].cell(0)[0] 
                z2 = closest_z
                slope_z1 = slope_cube.data[z_index-1, x_index]
                slope_z2 = slope_cube.data[z_index, x_index]
            elif not closest_z == z:
                raise Exception('Something has gone wrong, why can z not be ordered?')

            # Interpolate to find slope at z
            if not closest_z == z:
                t_interval_parameter = (z-z1)/(z2-z1)
                interp_slope = slope_z1 * (1-t_interval_parameter) + slope_z2 * t_interval_parameter
            else:        
                z1 = z
                interp_slope = slope_cube.data[z_index, x_index]
            # 
            # Step forwards using slope unless interp slope is masked
            if np.ma.is_masked(interp_slope):
                #print('Slope at this point is masked, ending trajectory.')
                break
            else:
                x_index = x_index + 1
                z = (longsCoord[x_index].cell(0)[0] - x)*interp_slope + z
                x = longsCoord[x_index].cell(0)[0]
    
            # Check that z isn't below our model region
            if z > max_depth:
                x_store.append(x)
                z_store.append(z)
                #print('Depth exceeds max model depth, ending trajectory.')
                break
           
           
        #
        ray_trajectories.append( (x_store, z_store) )
    return ray_trajectories


