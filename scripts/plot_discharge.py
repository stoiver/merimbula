try:
    from pylab import ion, hold, plot, title, legend, xlabel, ylabel, savefig
except:
    plotting = False
else:
    plotting = True

print 'Plotting is: ', plotting




csvfilename='discharge_domain.csv'

fid=open(csvfilename,'r')
lines=fid.readlines()
fid.close()

discharge_time=[]
discharge_data=[]

for i,line in enumerate(lines):
    fields=line.split()
    discharge_time.append(float(fields[0]))
    discharge_data.append(float(fields[1]))


fid=open('Site04_discharge_tide_data.dat')
lines=fid.readlines()
fid.close()

true_discharge_time=[]
true_discharge_data=[]

for i,line in enumerate(lines):
        fields=line.split()
        true_discharge_time.append(float(fields[0]))
        true_discharge_data.append(float(fields[1]))
                

if plotting:
    ion()
    hold(False)
    plot(discharge_time,discharge_data,'-b',true_discharge_time,true_discharge_data,'-r')
    raw_input("Press any key")
    
