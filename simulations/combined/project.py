"""Common filenames for Merimbula simulation
"""

import os

#mesh_size = 10785
#mesh_size = 17156 # currently problem with these meshes 
mesh_size = 43200

model_date = 'sept_2003'
#model_date = 'sept_2004'

weeds = True
canal = True
depth_canal = 4

simulation_dir = os.path.dirname(os.path.abspath(__file__))

sec = 1.0
min = 60*sec
hr  = 60*min
day = 24*hr

yieldstep  = 10*sec
outputstep = 5*min
duration   = 5*day




#------------------------------------
# No need to edit below this line
#------------------------------------
import anuga

georef = anuga.Geo_reference(zone = 55,  hemisphere = 'southern')

from datetime import datetime
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


