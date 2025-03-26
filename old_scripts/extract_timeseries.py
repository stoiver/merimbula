"""Read in tms file, interpolate at specified locations
"""

import sys
from os import sep
from anuga.caching import cache

sys.path.append('..'+sep+'..'+sep)

points = [[759205, 5912912],[760070, 5912979],[759306, 5913042],
          [759269, 5912751],[757799, 5910529],[757545, 5912703],
          [756507, 5913260]]

gauge_names = ['unknown', 'Mitchies Beach', 'Wharf', 'Lake Bridge', 'South-East',
               'Lake Centre', 'North-West']


finaltime = 22.5
timestep = 0.05

#Read reference data

#gauges
reference_time = []
g1 = []
g2 = []
g3 = []
g4 = []
g5 = []
g6 = []
g7 = []

filename = 'gauge-heights.txt'
fid = open(filename)
lines = fid.readlines()
fid.close()
for i, line in enumerate(lines[1:]):
    if i == len(input_time): break

    fields = line.split()

    reference_time.append(float(fields[0]))

    ch5.append(float(fields[1]))
    ch7.append(float(fields[2]))
    ch9.append(float(fields[3]))


from pyvolution.util import file_function
from utilities.numerical_tools import ensure_numeric
gauge_values = [ensure_numeric(input_stage),
                ensure_numeric(ch5),
                ensure_numeric(ch7),
                ensure_numeric(ch9)] #Reference values



#Read model output
#filename = 'output.sww'
filename = 'lwru2.sww'

#f = file_function(filename,
#                  quantities = 'stage',
#                  interpolation_points = gauges,
#                  verbose = True)

f = cache(file_function,filename,
          {'quantities': 'stage',
           'interpolation_points': gauges,
           'verbose': True},
          #evaluate = True,
          dependencies = [filename],
          verbose = True)




#Checks
#print reference_time
#print input_time
assert reference_time[0] == 0.0
assert reference_time[-1] == finaltime
assert allclose(reference_time, input_time)



#Validation


for k, name in enumerate(gauge_names):
    sqsum = 0
    denom = 0
    model = []
    print 'Validating ' + name
    for i, t in enumerate(reference_time):
        ref = gauge_values[k][i]
        val = f(t, point_id = k)[0]
        model.append(val)

        sqsum += (ref - val)**2
        denom += ref**2

    print sqsum
    print sqsum/denom

    from pylab import *
    ion()
    hold(False)
    plot(reference_time, gauge_values[k], 'r.-',
         reference_time, model, 'k-')
    title('Gauge %s' %name)
    xlabel('time(s)')
    ylabel('stage (m)')
    legend(('Observed', 'Modelled'), shadow=True, loc='upper left')
    savefig(name, dpi = 300)

    raw_input('Next')
show()



#from pylab import *
#plot(time, stage)
#show()
