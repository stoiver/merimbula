from os import getcwd, sep, altsep, mkdir, access, F_OK
import project
from anuga.abstract_2d_finite_volumes.util import sww2timeseries


# nominate directory location of sww file with associated attribute
production_dirs = {'timeseries': 'gauge_timeseries'}



swwfiles = {}
for label_id in production_dirs.keys():
	file_loc = label_id + sep
	swwfile = file_loc + label_id + 'source.sww'
	swwfiles[swwfile] = label_id

texname, elev_output = sww2timeseries(swwfiles,
                                      project.gauge_filename,
                                      production_dirs,
                                      report = False,
                                      reportname = '',
                                      plot_quantity = ['stage', 'speed'],
				      generate_fig=True,
                                      surface = False,
                                      time_min = None,
                                      time_max = None,
                                      title_on = True,
				      verbose = True)
