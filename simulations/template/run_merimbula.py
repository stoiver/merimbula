"""
Main meribula script using new interface
"""

#-------------------------------
# Module imports
#-------------------------------
import sys, os
import numpy as np

import pandas as pd
from scipy.interpolate import interp1d

import anuga
import project
from project import yieldstep, outputstep, duration
from project import weeds, canal, depth_canal

from anuga import log
log.log_filename = 'run_merimbula.log'

weed_dir = project.weed_dir

#-------------------------------
# Domain
#-------------------------------

if anuga.myid == 0:
    print ('Creating domain from', project.mesh_filename)

    domain = anuga.pmesh_to_domain_instance(project.mesh_filename, anuga.Domain, use_cache=True)

    domain.set_name(project.simulation_name)
    domain.check_integrity()
    domain.set_georeference(project.georef)


    print ('Number of triangles = ', len(domain))
    print ('The extent is ', domain.get_extent())


    #-------------------------------
    # Initial Conditions
    #-------------------------------

    #elevation_offset=0.1

    print ('Initial values')
    bathymetry_filename =  project.bathymetry_filename[:-4] + '.xya'

    print (bathymetry_filename)

    # domain.set_quantity('elevation',
    #                     filename = bathymetry_filename,
    #                     alpha = 0.5,
    #                     verbose = True,
    #                     use_cache = True)

    basename = project.bathymetry_filename[:-4]
    print('TRYING TO READ %s' % basename+'.npy')
    try:
        elev_xyz = np.load(basename+'.npy')
    except:
        print('TRYING TO READ %s' % basename+'.xya')
        elev_xyz = np.genfromtxt(fname=basename+'.xya', delimiter=',', skip_header=1)
        print('SAVING %s' % basename+'.npy')
        np.save(basename+'.npy', elev_xyz)

    print('CREATING nearest neighbour interpolator')
    from anuga.utilities.quantity_setting_functions import make_nearestNeighbour_quantity_function
    elev_fun_wrapper = make_nearestNeighbour_quantity_function(elev_xyz, domain, k_nearest_neighbours=3, method='min')
    
    print('FITTING to domain')
    domain.set_quantity('elevation', elev_fun_wrapper, location='centroids')

    #domain.set_quantity('elevation',expression='elevation +%f' %elevation_offset)
    domain.set_quantity('stage', 0.0)

else:
    domain = None

domain = anuga.distribute(domain)

#-------------------------------
# Setup domain runtime parameters
#-------------------------------

domain.store = project.store   #Store for visualisation purposes
domain.smooth = project.store_vertices_uniquely
domain.set_low_froude(project.low_froude)
domain.set_flow_algorithm(project.flow_algorithm)
domain.set_quantity('friction', project.global_friction)
try:
    domain.set_multiprocessor_mode(project.multiprocessor_mode)
except:
    pass


print (f'Stats for domain on rank {anuga.myid}')
print (domain.statistics())


if weeds:
    from weed_zones import set_friction_from_weed_zones
    set_friction_from_weed_zones(domain, weed_dir)

# domain.set_plotter()
# import matplotlib.pyplot as plt

# import matplotlib.cm as cm
# import numpy as np

# domain.tripcolor(
#               facecolors=np.sqrt(domain.stage - domain.elev),
#               cmap=cm.viridis,  # A visually appealing colormap
#               vmin=0.0,
#               vmax=2.0  # Adjusted to cover the range of friction values
#               )
# plt.colorbar()
# plt.show()

#--------------------------------
# dredge out the canal
#--------------------------------
if canal:
    canal_polygon = [[759222.474012,5912903.796898],
            [759191.946009,5912861.297128],
            [759224.269777,5912866.684423],
            [759242.100000,5912879.000000],
            [759252.700000,5912892.000000],
            [759256.593546,5912915.170076],
            [759242.826015,5912939.113609],
            [759228.000000,5912954.000000],
            [759209.600000,5912931.000000],
            [759193.800000,5912906.000000],
            [759170.000000,5912890.000000]]

    domain.set_quantity('elevation',numeric = -depth_canal,
                   polygon = canal_polygon,
                   smooth = True,
                   verbose = True,
                   location = 'centroids',
                   use_cache = True)





