"""Validation study of Merimbula lake using Pyvolution.

   Copyright 2004
   Christopher Zoppou, Stephen Roberts, Ole Nielsen, Duncan Gray
   Geoscience Australia, ANU
   
Specific methods pertaining to the 2D shallow water equation
are imported from shallow_water
for use with the generic finite volume framework

Conserved quantities are h, uh and vh stored as elements 0, 1 and 2 in the
numerical vector named conserved_quantities.

Existence of file 'merimbula_interpolated.tsh' is assumed.
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
from data_manager import sww2domain

import time

#-------
# Domain
# This is the original file used to create the SWW file from t = 0.
# It is also needed to define the domain if it contains boundaryies other that
# external.
filename = 'merimbula_10834_bridge_refined_bathymetry.tsh'
domain_old = pmesh_to_domain_instance(filename, Domain)

# The evolution starts from the last time step contained in the following file.
filename_sww = 'c:\grohm_output\Merimbula_2003_4days_dry.sww'
print 'Creating domain from', filename_sww
domain = sww2domain(filename_sww)
print "Number of triangles = ", len(domain)

# Extract old boundary data form original tsh file
domain.boundary = domain_old.boundary

#------------------------------------------
# Reduction operation for get_vertex_values              
from util import mean
domain.reduction = mean 

domain.set_quantity('friction',0.03)
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
# Initial water surface elevation: only required for initial run
# domain.set_quantity('stage', -50.0)
# All conserved values are retrieved from the SWW file
    
#----------------------------------------------------------
# Decide which quantities are to be stored at each timestep
domain.quantities_to_be_stored = ['stage', 'xmomentum', 'ymomentum']

#-------------------------------------
# Provide file name for storing output
domain.store = True     #Store for visualisation purposes
domain.format = 'sww'   #Native netcdf visualisation format
# Caution: Should not store results in the SWW file
filename = 'Merimbula_2003_4days_dry_plus'
domain.filename = (filename)
if filename_sww == filename:
    msg = 'SWW file name is the same as the output file name'
    raise msg

#----------------------
# Set order of accuracy
domain.default_order = 1
# Smooth in True or discontinuous triangles if False (Default is minimum for True)
domain.smooth = True
domain.reduction = 'mean'

# Use the inscribed circle with safety factor of 0.9 to establish the time step
# domain.set_to_inscribed_circle(safety_factor=0.9)

#---------
# Evolution
# t0 is the computer clock time
t0 = time.time()
yieldstep = 9

# domain.startime is obtained from the SWW file and is the last evolution time
# time_extra is the additional evolution time final evolution time
# is equal to desired_finaltime
time_extra = 90
desired_finaltime = domain.starttime + time_extra
finaltime = desired_finaltime - domain.starttime

for t in domain.evolve(yieldstep = yieldstep, finaltime = finaltime):
    domain.write_time()
    
print 'That took %.2f seconds' %(time.time()-t0)    
