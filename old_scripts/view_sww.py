"""
View swww files
"""


#from pyvolution.data_manager import sww2domain
from anuga.shallow_water.data_manager import sww2domain
swwfilename=raw_input('Input sww filename:\n')

domain = sww2domain(swwfilename,very_verbose = True)

domain.visualise = True
domain.visualise_color_stage = True

domain.initialise_visualiser()

domain.visualiser.setup_all()
domain.visualiser.update_timer()



raw_input()
