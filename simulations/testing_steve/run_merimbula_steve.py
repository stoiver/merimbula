"""
Main meribula script using new interface
"""

#-------------------------------
# Module imports
#-------------------------------
import sys, os
import anuga
import project_steve as project

#-------------------------------
# Domain
#-------------------------------
print ('Creating domain from', project.mesh_filename)

domain = anuga.pmesh_to_domain_instance(project.mesh_filename, anuga.Domain, use_cache=True)

domain.check_integrity()


print ('Number of triangles = ', len(domain))
print ('The extent is ', domain.get_extent())

print ('stats')
print (domain.statistics())

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


# dredge out the canal

##canal_polygon = [[759222.474012,5912903.796898],
##           [759191.946009,5912861.297128],
##           [759224.269777,5912866.684423],
##           [759242.100000,5912879.000000],
##           [759252.700000,5912892.000000],
##           [759256.593546,5912915.170076],
##           [759242.826015,5912939.113609],
##           [759228.000000,5912954.000000],
##           [759209.600000,5912931.000000],
##           [759193.800000,5912906.000000],
##           [759170.000000,5912890.000000]]
##
##domain.set_quantity('elevation',numeric = -4.0,
##                    polygon = canal_polygon,
##                    smooth = True,
##                    verbose = True,
##                    use_cache = True)



#domain.set_quantity('elevation',expression='elevation +%f' %elevation_offset)
domain.set_quantity('friction', 0.0)
domain.set_quantity('stage', 0.0)

#-------------------------------
# Boundary conditions
#-------------------------------
print ('Boundaries')

#----------------------------------------
#   Tidal cycle recorded at Eden as open
#----------------------------------------
print ('Open sea boundary condition from ',project.boundary_filename)



tide_function = anuga.file_function(project.boundary_filename[:-4] + '.tms', domain,
                         verbose = True)



#Bt = Time_boundary(domain = domain, function = tide_function)
#Bt = Transmissive_momentum_set_stage_boundary(domain, function = tide_function)
Bt = anuga.Transmissive_n_momentum_zero_t_momentum_set_stage_boundary(domain, function = tide_function)

#--------------------------------------
#   All other boundaries are reflective
#--------------------------------------
Br = anuga.Reflective_boundary(domain)

domain.set_boundary({'exterior': Br, 'open': Bt})

#-------------------------------
# Setup domain runtime parameters
#-------------------------------
domain.set_name(project.simulation_name)
domain.store = True    #Store for visualisation purposes
domain.smooth = False

#-------------------------------
# Evolve
#-------------------------------
import time
t0 = time.time()
sec = 1.0
min = 60*sec
hr  = 60*min
yieldstep = 1*min
finaltime = 24*hr


for t in domain.evolve(yieldstep = yieldstep, finaltime = finaltime):
    domain.write_time()
    print (tide_function(domain.get_time())[0],' ',domain.get_conserved_quantities(9433, edge=0)[0])


print ('That took %.2f seconds' %(time.time()-t0))
