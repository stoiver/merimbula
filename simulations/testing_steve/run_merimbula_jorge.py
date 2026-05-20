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
multiproc=2

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
print(f"[{anuga.myid}] After distribute", flush=True)
anuga.barrier()
#-------------------------------
# Setup domain runtime parameters
#-------------------------------

domain.store = True    #Store for visualisation purposes
domain.smooth = False
domain.set_low_froude(1)
#domain.set_flow_algorithm('DE1')
domain.set_fixed_flux_timestep(0.1)
domain.set_flow_algorithm('DE_ader2')
print(f"[{anuga.myid}] After set_multiprocessor_mode", flush=True)
anuga.barrier()
if multiproc == 2:
   # NOTE: setting use_c_rk2_loop = False forces ANUGA to call back into
   # Python for every RK substep instead of running the whole yieldstep
   # inside one C call. ~30x slower, but we can now print per-substep
   # diagnostics to find where the run hangs.
   domain.use_c_rk2_loop = False


#domain.gpu.flop_counters_reset()
#domain.gpu.flop_counters_start_timer()



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

print(f"[{anuga.myid}] After file_function", flush=True)
anuga.barrier()

#Bt = Time_boundary(domain = domain, function = tide_function)
#Bt = Transmissive_momentum_set_stage_boundary(domain, function = tide_function)
Bt = anuga.Transmissive_n_momentum_zero_t_momentum_set_stage_boundary(domain, function = tide_function)

#--------------------------------------
#   All other boundaries are reflective
#--------------------------------------
Br = anuga.Reflective_boundary(domain)

domain.set_boundary({'exterior': Br, 'open': Bt})


domain.set_multiprocessor_mode(multiproc)

#-------------------------------
# Evolve
#-------------------------------
import time
t0 = time.time()
sec = 1.0
min = 60*sec
hr  = 60*min
day = 24*hr
yieldstep = 10*sec
finaltime = 120*min

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
    print ('#','Final time = ', finaltime)
    print ('#',60*'=')
    print (' ')
#===========================================================================
# Main Evolve Loop
#===========================================================================

CFL_DT_THRESHOLD = 1e-3   # warn if global min cell-dt drops below this
_dt_blowup_aborted = False

# ---------------------------------------------------------------------------
# Per-substep instrumentation. Wraps domain.evolve_one_rk2_step so we get
# one compact line per RK substep on every rank, BEFORE and AFTER the call.
# The "BEFORE" line is what survives a hang: if substep N's BEFORE prints
# but substep N's AFTER never does, the hang is inside that substep on
# whichever rank stopped printing.
# ---------------------------------------------------------------------------
import numpy as _np
_substep_idx = [0]
_substep_log_every = 1          # set higher to thin out logs
_substep_panic_dt = CFL_DT_THRESHOLD
_orig_evolve_one_rk2_step = domain.evolve_one_rk2_step

def _instrumented_evolve_one_rk2_step(yieldstep, finaltime):
    _substep_idx[0] += 1
    n = _substep_idx[0]

    if n % _substep_log_every == 0:
        print(f'[ss r{anuga.myid} #{n:>7} BEFORE] '
              f't={domain.get_time():.4f}s  dt_in={domain.timestep:.3e}',
              flush=True)

    _orig_evolve_one_rk2_step(yieldstep, finaltime)

    stage_c = domain.quantities['stage'].centroid_values
    xmom_c  = domain.quantities['xmomentum'].centroid_values
    ymom_c  = domain.quantities['ymomentum'].centroid_values
    nan_s = int((~_np.isfinite(stage_c)).sum())
    nan_u = int((~_np.isfinite(xmom_c)).sum())
    nan_v = int((~_np.isfinite(ymom_c)).sum())
    ms = float(_np.nanmax(domain.max_speed)) if domain.max_speed is not None else float('nan')

    if n % _substep_log_every == 0 or nan_s or nan_u or nan_v \
       or domain.timestep < _substep_panic_dt:
        print(f'[ss r{anuga.myid} #{n:>7}  AFTER] '
              f't={domain.get_time():.4f}s  dt_out={domain.timestep:.3e}  '
              f'max_speed={ms:.3f}  nan(s,u,v)=({nan_s},{nan_u},{nan_v})',
              flush=True)

        # If anything looks broken on this substep, dump full per-cell info.
        if nan_s or nan_u or nan_v or domain.timestep < _substep_panic_dt:
            domain.diagnose_timestep(threshold_dt=_substep_panic_dt,
                                     top_n=5, verbose=True)

domain.evolve_one_rk2_step = _instrumented_evolve_one_rk2_step
# ---------------------------------------------------------------------------

