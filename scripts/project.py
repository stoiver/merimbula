"""Common filenames for Merimbula simulation
"""

import anuga

model_dir = '../Model_Data_Sept_2003'
mesh_dir = '../Meshes'

original_boundary_filename = anuga.join(model_dir,'Eden_tide_Sept03.dat')
original_wind_filename = anuga.join(model_dir,'merimbula_wind_sept_2003.dat')
boundary_filename = anuga.join(model_dir,'Eden_tide_Sept03.tms')
gauge_filename=anuga.join(model_dir,'gauge_locations.csv')

bathymetry_filename = anuga.join(mesh_dir,'merimbula_bathymetry.xya')
mesh_filename = anuga.join(mesh_dir,'merimbula_10785.tsh')
#mesh_filename = 'merimbula_43200.tsh'


gauge_filename='gauge_locations.csv'

depth_canal = 4
simulation_name = 'domain_10785_canal_%i' % depth_canal

