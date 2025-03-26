"""
Main meribula script using new interface
"""
#%%
#-------------------------------
# Module imports
#-------------------------------
import sys, os, anuga
import numpy as np
import project





#-------------------------------
# Domain
#-------------------------------
print ('Creating domain from', project.mesh_filename)

domain = anuga.Domain(project.mesh_filename)

domain.check_integrity()
print ('Number of triangles = ', len(domain))
print ('The extent is ', domain.get_extent())

#-------------------------------
# Initial Conditions
#-------------------------------
print ('Initial values')

domain.set_quantity('elevation',
                    filename = project.bathymetry_filename[:-4] + '.xya',
                    alpha = 10.0,
                    verbose = True,
                    use_cache = True)

domain.set_quantity('stage', 0.0)

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
weed_zone47 = image_points_to_northing_eastings(read_polygon('weed_zone.047',split=' '))
weed_zone2   = image_points_to_northing_eastings(read_polygon('weed_zone.002',split=' '))
weed_zone12  = image_points_to_northing_eastings(read_polygon('weed_zone.012',split=' '))
weed_zone35  = image_points_to_northing_eastings(read_polygon('weed_zone.035',split=' '))
weed_zone8   = image_points_to_northing_eastings(read_polygon('weed_zone.008',split=' '))
weed_zone10  = image_points_to_northing_eastings(read_polygon('weed_zone.010',split=' '))
weed_zone13  = image_points_to_northing_eastings(read_polygon('weed_zone.013',split=' '))
weed_zone15  = image_points_to_northing_eastings(read_polygon('weed_zone.015',split=' '))
weed_zone19  = image_points_to_northing_eastings(read_polygon('weed_zone.019',split=' '))
weed_zone18  = image_points_to_northing_eastings(read_polygon('weed_zone.018',split=' '))
weed_zone24  = image_points_to_northing_eastings(read_polygon('weed_zone.024',split=' '))
weed_zone26  = image_points_to_northing_eastings(read_polygon('weed_zone.026',split=' '))
weed_zone27  = image_points_to_northing_eastings(read_polygon('weed_zone.027',split=' '))
weed_zone32  = image_points_to_northing_eastings(read_polygon('weed_zone.032',split=' '))
weed_zone31  = image_points_to_northing_eastings(read_polygon('weed_zone.031',split=' '))
weed_zone33  = image_points_to_northing_eastings(read_polygon('weed_zone.033',split=' '))
weed_zone34  = image_points_to_northing_eastings(read_polygon('weed_zone.034',split=' '))
weed_zone36  = image_points_to_northing_eastings(read_polygon('weed_zone.036',split=' '))
weed_zone37  = image_points_to_northing_eastings(read_polygon('weed_zone.037',split=' '))
weed_zone38  = image_points_to_northing_eastings(read_polygon('weed_zone.038',split=' '))
weed_zone40  = image_points_to_northing_eastings(read_polygon('weed_zone.040',split=' '))
weed_zone41  = image_points_to_northing_eastings(read_polygon('weed_zone.041',split=' '))
weed_zone42  = image_points_to_northing_eastings(read_polygon('weed_zone.042',split=' '))
weed_zone43  = image_points_to_northing_eastings(read_polygon('weed_zone.043',split=' '))
weed_zone44  = image_points_to_northing_eastings(read_polygon('weed_zone.044',split=' '))
weed_zone45  = image_points_to_northing_eastings(read_polygon('weed_zone.045',split=' '))
weed_zone46  = image_points_to_northing_eastings(read_polygon('weed_zone.046',split=' '))
weed_zone1   = image_points_to_northing_eastings(read_polygon('weed_zone.001',split=' '))
weed_zone20  = image_points_to_northing_eastings(read_polygon('weed_zone.020',split=' '))
weed_zone21  = image_points_to_northing_eastings(read_polygon('weed_zone.021',split=' '))
weed_zone22  = image_points_to_northing_eastings(read_polygon('weed_zone.022',split=' '))
weed_zone23  = image_points_to_northing_eastings(read_polygon('weed_zone.023',split=' '))
weed_zone25  = image_points_to_northing_eastings(read_polygon('weed_zone.025',split=' '))
weed_zone16  = image_points_to_northing_eastings(read_polygon('weed_zone.016',split=' '))
weed_zone17  = image_points_to_northing_eastings(read_polygon('weed_zone.017',split=' '))
weed_zone3   = image_points_to_northing_eastings(read_polygon('weed_zone.003',split=' '))
weed_zone6   = image_points_to_northing_eastings(read_polygon('weed_zone.006',split=' '))
weed_zone7   = image_points_to_northing_eastings(read_polygon('weed_zone.007',split=' '))
weed_zone9   = image_points_to_northing_eastings(read_polygon('weed_zone.009',split=' '))
weed_zone4   = image_points_to_northing_eastings(read_polygon('weed_zone.004',split=' '))
weed_zone39  = image_points_to_northing_eastings(read_polygon('weed_zone.039',split=' '))
weed_zone28  = image_points_to_northing_eastings(read_polygon('weed_zone.028',split=' '))
weed_zone29  = image_points_to_northing_eastings(read_polygon('weed_zone.029',split=' '))
weed_zone30  = image_points_to_northing_eastings(read_polygon('weed_zone.030',split=' '))
weed_zone5   = image_points_to_northing_eastings(read_polygon('weed_zone.005',split=' '))
weed_zone11  = image_points_to_northing_eastings(read_polygon('weed_zone.011',split=' '))
weed_zone14  = image_points_to_northing_eastings(read_polygon('weed_zone.014',split=' '))

