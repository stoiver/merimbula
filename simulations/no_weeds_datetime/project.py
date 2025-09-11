"""Common filenames for Merimbula simulation
"""
import anuga

from datetime import datetime

now = datetime.now() # current date and time

date_time = now.strftime("%Y%m%d_%H%M%S")

print("date and time:",date_time)

mesh_size = 10785
#mesh_size = 17156
#mesh_size = 43200

#model_date = 'sept_2003'
model_date = 'sept_2004'

weeds = False
depth_canal = 4

simulation_dir           = 'datetime'

model_dir = f'../../model_data_{model_date}'
mesh_dir  = '../../meshes'
weed_dir  = '../../weed_zones'


boundary_filename          = anuga.join(model_dir,'boundary.csv')
gauge_filename             = anuga.join(model_dir,'gauge_locations.csv')

bathymetry_filename        = anuga.join(mesh_dir,'merimbula_bathymetry.xya')

mesh_filename              = anuga.join(mesh_dir,f'merimbula_{mesh_size}.tsh')

simulation_name            = f'{simulation_dir}_{model_date}_{mesh_size}_{depth_canal}_{date_time}'

sec = 1.0
min = 60*sec
hr  = 60*min
day = 24*hr

yieldstep  = 5*min
outputstep = 15*min
duration   = 30*min
