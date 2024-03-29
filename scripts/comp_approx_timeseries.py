"""Verify that the ANUGA simulation compares to the gauge levels recorded
   from a sww file and observed data extracted from 
   Site* data files 

   Written by: Piers Lawrence
   Enquiries: piers.lawrence@maths.anu.edu.au

   Input arguments: sww_filename [default=project.output_filename]
		   							 """


#-------------------------------------------------------------------------
#	Import relevent packages:
#-------------------------------------------------------------------------

from Numeric import allclose, argmin, argmax,array,resize
from Scientific.IO.NetCDF import NetCDFFile

from anuga.abstract_2d_finite_volumes.util import file_function
from anuga.utilities.numerical_tools import\
     ensure_numeric, cov, get_machine_precision

import project

#=========================================================================

#-------------------------------------------------------------------------
#	Make sure that plotting packages exist, if not then there will be 
#	no plots of gauge data against modelled data
#-------------------------------------------------------------------------
try:
    from pylab import ion, hold, plot, title, legend, xlabel, ylabel, savefig
except:
    plotting = False
else:
    plotting = True

print 'Plotting is: ', plotting
#=========================================================================

#-------------------------------------------------------------------------
#	Basic data and locations of gauges
#-------------------------------------------------------------------------

dateconversion=265		# between the 22/09/2003 and 01/01/2003

timeconversion=24*60*60		#[hours]*[mins/hours]*[seconds/min] #conversion for gauge data

gauge_locations = [[760375.1    ,  5912233.1]]	#boundary gauge data
gauge_locations += [[759205, 5912912],[760070, 5912979],[759306, 5913042],
          	   [759269, 5912751],[757799, 5910529],[757545, 5912703],
          	   [756507, 5913260]]

gauge_names = ['boundary','gauge_4','gauge_2','gauge_3','gauge_5','gauge_6','gauge_7','gauge_8']
filenames=['Site00tide','Site02tide','Site03tide','Site05tide','Site06tide','Site07tide','Site08tide']

#=========================================================================


#-------------------------------------------------------------------------
#	Initialize data structures
#-------------------------------------------------------------------------

validation_data = {}
for key in gauge_names:
    validation_data[key] = []

reference_times={}
for key in gauge_names:
    reference_times[key]=[]

gauge_filenames={}
gauge_filenames['boundary']=[]
for k, key in enumerate(gauge_names[1:]):
    gauge_filenames[key]=filenames[k]

#=========================================================================

#-------------------------------------------------------------------------
#	Read in reference data into data structures
#-------------------------------------------------------------------------

#	Boundary data:
print 'Reading in boundary data from: ', project.boundary_filename
fid = NetCDFFile(project.boundary_filename, 'r')
reference_times['boundary'] = fid.variables['time'][:]
validation_data['boundary'] = fid.variables['stage'][:]
fid.close()

#	Gauge data
for key in gauge_names[1:]:
    print 'Reading in gauge data for gauge:',key,'from file:',gauge_filenames[key]
    fid = open(gauge_filenames[key])
    lines = fid.readlines()
    fid.close()

    for i, line in enumerate(lines):

        fields = line.split()
        reference_times[key].append(float(fields[0]))
        validation_data[key].append(float(fields[1]))
       
for key in gauge_names:
    validation_data[key] = ensure_numeric(validation_data[key])

# This moves the first value of the data to the origin, so that they will match up
#	(but not really as it gets a bit messed up with the decimal day type data)
#	need to really check this out, what dates do we need???    
for key in gauge_names[1:]:
    reference_times[key]=array(reference_times[key])
    reference_times[key]=(reference_times[key]-dateconversion)*timeconversion

#=========================================================================

import sys
if len(sys.argv) > 1:
   sww_filename = sys.argv[1]
else:    
   sww_filename =  'domain20070324.sww' # project.output_filename

#sww_filename='domain20070324.sww'

def nearest_node_to_gauge_point(filename,quantity_names,gauge_locations):

    import time, calendar, types
    from anuga.config import time_format
    from Scientific.IO.NetCDF import NetCDFFile
    from Numeric import array, zeros, Float, alltrue, concatenate, reshape

    # Open NetCDF file
    fid = NetCDFFile(filename, 'r')


    # Get variables
    time = fid.variables['time'][:]    

    # Get time independent stuff
    # Get origin
    xllcorner = fid.xllcorner[0]
    yllcorner = fid.yllcorner[0]
    zone = fid.zone[0]        

    x = fid.variables['x'][:]
    y = fid.variables['y'][:]
    triangles = fid.variables['volumes'][:]

    x = reshape(x, (len(x),1))
    y = reshape(y, (len(y),1))
    vertex_coordinates = concatenate((x,y), axis=1) #m x 2 array

    for gauge in gauge_locations:
        
    
    quantities = {}
    for i, name in enumerate(quantity_names):
        quantities[name] = fid.variables[name][:]
    fid.close()



    
f = file_function(sww_filename,
                  quantities='stage',
                  interpolation_points=gauge_locations,
                  use_cache=True,
                  verbose=True)

finaltime=f.time[-1]	# to ensure that the times evaluated are consistent with the maximum modelled time

#=========================================================================

#--------------------------------------------------
# Compare model output to validation data
#--------------------------------------------------

eps = get_machine_precision()
for k, name in enumerate(gauge_names):
    sqsum = 0
    denom = 0
    model = []
    print 
    print 'Validating ' + name
    observed_timeseries = [] #validation_data[name]
    
    for i, t in enumerate(reference_times[name]):
	if t>=finaltime:break	#this is to make sure that the measured data comes within the modeled data.
        model.append(f(t, point_id=k)[0])
    	observed_timeseries.append(validation_data[name][i])
   
    # Resize original data so theat the data extracted from the model is not violated
    # and convert observed and modelled data to arrays 
    reference_times[name]=resize(reference_times[name],(len(model),))
    validation_data[name]=resize(validation_data[name],(len(model),))
    observed_timeseries=array(observed_timeseries)
    model=array(model)

    # Covariance measures    
    res = cov(observed_timeseries, model)     
    print 'Covariance = %.18e' %res

    # Difference measures    
    res = sum(abs(observed_timeseries-model))/len(model)     
    print 'Accumulated difference = %.18e' %res

    # Extrema
    res = abs(max(observed_timeseries)-max(model))
    print 'Difference in maxima = %.18e' %res

    
    res = abs(min(observed_timeseries)-min(model))
    print 'Difference in minima = %.18e' %res

    # Locations of extrema
    i0 = argmax(observed_timeseries)
    i1 = argmax(model)
    res = abs(reference_times[name][i1] - reference_times[name][i0])
    print 'Timelag between maxima = %.18e' %res
    

    i0 = argmin(observed_timeseries)
    i1 = argmin(model)
    res = abs(reference_times[name][i1] - reference_times[name][i0])
    print 'Timelag between minima = %.18e' %res




    if plotting is True:
        ion()
        hold(False)
    
        plot(reference_times[name], validation_data[name], 'r-',
             reference_times[name], model, 'k-')
        title('Gauge %s' %name)
        xlabel('time(s)')
        ylabel('stage (m)')    
        legend(('Observed', 'Modelled'), shadow=True, loc='upper left')
        savefig(name+'.eps', dpi = 300)
        #savefig(name, dpi = 300)        

	raw_input('Next')

