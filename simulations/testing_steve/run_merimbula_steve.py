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
    domain.set_quantity('friction', 0.01)
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




print (f'Stats for domain on rank {anuga.myid}')
print (domain.statistics())




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



tide_function = anuga.file_function(project.boundary_filename[:-4] + '.tms', domain,
                         verbose = False)



#Bt = Time_boundary(domain = domain, function = tide_function)
#Bt = Transmissive_momentum_set_stage_boundary(domain, function = tide_function)
Bt = anuga.Transmissive_n_momentum_zero_t_momentum_set_stage_boundary(domain, function = tide_function)

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
sec = 1.0
min = 60*sec
hr  = 60*min
day = 24*hr
yieldstep = 5*min
finaltime = 15*min

try:
    tid = domain.get_triangle_containing_point([ 760951.44544767, 5912173.85974667])
except:
    tid = None

print (f'Triangle id next to middle of tide: {tid}')
#print (domain.centroid_coordinates[9433])

anuga.barrier()

if anuga.myid == 0:
    print (' ')
    print ('#',60*'=')
    print ('#','Evolving domain')
    print ('#',60*'=')
    print ('#','Number of processors = ', anuga.numprocs)
    print ('#','Multiprocessor Mode = ', domain.multiprocessor_mode)
    print ('#','Yield step = ', yieldstep)
    print ('#','Final time = ', finaltime)
    print ('#',60*'=')
    print (' ')
#===========================================================================
# Main Evolve Loop
#===========================================================================

for t in domain.evolve(yieldstep = yieldstep, finaltime = finaltime):
        
    # This only happens on processor that owns the triangle.
    if tid is not None:
        print (domain.timestepping_statistics(datetime = True))
        print (f'    Tide {tide_function(t)[0]:.3f}, Mid Boundary Stage {domain.get_quantity("stage").centroid_values[tid]:.3f} ')
        sys.stdout.flush()

anuga.barrier()

if anuga.myid == 0:
    print (f'That took {(time.time()-t0):.2f} seconds on {anuga.numprocs} processors')


anuga.barrier()


if anuga.numprocs > 1:

    if anuga.myid == 0:
        print (' ')
        print ('#',60*'=')
        print ('#','Merging partitioned sww files')
        print ('#',60*'=')
        print (' ')
        
    #domain.sww_merge(delete_old=True)

anuga.finalize()

