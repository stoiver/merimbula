"""Validation study of Merimbula lake using Pyvolution.

   Copyright 2006
   Christopher Zoppou, Stephen Roberts
   Geoscience Australia, ANU
   
Specific methods pertaining to the 2D shallow water equation
are imported from shallow_water
for use with the generic finite volume framework

Conserved quantities are h, uh and vh stored as elements 0, 1 and 2 in the
numerical vector named conserved_quantities.

"""

#------------------------------
# Setup Path and import modules
import sys
from os import sep, path
sys.path.append('..'+sep+'pyvolution')

from shallow_water import Domain, Reflective_boundary, File_boundary,\
     Dirichlet_boundary, Wind_stress
from pmesh2domain import pmesh_to_domain_instance
from util import file_function, Polygon_function, read_polygon, inside_polygon
from Numeric import zeros, Float, asarray
from least_squares import Interpolation
import time


#-------
# Domain
filename = 'merimbula_10834_bridge_refined_bathymetry.tsh'
print 'Creating domain from', filename
domain = pmesh_to_domain_instance(filename, Domain)
print "Number of triangles = ", len(domain)

#------------------------------------------
# Reduction operation for get_vertex_values              
from util import mean
domain.reduction = mean 


#-----------------
# Scale weed zones

def weed_zone(points):
    #print points
    n = len(points)
    print n
    z = []
    for i in range(n):
    #print i
        z.append([0,0])
        z[i][0] = 755471.4 + (points[i][0] + 3250.)/1.125
        z[i][1] = 5910260.0 + (points[i][1] + 1337.)/1.12
    #print z
    return z

#-------------
# Set friction
#       Sand bed
w = 0.035
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
#weed_zoneall = weed_zone([[-2269,-1337],[1894,-1339],[1894,2946],[-2669,2946]])

#---------------------------------------
#       Read friction polygon boundaries
#weed_zone47 = weed_zone(read_polygon('weed_zone.047'))
#weed_zone2   = weed_zone(read_polygon('weed_zone.002'))
#weed_zone12  = weed_zone(read_polygon('weed_zone.012'))
#weed_zone35  = weed_zone(read_polygon('weed_zone.035'))
#weed_zone8   = weed_zone(read_polygon('weed_zone.008'))
#weed_zone10  = weed_zone(read_polygon('weed_zone.010'))
#weed_zone13  = weed_zone(read_polygon('weed_zone.013'))
#weed_zone15  = weed_zone(read_polygon('weed_zone.015'))
#weed_zone19  = weed_zone(read_polygon('weed_zone.019'))
#weed_zone18  = weed_zone(read_polygon('weed_zone.018'))
#weed_zone24  = weed_zone(read_polygon('weed_zone.024'))
#weed_zone26  = weed_zone(read_polygon('weed_zone.026'))
#weed_zone27  = weed_zone(read_polygon('weed_zone.027'))
#weed_zone32  = weed_zone(read_polygon('weed_zone.032'))
#weed_zone31  = weed_zone(read_polygon('weed_zone.031'))
#weed_zone33  = weed_zone(read_polygon('weed_zone.033'))
#weed_zone34  = weed_zone(read_polygon('weed_zone.034'))
#weed_zone36  = weed_zone(read_polygon('weed_zone.036'))
#weed_zone37  = weed_zone(read_polygon('weed_zone.037'))
#weed_zone38  = weed_zone(read_polygon('weed_zone.038'))
#weed_zone40  = weed_zone(read_polygon('weed_zone.040'))
#weed_zone41  = weed_zone(read_polygon('weed_zone.041'))
#weed_zone42  = weed_zone(read_polygon('weed_zone.042'))
#weed_zone43  = weed_zone(read_polygon('weed_zone.043'))
#weed_zone44  = weed_zone(read_polygon('weed_zone.044'))
#weed_zone45  = weed_zone(read_polygon('weed_zone.045'))
#weed_zone46  = weed_zone(read_polygon('weed_zone.046'))
#weed_zone1   = weed_zone(read_polygon('weed_zone.001'))
#weed_zone20  = weed_zone(read_polygon('weed_zone.020'))
#weed_zone21  = weed_zone(read_polygon('weed_zone.021'))
#weed_zone22  = weed_zone(read_polygon('weed_zone.022'))
#weed_zone23  = weed_zone(read_polygon('weed_zone.023'))
#weed_zone25  = weed_zone(read_polygon('weed_zone.025'))
#weed_zone16  = weed_zone(read_polygon('weed_zone.016'))
#weed_zone17  = weed_zone(read_polygon('weed_zone.017'))
#weed_zone3   = weed_zone(read_polygon('weed_zone.003'))
#weed_zone6   = weed_zone(read_polygon('weed_zone.006'))
#weed_zone7   = weed_zone(read_polygon('weed_zone.007'))
#weed_zone9   = weed_zone(read_polygon('weed_zone.009'))
#weed_zone4   = weed_zone(read_polygon('weed_zone.004'))
#weed_zone39  = weed_zone(read_polygon('weed_zone.039'))
#weed_zone28  = weed_zone(read_polygon('weed_zone.028'))
#weed_zone29  = weed_zone(read_polygon('weed_zone.029'))
#weed_zone30  = weed_zone(read_polygon('weed_zone.030'))
#weed_zone5   = weed_zone(read_polygon('weed_zone.005'))
#weed_zone11  = weed_zone(read_polygon('weed_zone.011'))
#weed_zone14  = weed_zone(read_polygon('weed_zone.014'))

