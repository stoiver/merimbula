"""Common filenames for Merimbula simulation
"""
import anuga

from datetime import datetime

now = datetime.now() # current date and time

date_time = now.strftime("%Y%m%d_%H%M%S")

print("date and time:",date_time)

model_dir = '../../model_data_sept_2003'
mesh_dir  = '../../meshes'

original_boundary_filename = anuga.join(model_dir,'Eden_tide_Sept03.dat')
original_wind_filename     = anuga.join(model_dir,'merimbula_wind_sept_2003.dat')
boundary_filename          = anuga.join(model_dir,'Eden_tide_Sept03.tms')
gauge_filename             = anuga.join(model_dir,'gauge_locations.csv')

bathymetry_filename        = anuga.join(mesh_dir,'merimbula_bathymetry.xya')
mesh_filename              = anuga.join(mesh_dir,'merimbula_10785.tsh')

depth_canal = 4
simulation_name            = f'domain_10785_canal_{depth_canal}_{date_time}'