domain.set_quantity('friction',Polygon_function([  \
    (weed_zone15,  g), (weed_zone19, c), (weed_zone18, g), (weed_zone24, c), \
      (weed_zone26,  r), (weed_zone27, g), (weed_zone32, c), (weed_zone31, g), \
      (weed_zone33,  r), (weed_zone34, g), (weed_zone36, r), (weed_zone37, g), \
      (weed_zone38,  g), (weed_zone40, r), (weed_zone41, b), (weed_zone42, r), \
      (weed_zone43,  r), (weed_zone44, r), (weed_zone45, b), (weed_zone46, r), \
      (weed_zone1,   w), (weed_zone20, w), (weed_zone21, w), (weed_zone22, w), \
      (weed_zone23,  w), (weed_zone25, w), (weed_zone16, w), (weed_zone17, w), \
      (weed_zone3,   w), (weed_zone6,  w), (weed_zone7,  w), (weed_zone9,  w), \
      (weed_zone4,   b), (weed_zone39, b), (weed_zone28, r), (weed_zone29, b), \
      (weed_zone30,  b), (weed_zone5,  b), (weed_zone11, b), (weed_zone14, b) ]))


#---------------------------------------------
# Wind field
# Format is time [DD/MM/YY hh:mm:ss], speed [m/s] direction (degrees)
# This method is linearly interpolating the bearings and so will lead to
# close to bearing = 0 and 360!
#---------------------------------------------
#filename = project.original_wind_filename[:-4]+'.tms'
#print 'Wind field from ',filename
#wind = file_function(filename, domain=domain, quantities=['speed','bearing'])
#domain.forcing_terms.append(Wind_stress(wind))



#-------------------------------
# Boundary conditions
#-------------------------------
print ('Boundaries')

#   Tidal cycle recorded at Eden as open
print ('Open sea boundary condition from ',project.boundary_filename)

tide_function = anuga.file_function(project.boundary_filename[:-4] + '.tms', domain,
                         verbose = True)
Bts = Transmissive_Momentum_Set_Stage_boundary(domain, tide_function)

#   All other boundaries are reflective
Br = Reflective_boundary(domain)

domain.set_boundary({'exterior': Br, 'open': Bts})

#-------------------------------
# Setup domain runtime parameters
#-------------------------------

base = os.path.basename(sys.argv[0])
domain.filename, _ = os.path.splitext(base)

#-------------------------------
# Evolve
#-------------------------------
import time
t0 = time.time()
yieldstep = 10
finaltime = 60


for t in domain.evolve(yieldstep = yieldstep, finaltime = finaltime):
    domain.write_time()

print ('That took %.2f seconds' %(time.time()-t0))

# %%