#    (weed_zone15,  g), (weed_zone19, c), (weed_zone18, g), (weed_zone24, c), \
#      (weed_zone26,  r), (weed_zone27, g), (weed_zone32, c), (weed_zone31, g), \
#      (weed_zone33,  r), (weed_zone34, g), (weed_zone36, r), (weed_zone37, g), \
#      (weed_zone38,  g), (weed_zone40, r), (weed_zone41, b), (weed_zone42, r), \
#      (weed_zone43,  r), (weed_zone44, r), (weed_zone45, b), (weed_zone46, r), \
#      (weed_zone1,   w), (weed_zone20, w), (weed_zone21, w), (weed_zone22, w), \
#      (weed_zone23,  w), (weed_zone25, w), (weed_zone16, w), (weed_zone17, w), \
#      (weed_zone3,   w), (weed_zone6,  w), (weed_zone7,  w), (weed_zone9,  w), \
#      (weed_zone4,   b), (weed_zone39, b), (weed_zone28, r), (weed_zone29, b), \
#      (weed_zone30,  b), (weed_zone5,  b), (weed_zone11, b), (weed_zone14, b) ]))

domain.set_quantity('friction',0.01)
#--------------------
# Boundary conditions

#---------------------------------------
#   Tidal cycle recorded at Eden as open
filename = 'Eden_tide_Sept03.dat'
print 'Open sea boundary condition from ',filename
Bf = File_boundary(filename, domain)

#--------------------------------------
#   All other boundaries are reflective
Br = Reflective_boundary(domain)
domain.set_boundary({'exterior': Br, 'open': Bf})

#-----------
# Wind field
#   Format is time [DD/MM/YY hh:mm:ss], speed [m/s] direction (degrees)
filename = 'Merimbula_Weather_data_Sept03_m_per_s.dat'
print 'Wind field from ',filename
F = file_function(filename, domain)
domain.forcing_terms.append(Wind_stress(F))

#--------------------------------
# Initial water surface elevation
domain.set_quantity('stage', .0)
    
#----------------------------------------------------------
# Decide which quantities are to be stored at each timestep
domain.quantities_to_be_stored = ['stage', 'xmomentum', 'ymomentum']

#-------------------------------------
# Provide file name for storing output
domain.store = True     #Store for visualisation purposes
domain.format = 'sww'   #Native netcdf visualisation format
domain.filename = 'Merimbula_2003_60days_Manning_pt01'

#----------------------
# Set order of accuracy
domain.default_order = 1
domain.smooth = True
         
#---------
# Evolution
t0 = time.time()
yieldstep = 900
finaltime = 86400*60
for t in domain.evolve(yieldstep = yieldstep, finaltime = finaltime):
    domain.write_time()
    
print 'That took %.2f seconds' %(time.time()-t0)    
