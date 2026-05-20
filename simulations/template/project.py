"""Common filenames for Merimbula simulation
"""

import os

mesh_size = 10785
#mesh_size = 17156
#mesh_size = 19251
#mesh_size = 43200
#mesh_size = 86370
#mesh_size = 346671

model_date = 'sept_2003'
#model_date = 'sept_2004'

global_friction = 0.015
weeds = True
canal = False
depth_canal = 4

# domain simulation parameters
store = True
store_vertices_uniquely = True
low_froude = 1
flow_algorithm = 'DE_ader2' #'DE_ader2' #'DE1' # DE0
multiprocessor_mode = 1
cfl = 1.0


sec = 1.0
min = 60*sec
hr  = 60*min
day = 24*hr

# evolution of simulation parameters
yieldstep  = 1*min
outputstep = 30*min
duration   = 12*day #5*day

#----------------------------------------------------------------
# No need to edit below this line
#----------------------------------------------------------------
import anuga

simulation_dir = os.path.basename(os.path.abspath(os.path.dirname(__file__)))
print(f'Simulation directory: {simulation_dir}')

georef = anuga.Geo_reference(zone = 55,  hemisphere = 'southern')

from datetime import datetime
import os
now = datetime.now() # current date and time
date_time = now.strftime("%Y%m%d_%H%M%S")
print("date and time:",date_time)


model_dir = f'../../model_data_{model_date}'
mesh_dir  = '../../meshes'
weed_dir  = '../../weed_zones'


boundary_filename          = anuga.join(model_dir,'boundary.csv')
gauge_filename             = anuga.join(model_dir,'gauge_locations.csv')

bathymetry_filename        = anuga.join(mesh_dir,'merimbula_bathymetry.xya')
mesh_filename              = anuga.join(mesh_dir,f'merimbula_{mesh_size}.tsh')

if weeds:
    simulation_name            = f'{simulation_dir}_{model_date}_{mesh_size}_weeds_{date_time}'
else:
    simulation_name            = f'{simulation_dir}_{model_date}_{mesh_size}_no_weeds_{date_time}'


