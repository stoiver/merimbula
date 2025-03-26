""" discharge.py is a function to extract the discharge through the causeway area of lake merimbula, this is done by integrating the dot product of the normal vector and the momentum of the fluid at many interpolated points across the causeway

positive discharge is flowing into the lake and negative out of the lake

There is very little error checking, so just get it correct the first time

Also this will save a .csv file containing the discharge values"""





sww_filename='domain20070324.sww'

from Scientific.IO.NetCDF import NetCDFFile
from anuga.abstract_2d_finite_volumes.util import file_function
from Numeric import array, zeros, Float, alltrue, concatenate, reshape,dot
from pylab import ion,hold,plot,title, legend, xlabel, ylabel, savefig
from utilities.numerical_tools import norm,normal_vector

app_gloc=[[759209.625, 5912931.0],[759242.09999999998, 5912879.0]]
gauge_names=['land','caus']
gauge_locations={}

for ind,key in enumerate(gauge_names):
    gauge_locations[key]=app_gloc[ind]


def find_pair(arry, other_point):
    for i in xrange(len(arry)-1):
        if min(abs(arry[i]-other_point))<=0.1:
           return i

fid=NetCDFFile(sww_filename)
x=fid.variables['x'][:]
y=fid.variables['y'][:]
triangles = fid.variables['volumes'][:]
time=fid.variables['time'][:]
fid.close()
x = reshape(x, (len(x),1))
y = reshape(y, (len(y),1))
vertex_coordinates = concatenate((x,y), axis=1)

gauge_ind={}
new_gauge_locations={}

for key in gauge_names:
    gauge_ind[key]=find_pair(vertex_coordinates,gauge_locations[key])
    new_gauge_locations[key]=vertex_coordinates[gauge_ind[key]]

transect_vec=new_gauge_locations[gauge_names[0]]-new_gauge_locations[gauge_names[1]]
channel_width=norm(transect_vec)
norm_vec=normal_vector(transect_vec)
norm_vec=norm_vec/norm(norm_vec)

trans_norm=-transect_vec/norm(transect_vec)

strip_number=10
strip_width=channel_width/strip_number

trans_points=[]
for i in range(strip_number+1):
    trans_points.append((new_gauge_locations[gauge_names[0]]+i*strip_width*trans_norm).tolist())

f = file_function(sww_filename,
                  quantities=['xmomentum','ymomentum'],
                  interpolation_points=trans_points,
                  use_cache=True,
                  verbose=True)


integrand=zeros([len(time),len(trans_points)],Float)
for time_ind,t in enumerate(time):
    for gauge in range(strip_number+1):
        integrand[time_ind,gauge]=dot(f(t,point_id=gauge),norm_vec)

        
def quad(f,dw):
    n=len(f)
    return dw*((f[0]-f[n-1])/2+sum(f[1:n-2]))

out_file='discharge_'+sww_filename[:-4]+'.csv'
fid=open(out_file,'w')

discharge=[]
for time_ind,t in enumerate(time):
    dis_tmp=quad(integrand[time_ind,:],strip_width)
    discharge.append(dis_tmp)
    st="%.2f, %.2f\n" %(t,dis_tmp)
    fid.write(st)
    
fid.close()


dateconversion=(297-265)*24*60*60		# between the 22/09/2003 and 01/01/2003

timeconversion=60*60		#[hours]*[mins/hours]*[seconds/min] #conversion for gauge data


fid=open('Site04_discharge_tide_data.dat','r')
lines=fid.readlines()
fid.close()

measured_gauge_data=[]
measured_gauge_time=[]

for i, line in enumerate(lines):
    fields=line.split()
    measured_gauge_time.append(float(fields[0])*timeconversion+dateconversion)
    measured_gauge_data.append(float(fields[1]))



#plotting
ion()
hold(False)
plot(time,discharge,'-b',measured_gauge_time,measured_gauge_data,'-r')
title("Discharge over time")
xlabel('time(s)')
ylabel('discharge (m^3/s)')    
raw_input('Press any key to continue')
