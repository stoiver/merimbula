from Scientific.IO.NetCDF import NetCDFFile
fid=NetCDFFile('domain20070324.sww')
x=fid.variables['x'][:]
y=fid.variables['y'][:]
from pylab import ion, hold, plot, title, legend, xlabel, ylabel, savefig
ion()
plot(x,y,'r+')
title('Why does this shit work???')
raw_input('Next')

