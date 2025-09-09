% Plot Discharge at Site 04

clear all;

desc = {'Measured Discharge at Site 04',
        '25 October 2003'};
text(-400,350,desc)


load Site04_discharge_tide_data.dat

x = Site04_discharge_tide_data(:,1);
y = Site04_discharge_tide_data(:,2);

plot(x,y)
axis([ 8 22 -200 200])
title('Measured discharge Site04 25 October 2003')