#-------------------------------
# Boundary conditions
#-------------------------------
if anuga.myid == 0: 
    print ('Boundaries')

#----------------------------------------
#   Tidal cycle recorded at Eden as open
#----------------------------------------
if anuga.myid == 0:
    print ('Open sea boundary condition from ',project.boundary_filename)


tide_df = pd.read_csv(project.boundary_filename)
tide_function = interp1d(tide_df['timestamp'], tide_df['Stage'], kind='linear', fill_value=0.0, bounds_error=False)


#--------------------------------------
#  Boundaries, open boundary with tide
#  elsewhere reflective
#--------------------------------------
Br = anuga.Reflective_boundary(domain)
Bf = anuga.Flather_external_stage_zero_velocity_boundary(domain, function = tide_function)

domain.set_boundary({'exterior': Br, 'open': Bf})

#-------------------------------------------------------
# Set the start time of the simulation to the first time in the tide data
#-------------------------------------------------------
domain.set_starttime(tide_df['timestamp'].iloc[0])
domain.set_timezone('Australia/Sydney')

# 26th October 2003 01:45:00, just before change from 
# AEST (UTC+10) to AEDT (UTC+11  at 2am)
# domain.set_starttime(tide_df['timestamp'].iloc[3271])

#-------------------------------
# Find a triangle next to mid point of tide boundary
#-------------------------------

import numpy as np
p0 = np.array([761052.7, 5912151.0])
p1 = np.array([759608.8, 5912326.0])

x0 = 0.5*(p0[0]+p1[0])
y0 = 0.5*(p0[1]+p1[1])

try:
    tid = domain.get_triangle_containing_point([ x0-9, y0+6])
except:
    tid = None

print (f'Triangle id next to middle of tide boundary: {tid}')
#print (domain.centroid_coordinates[9433])

anuga.barrier()

#-------------------------------
# Evolve
#-------------------------------
import time
t0 = time.time()

if anuga.myid == 0:
    import os
    num_threads = os.environ.get('OMP_NUM_THREADS')
    if num_threads is not None:
        num_threads = int(num_threads)
    else:
        num_theads = 1     
    print (' ')
    print ('#',60*'=')
    print ('#','Evolving domain')
    print ('#',60*'=')
    print ('#','Number of MPI processes = ', anuga.numprocs)
    print ('#','Number of OPENMP threads = ', num_threads)
    print ('#','Multiprocessor Mode = ', domain.multiprocessor_mode)
    print ('#','Yield step = ', yieldstep)
    print ('#','Output step = ', outputstep)
    print ('#','Duration  = ', duration)
    print ('#',60*'=')
    print (' ')
#===========================================================================
# Main Evolve Loop
#===========================================================================

for t in domain.evolve(yieldstep = yieldstep, outputstep = outputstep, duration = duration):
        
    # This only happens on processor that owns the triangle.
    if tid is not None:
        print (domain.timestepping_statistics(datetime = True))
        print (f'    Tide {tide_function(t):.3f}, Mid Boundary Stage {domain.get_quantity("stage").centroid_values[tid]:.3f} ')
        sys.stdout.flush()

anuga.barrier()

if anuga.myid == 0:
    print (f'That took {(time.time()-t0):.2f} seconds on {anuga.numprocs} MPI processes and {num_threads} OPENMP threads')



anuga.barrier()


if anuga.numprocs > 1:

    if anuga.myid == 0:
        print (' ')
        print ('#',60*'=')
        print ('#','Merging partitioned sww files')
        print ('#',60*'=')
        print (' ')
        
    domain.sww_merge(delete_old=True)

    anuga.finalize()

