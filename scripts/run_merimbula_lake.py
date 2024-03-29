"""Validation study of Merimbula lake using Pyvolution.

   Copyright 2004
   Christopher Zoppou, Stephen Roberts, Ole Nielsen, Duncan Gray
   Geoscience Australia, ANU

Specific methods pertaining to the 2D shallow water equation
are imported from shallow_water
for use with the generic finite volume framework

Conserved quantities are h, uh and vh stored as elements 0, 1 and 2 in the
numerical vector named conserved_quantities.

Existence of file 'merimbula_10785_1.tsh' is assumed.
"""

#------------------------------
# Setup Path and import modules
import sys
from os import sep, path
sys.path.append('..'+sep+'pyvolution')

from anuga.shallow_water import Domain, Reflective_boundary, File_boundary,\
     Dirichlet_boundary, Wind_stress
from anuga.pmesh2domain import pmesh_to_domain_instance
from anuga.util import file_function, Polygon_function, read_polygon, inside_polygon
from Numeric import zeros, Float, asarray
from least_squares import Interpolation
import time


#-------
# Domain
filename = 'merimbula_10785_1.tsh'
print 'Creating domain from', filename
domain = pmesh_to_domain_instance(filename, Domain)
print "Number of triangles = ", len(domain)

#------------------------------------------
# Reduction operation for get_vertex_values
from util import mean
domain.reduction = mean


domain.set_quantity('friction',0.03)
#--------------------
# Boundary conditions

#---------------------------------------
#   Tidal cycle recorded at Eden as open
filename = 'Eden_tide_Sept03.tms'
print 'Open sea boundary condition from ',filename
Bf = File_boundary(filename, domain)

#--------------------------------------
#   All other boundaries are reflective
Br = Reflective_boundary(domain)
domain.set_boundary({'exterior': Br, 'open': Bf})

#-----------
# Wind field
#   Format is time [DD/MM/YY hh:mm:ss], speed [m/s] direction (degrees)
#filename = 'Merimbula_Weather_data_Sept03_m_per_s.dat'
#print 'Wind field from ',filename
#F = file_function(filename, domain)
#domain.forcing_terms.append(Wind_stress(F))

#--------------------------------
# Initial water surface elevation
domain.set_quantity('stage', -50.0)

#----------------------------------------------------------
# Decide which quantities are to be stored at each timestep
domain.quantities_to_be_stored = ['stage', 'xmomentum', 'ymomentum']

#-------------------------------------
# Provide file name for storing output
domain.store = True     #Store for visualisation purposes
domain.format = 'sww'   #Native netcdf visualisation format
from normalDate import ND
domain.filename = 'Merimbula_2003_4days_dry_%s'%ND()

print domain.filename

#----------------------
# Set order of accuracy
domain.default_order = 1
domain.smooth = True
print domain.use_inscribed_circle

#---------
# Evolution
t0 = time.time()
domain.visualise = False
yieldstep = 60
finaltime = 3600*24*3
for t in domain.evolve(yieldstep = yieldstep, finaltime = finaltime):
    domain.write_time()

print 'That took %.2f seconds' %(time.time()-t0)
