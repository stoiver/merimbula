from anuga.pmesh.mesh import *
from anuga.pmesh.mesh_interface import create_mesh_from_regions
from anuga.coordinate_transforms.geo_reference import Geo_reference
from anuga.geospatial_data import Geospatial_data
from anuga.config import netcdf_float

from Scientific.IO.NetCDF import NetCDFFile


def prepare_wind_stress(filename):
    """Converting wind timeseries to NetCDF tms file.
    This is a 'throw-away' code taylor made for files like
    'Benchmark_2_input.txt' from the LWRU2 benchmark
    """

    print 'Preparing wind timeseries %s' %filename
    from numpy import array, zeros, float, asarray
    
    fid = open(filename)

    #Skip first line
    #line = fid.readline()

    #Read remaining lines
    lines = fid.readlines()
    fid.close()


    N = len(lines)
    T = zeros(N, float)  #Time
    S = zeros(N, float)  #Speed
    B = zeros(N, float)  #Bearing

    Told = 0.0
    Sold = ' '
    Lold = ' '

    for i, line in enumerate(lines):
        fields = line.split()

        #print fields

        l_time = (fields[0]+' '+fields[1])[0:-1]
        from time import strptime, mktime

        s_time = strptime(l_time,'%d/%m/%y  %H:%M:%S')

        #print s_time

        T[i] = float(mktime(s_time))

        if i==0:
            Tstart = T[0]

        T[i] = T[i] - Tstart
        #this is specific to this data set. deals with daylight saving
#        if i>3270:
#            T[i] = T[i]+3600
#
        if T[i]<Told :
            print Lold
            print l_time
            print Sold
            print s_time
            print Told
            print T[i]
            print i, T[i]-Told

        S[i] = float(fields[2])
        B[i] = float(fields[3])

        Told = T[i]
        Sold = s_time
        Lold = l_time


    #print T
    #Create tms file
    from Scientific.IO.NetCDF import NetCDFFile

    outfile = filename[:-4] + '.tms'
    print 'Writing to', outfile
    fid = NetCDFFile(outfile, 'w')

    fid.institution = 'Australian National University'
    fid.description = 'Input wind for Merimbula'
    fid.starttime = 0.0
    fid.createDimension('number_of_timesteps', len(T))
    fid.createVariable('time', netcdf_float, ('number_of_timesteps',))
    fid.variables['time'][:] = T

    fid.createVariable('speed', netcdf_float, ('number_of_timesteps',))
    fid.variables['speed'][:] = S[:]

    fid.createVariable('bearing', netcdf_float, ('number_of_timesteps',))
    fid.variables['bearing'][:] = B[:]


    fid.close()


def prepare_timeboundary(filename):
    """Converting tide time series to NetCDF tms file.
    This is a 'throw-away' code taylor made for files like
    'Eden_tide_Sept03.dat' from the LWRU2 benchmark
    """

    print 'Preparing time boundary from %s' %filename
    from numpy import array, zeros, float, asarray

    fid = open(filename)

    #Skip first line
    #line = fid.readline()

    #Read remaining lines
    lines = fid.readlines()
    fid.close()


    N = len(lines)
    T = zeros(N, float)  #Time
    Q = zeros(N, float)  #Values

    Told = 0.0
    Sold = ' '
    Lold = ' '
    for i, line in enumerate(lines):
        fields = line.split()

        #print fields

        l_time = (fields[0]+' '+fields[1])[0:-1]
        from time import strptime, mktime

        s_time = strptime(l_time,'%d/%m/%y  %H:%M:%S')

        #print s_time

        T[i] = float(mktime(s_time))

        if i==0:
            Tstart = T[0]

        T[i] = T[i] - Tstart
        #strptime is too clever in that it adjusts for daylight savings!
        if i>3275:
            T[i] = T[i]+3600

        if T[i]<Told :
            print Lold
            print l_time
            print Sold
            print s_time
            print Told
            print T[i]
            print i, T[i]-Told

        Q[i] = float(fields[2])

        Told = T[i]
        Sold = s_time
        Lold = l_time


    #print T
    #Create tms file
    from Scientific.IO.NetCDF import NetCDFFile

    outfile = filename[:-4] + '.tms'
    print 'Writing to', outfile
    fid = NetCDFFile(outfile, 'w')

    fid.institution = 'Australian National University'
    fid.description = 'Input wave for Merimbula'
    fid.starttime = 0.0
    fid.createDimension('number_of_timesteps', len(T))
    fid.createVariable('time', netcdf_float, ('number_of_timesteps',))
    fid.variables['time'][:] = T

    fid.createVariable('stage', netcdf_float, ('number_of_timesteps',))
    fid.variables['stage'][:] = Q[:]

    fid.createVariable('xmomentum', netcdf_float, ('number_of_timesteps',))
    fid.variables['xmomentum'][:] = 0.0

    fid.createVariable('ymomentum', netcdf_float, ('number_of_timesteps',))
    fid.variables['ymomentum'][:] = 0.0

    fid.close()


def prepare_bathymetry(filename):
    """Convert benchmark 2 bathymetry to NetCDF pts file.
    This is a 'throw-away' code taylor made for files like
    'Benchmark_2_bathymetry.txt' from the LWRU2 benchmark
    """

    print 'Creating', filename
    
    # Read the ascii (.txt) version of this file,
    # make it comma separated and invert the bathymetry
    # (Below mean sea level should be negative)
    infile = open(filename[:-4] + '.xya')

    points = []
    attribute = []
    for line in infile.readlines()[1:]: #Skip first line (the header)
        fields = line.strip().split(',')

        x = float(fields[0])
        y = float(fields[1])
        z = float(fields[2]) # Bathymetry is inverted in original file
        
        points.append([x,y])
        attribute.append(z)
    infile.close()

    # Convert to geospatial data and store as NetCDF
    G = Geospatial_data(data_points=points,
                        attributes=attribute)
    G.export_points_file(filename)
    


#-------------------------------------------------------------
if __name__ == "__main__":
    import project
    print 'Prepare Open sea boundary condition from ',project.original_boundary_filename
    prepare_timeboundary(project.original_boundary_filename )


    print 'Prepare wind from ',project.original_wind_filename
    prepare_wind_stress(project.original_wind_filename )

    #Preparing points
    print 'Prepare bathymetry from xya file ',project.bathymetry_filename
    prepare_bathymetry(project.bathymetry_filename)


##    from anuga.shallow_water.data_manager import xya2pts
##    xya2pts(project.bathymetry_filename, verbose = True)


#    fit_to_mesh_file(mesh_file, point_file, mesh_output_file,
#                     alpha=DEFAULT_ALPHA, verbose= False,
#                     expand_search = False,
#                     data_origin = None,
#                     mesh_origin = None,
#                     precrop = False,
#                     display_errors = True):
