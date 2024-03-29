""" Plotting file to plot boundary and gauge locations"""

import sys, os
import anuga

from pylab import plot, ion
import project

#-------------------------------
# Domain
#-------------------------------
print ('Creating domain from', project.mesh_filename)

#domain = pmesh_to_domain_instance(project.mesh_filename, Domain, use_cache=True)

domain = anuga.Domain(project.mesh_filename)
domain.check_integrity()
print ('Number of triangles = ', len(domain))
print ('The extent is ', domain.get_extent())

boundary=domain.get_boundary_polygon()


gauge_locations = [[760375.1    ,  5912233.1]]  #boundary gauge data
gauge_locations += [[759205, 5912912],[760070, 5912979],[759306, 5913042],
                   [759269, 5912751],[757799, 5910529],[757545, 5912703],
                   [756507, 5913260]]

g_x=[]
g_y=[]

for g_x_co,g_y_co in gauge_locations:
	g_x.append(g_x_co)
	g_y.append(g_y_co)



x=[]
y=[]

for x_co,y_co in boundary:
	x.append(x_co)
	y.append(y_co)

from netCDF4 import Dataset

#fid=Dataset('domain_piers2.sww','r')



import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import plot, savefig, xlabel, \
	ylabel, title, close, title, fill


#ion()
plot(x,y,'b-')
plot(g_x,g_y,'or')
#plot(fid.variables['x'][:],fid.variables['y'][:],'g+')

#raw_input('Press any key to close')

savefig('boundary_image')