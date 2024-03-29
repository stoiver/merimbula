% Plot Merimbula weather data

clear all;

[number,date,time,temperature,speed,direction,pressure]=...
    textread('Merimbula_Weather_data.txt','%s %s %s %f %u %u %f');

n_segments = 24;
m = max(size(number));
figure(1)
direction_north = direction*pi/180.;
rose_north(direction_north,n_segments);
[tout,rout] = rose_north(direction_north,n_segments);
desc = {'Wind Direction at',
        'Merimbula Airport for ',
        'Sept. through',
        'Nov. 2003'};
text(-400,350,desc)

figure(2)
edges = 0:2*pi/n_segments:2*pi;
for i=1:n_segments
    start = edges(i);
    finish = edges(i+1);
    k(i) = 0;
    v_sum(i) = 0;
    yes = 0;
    no = 0;
    for j=1:m
       if direction_north(j) >= start & direction_north(j) < finish+eps*100
           v_sum(i) = v_sum(i) + speed(j);
           yes = yes + 1;
       else
           no = no + 1;
       end
    end
    if yes > 0
        v_mean(i) = v_sum(i)/yes;
    else
        v_mean(i) = 0;
    end
    direction_average(i) = (start+finish)/2;
end
[x,y] = pol2cart(direction_average+pi/4,v_mean);
compass(x,y)

figure(3)
day = datenum(date)+datenum(time);
plot(day,temperature)
axis([min(day) max(day) -5 35])

hold on
datetick('x',20)

figure(4)
plot(day,pressure)
axis([min(day) max(day) 985 1035])
hold on
datetick('x',20)

figure(5)
rain = ([0.2 0.0 0.0 0.0 0.0 0.0 0.0 0.2 0.0 0.0...
         2.0 0.0 0.2 0.0 1.0 0.0 0.0 0.0 0.0 0.4...
         0.6 0.2 0.0 0.8 0.0 0.0 2.0 0.0 0.0 0.0...
         0.0 6.0 3.0 0.2 0.0 17. 0.2 0.0 0.0 0.0...
         3.0 2.0 0.2 0.0 0.0 1.0 0.0 0.0 0.0 NaN...
         0.0 1.0 0.0 3.0 0.0 24. 0.2 0.0 5.0 0.0...
         0.0 1.0 0.2 0.0 0.0 0.0 NaN 0.0 0.2 0.0...
         0.0 0.0 0.0 0.0 NaN 0.0 23. 1.0 0.0 0.2...
         3.0 25. 27. 2.0 0.0 0.4 0.0 0.0 0.0 0.0]);

n = max(size(rain));
xx = 1:1:n;
days = day(1) + xx;
bar(days,rain,1)
axis([min(day) max(day) 0 30])
hold on
datetick('x',20)