# Per-yieldstep wall-clock + substep tracking. These are reset by the
# evolve machinery each yieldstep, so we read them BEFORE doing anything
# that might mutate them.
_wall_prev = time.time()
_yield_iter = 0

for t in domain.evolve(yieldstep = yieldstep, finaltime = finaltime):
    _yield_iter += 1
    _wall_now = time.time()
    _wall_dt = _wall_now - _wall_prev
    _wall_prev = _wall_now

    # Snapshot per-yieldstep substep info BEFORE diagnose_timestep (which
    # is cheap but does an MPI reduce that we want to keep separate).
    nsteps        = domain.number_of_steps
    n_first_order = domain.number_of_first_order_steps
    rec_min_dt    = domain.recorded_min_timestep
    rec_max_dt    = domain.recorded_max_timestep

    # Heartbeat on EVERY rank, so a stalled rank is obvious. One line,
    # flushed immediately, includes iter / wall-clock / substep envelope.
    print(f'[hb r{anuga.myid} iter={_yield_iter:>5} t={t:.2f}s] '
          f'wall_dt={_wall_dt:6.2f}s  substeps={nsteps} '
          f'(1st_order={n_first_order})  '
          f'dt[min,max]=[{rec_min_dt:.3e},{rec_max_dt:.3e}]  '
          f'last_dt={domain.timestep:.3e}',
          flush=True)

    # CFL / NaN diagnostic — runs on ALL ranks (MPI-collective inside).
    diag = domain.diagnose_timestep(threshold_dt=CFL_DT_THRESHOLD,
                                    top_n=3,
                                    verbose=True)

    # Abort the evolve loop on every rank if anything has NaN'd, so we get
    # one clean stack of diagnostics rather than runaway garbage.
    global_nan_total = sum(diag['global_nan_counts'].values())
    if global_nan_total > 0 and not _dt_blowup_aborted:
        if anuga.myid == 0:
            print(f'[ABORT] NaN/inf detected at t={t:.3f}s '
                  f'(stage={diag["global_nan_counts"]["stage"]}, '
                  f'xmom={diag["global_nan_counts"]["xmomentum"]}, '
                  f'ymom={diag["global_nan_counts"]["ymomentum"]}). '
                  f'Stopping evolve.')
            sys.stdout.flush()
        _dt_blowup_aborted = True
        break

    # This only happens on processor that owns the triangle.
    if tid is not None:
        print (domain.timestepping_statistics(datetime = True))
        print (f'    Tide {tide_function(t)[0]:.3f}, Mid Boundary Stage {domain.get_quantity("stage").centroid_values[tid]:.3f} ')

        # Additional diagnostics for verification
        stage = domain.get_quantity("stage")
        xmom = domain.get_quantity("xmomentum")
        ymom = domain.get_quantity("ymomentum")

        stage_c = stage.centroid_values
        xmom_c = xmom.centroid_values
        ymom_c = ymom.centroid_values

        print(f'    Stage:  min={stage_c.min():.4f}, max={stage_c.max():.4f}, mean={stage_c.mean():.4f}')
        print(f'    Xmom:   min={xmom_c.min():.4f}, max={xmom_c.max():.4f}, mean={xmom_c.mean():.6f}')
        print(f'    Ymom:   min={ymom_c.min():.4f}, max={ymom_c.max():.4f}, mean={ymom_c.mean():.6f}')
        #print(f'    Volume: {domain.get_water_volume():.2f} m³')
        if multiproc == 2:
            print(f'    C RK2 loop: {domain.use_c_rk2_loop}')
            # Diagnostic: verify sync is working
            stage_before = domain.get_quantity("stage").centroid_values[tid]
            domain.gpu_interface.sync_from_device()
            stage_after = domain.get_quantity("stage").centroid_values[tid]
            print(f'    [SYNC CHECK] Stage at tid before={stage_before:.4f}, after explicit sync={stage_after:.4f}')
        print()
        sys.stdout.flush()

anuga.barrier()

if anuga.myid == 0:
    print (f'That took {(time.time()-t0):.2f} seconds on {anuga.numprocs} MPI processes and {num_threads} OPENMP threads')


anuga.barrier()

#domain.gpu.flop_counters_stop_timer()
#domain.gpu.flop_counters_print_global()


if anuga.numprocs > 1:

    if anuga.myid == 0:
        print (' ')
        print ('#',60*'=')
        print ('#','Merging partitioned sww files')
        print ('#',60*'=')
        print (' ')
        
    domain.sww_merge(delete_old=True)

    anuga.finalize()

