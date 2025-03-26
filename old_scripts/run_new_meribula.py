"""
Main meribula script using new interface
"""

#-------------------------------
# Module imports
#-------------------------------
import sys, os
from anuga.shallow_water import Domain, Reflective_boundary,\
     File_boundary, Transmissive_Momentum_Set_Stage_boundary
from anuga.abstract_2d_finite_volumes.mesh_factory import rectangular_cross
from anuga.abstract_2d_finite_volumes.pmesh2domain import pmesh_to_domain_instance
from numpy import array, zeros, float, allclose
import project
from anuga.caching import cache




#-------------------------------
# Domain
#-------------------------------
print 'Creating domain from', project.mesh_filename

## domain = cache(pmesh_to_domain_instance,
##                (project.mesh_filename, Domain),
##                dependencies = [project.mesh_filename])

domain = pmesh_to_domain_instance(project.mesh_filename, Domain, use_cache=True)

domain.check_integrity()
print 'Number of triangles = ', len(domain)
print 'The extent is ', domain.get_extent()



#-------------------------------
# Initial Conditions
#-------------------------------

#elevation_offset=0.1

print 'Initial values'
bathymetry_filename =  project.bathymetry_filename[:-4] + '.xya'

domain.set_quantity('elevation',
                    filename = bathymetry_filename,
                    alpha = 2.0,
                    verbose = False,
                    use_cache = True)

#domain.set_quantity('elevation',expression='elevation +%f' %elevation_offset)
domain.set_quantity('friction', 0.0)
domain.set_quantity('stage', 0.0)

#-------------------------------
# Boundary conditions
#-------------------------------
print 'Boundaries'

#   Tidal cycle recorded at Eden as open
print 'Open sea boundary condition from ',project.boundary_filename

from anuga.abstract_2d_finite_volumes.util import file_function

tide_function = file_function(project.boundary_filename[:-4] + '.tms', domain,
                         verbose = True)
Bts = Transmissive_Momentum_Set_Stage_boundary(domain, tide_function)

#===============================================================================
# from pylab import plot, show
# x = []
# y = []
# for t in range(0,24*65):
#    #print t*3600,tide_function(t*3600)
#     x.append(t*3600)
#     y.append(tide_function(t*3600)[0])
#    
# plot(x,y)
# show()    
#===============================================================================

#   All other boundaries are reflective
Br = Reflective_boundary(domain)

domain.set_boundary({'exterior': Br, 'open': Bts})

#-------------------------------
# Setup domain runtime parameters
#-------------------------------
base = os.path.basename(sys.argv[0])
domain.filename, _ = os.path.splitext(base)
domain.default_order = 2
domain.limit2007 = 1
domain.store = True    #Store for visualisation purposes
domain.beta_h = 0.0
domain.limit2007 = 1
domain.smooth = False


#-------------------------------
# Evolve
#-------------------------------
import time
t0 = time.time()
yieldstep = 60*60
finaltime = 3600*24*10



for t in domain.evolve(yieldstep = yieldstep, finaltime = finaltime):
    domain.write_time()


print 'That took %.2f seconds' %(time.time()-t0)
