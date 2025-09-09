"""
Main meribula script using new interface
"""

#-------------------------------
# Module imports
#-------------------------------
import sys, os

import pandas as pd
from scipy.interpolate import interp1d

import anuga
import project
from project import yieldstep, outputstep, duration

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

    print ('Number of triangles = ', len(domain))
    print ('The extent is ', domain.get_extent())


    #-------------------------------
    # Initial Conditions
    #-------------------------------

    #elevation_offset=0.1

    print ('Initial values')
    bathymetry_filename =  project.bathymetry_filename[:-4] + '.xya'

    print (bathymetry_filename)

    domain.set_quantity('elevation',
                        filename = bathymetry_filename,
                        alpha = 0.5,
                        verbose = True,
                        use_cache = True)

    #domain.set_quantity('elevation',expression='elevation +%f' %elevation_offset)
    #domain.set_quantity('friction', 0.01)
    domain.set_quantity('stage', 0.0)

else:
    domain = None

domain = anuga.distribute(domain)

#-------------------------------
# Setup domain runtime parameters
#-------------------------------

domain.store = True    #Store for visualisation purposes
domain.smooth = False
domain.set_low_froude(1)
domain.set_flow_algorithm('DE1')
try:
    domain.set_multiprocessor_mode(1)
except:
    pass


print (f'Stats for domain on rank {anuga.myid}')
print (domain.statistics())


#-------------------------------
# Setup Friction (due to weeds)
#-------------------------------
def image_points_to_northing_eastings(points):
    #print points
    n = len(points)

    z = []
    for i in range(n):
        #print i
        z.append([0,0])
        z[i][0] = 755471.4 + (points[i][0] + 3250.)/1.125
        z[i][1] = 5910260.0 + (points[i][1] + 1337.)/1.12

    return z

#------------------------------------------
# Set friction for different bed types
#------------------------------------------
#   Sand bed
w = 0.01
#   Saltmarsh
g = 0.060
#   Paddle weed
y = 0.025
#   Eel grass
r = 0.035
#   Mangroves
c = 0.065
#   Strap weed
b = 0.040


#-----------------------------------------------
#   Set the whole region to a constant value
#-----------------------------------------------
weed_zoneall = image_points_to_northing_eastings([[-2269,-1337],[1894,-1339],[1894,2946],[-2669,2946]])

#---------------------------------------
#       Read friction polygon boundaries
#---------------------------------------
# weed_zone47  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.047'),delimiter=' '))
# weed_zone2   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.002'),delimiter=' '))
# weed_zone12  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.012'),delimiter=' '))
# weed_zone35  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.035'),delimiter=' '))
# weed_zone8   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.008'),delimiter=' '))
# weed_zone10  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.010'),delimiter=' '))
# weed_zone13  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.013'),delimiter=' '))
# weed_zone15  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.015'),delimiter=' '))
# weed_zone19  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.019'),delimiter=' '))
# weed_zone18  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.018'),delimiter=' '))
# weed_zone24  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.024'),delimiter=' '))
# weed_zone26  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.026'),delimiter=' '))
# weed_zone27  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.027'),delimiter=' '))
# weed_zone32  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.032'),delimiter=' '))
# weed_zone31  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.031'),delimiter=' '))
# weed_zone33  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.033'),delimiter=' '))
# weed_zone34  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.034'),delimiter=' '))
# weed_zone36  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.036'),delimiter=' '))
# weed_zone37  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.037'),delimiter=' '))
# weed_zone38  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.038'),delimiter=' '))
# weed_zone40  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.040'),delimiter=' '))
# weed_zone41  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.041'),delimiter=' '))
# weed_zone42  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.042'),delimiter=' '))
# weed_zone43  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.043'),delimiter=' '))
# weed_zone44  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.044'),delimiter=' '))
# weed_zone45  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.045'),delimiter=' '))
# weed_zone46  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.046'),delimiter=' '))
# weed_zone1   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.001'),delimiter=' '))
# weed_zone20  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.020'),delimiter=' '))
# weed_zone21  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.021'),delimiter=' '))
# weed_zone22  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.022'),delimiter=' '))
# weed_zone23  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.023'),delimiter=' '))
# weed_zone25  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.025'),delimiter=' '))
# weed_zone16  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.016'),delimiter=' '))
# weed_zone17  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.017'),delimiter=' '))
# weed_zone3   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.003'),delimiter=' '))
# weed_zone6   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.006'),delimiter=' '))
# weed_zone7   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.007'),delimiter=' '))
# weed_zone9   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.009'),delimiter=' '))
# weed_zone4   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.004'),delimiter=' '))
# weed_zone39  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.039'),delimiter=' '))
# weed_zone28  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.028'),delimiter=' '))
# weed_zone29  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.029'),delimiter=' '))
# weed_zone30  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.030'),delimiter=' '))
# weed_zone5   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.005'),delimiter=' '))
# weed_zone11  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.011'),delimiter=' '))
# weed_zone14  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.014'),delimiter=' '))

# domain.set_quantity('friction',anuga.Polygon_function([  \
#     (weed_zone15,  g), (weed_zone19, c), (weed_zone18, g), (weed_zone24, c), \
#       (weed_zone26,  r), (weed_zone27, g), (weed_zone32, c), (weed_zone31, g), \
#       (weed_zone33,  r), (weed_zone34, g), (weed_zone36, r), (weed_zone37, g), \
#       (weed_zone38,  g), (weed_zone40, r), (weed_zone41, b), (weed_zone42, r), \
#       (weed_zone43,  r), (weed_zone44, r), (weed_zone45, b), (weed_zone46, r), \
#       (weed_zone1,   w), (weed_zone20, w), (weed_zone21, w), (weed_zone22, w), \
#       (weed_zone23,  w), (weed_zone25, w), (weed_zone16, w), (weed_zone17, w), \
#       (weed_zone3,   w), (weed_zone6,  w), (weed_zone7,  w), (weed_zone9,  w), \
#       (weed_zone4,   b), (weed_zone39, b), (weed_zone28, r), (weed_zone29, b), \
#       (weed_zone30,  b), (weed_zone5,  b), (weed_zone11, b), (weed_zone14, b) ]), location='centroids')



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

domain.set_quantity('elevation',numeric = -4.0,
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



#tide_function = anuga.file_function(project.boundary_filename[:-4] + '.tms', domain,
#                        verbose = False)




import numpy as np



#df = pd.read_csv(file_name, sep=r'[,\s]+', engine='python', names=['Date', 'Time', 'Stage', 'Xmom', 'Ymom'])
#df['DateTime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str), dayfirst=True, format='%d/%m/%y %H:%M:%S')
#df['timestamp'] = df['DateTime'].values.astype(np.int64) // 10**9


tide_df = pd.read_csv(project.boundary_filename)
tide_function = interp1d(tide_df['timestamp'], tide_df['Stage'], kind='linear', fill_value=0.0, bounds_error=False)



#Bt = Time_boundary(domain = domain, function = tide_function)
#Bt = Transmissive_momentum_set_stage_boundary(domain, function = tide_function)
Bt = anuga.Transmissive_n_momentum_zero_t_momentum_set_stage_boundary(domain, function = tide_function)

domain.set_starttime(tide_df['timestamp'].iloc[0])


#--------------------------------------
#   All other boundaries are reflective
#--------------------------------------
Br = anuga.Reflective_boundary(domain)

domain.set_boundary({'exterior': Br, 'open': Bt})



#-------------------------------
# Evolve
#-------------------------------
import time
t0 = time.time()


try:
    tid = domain.get_triangle_containing_point([ 760951.44544767, 5912173.85974667])
except:
    tid = None

print (f'Triangle id next to middle of tide: {tid}')
#print (domain.centroid_coordinates[9433])

anuga.barrier()


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

