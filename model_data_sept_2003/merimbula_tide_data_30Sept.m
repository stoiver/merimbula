% Plot Merimbula tide data for 30 September 2004

clear all;

desc = {'Recorded Tide Data at Eden (Site 0), and Sites 2, 3, 5, 6, 7, 8',
        'Merimbula Lake',
        '30 Sept. through',
        '10 Nov. 2004'};
text(-400,350,desc)

date = '09-30-2004'

load Site00_30Sept04_tide.dat

x = Site00_30Sept04_tide(:,1)-274;
y = Site00_30Sept04_tide(:,2);

day = datenum(date)+datenum(x);
XTick = ([datenum('10/01/2004');datenum('10/10/2004');datenum('10/20/2004');...
        datenum('11/01/2004');datenum('11/10/2004')])

figure(1)
subplot(2,1,1), plot(day,y)
hold on
axis([datenum('09/30/2004') datenum('11/11/2004') -1.5 1.5])
set(gca,'XTick',XTick)
title('Site00 30Sept04 tide')

load Site02_30Sept04_tide.dat

x = Site02_30Sept04_tide(:,1)-274;
y = Site02_30Sept04_tide(:,2);

day = datenum(date)+datenum(x);
XTick = ([datenum('10/01/2004');datenum('10/10/2004');datenum('10/20/2004');...
        datenum('11/01/2004');datenum('11/10/2004')])

figure(2)
subplot(2,1,1), plot(day,y)
hold on
axis([datenum('09/30/2004') datenum('11/11/2004') -1.5 1.5])
set(gca,'XTick',XTick)
title('Site02 30Sept04 tide')


load Site03_30Sept04_tide.dat

x = Site03_30Sept04_tide(:,1)-274;
y = Site03_30Sept04_tide(:,2);

day = datenum(date)+datenum(x);
XTick = ([datenum('10/01/2004');datenum('10/10/2004');datenum('10/20/2004');...
        datenum('11/01/2004');datenum('11/10/2004')])

figure(3)
subplot(2,1,1), plot(day,y)
hold on
axis([datenum('09/30/2004') datenum('11/11/2004') -1.5 1.5])
set(gca,'XTick',XTick)
title('Site03 30Sept04 tide')


load Site05_30Sept04_tide.dat

x = Site05_30Sept04_tide(:,1)-274;
y = Site05_30Sept04_tide(:,2);

day = datenum(date)+datenum(x);
XTick = ([datenum('10/01/2004');datenum('10/10/2004');datenum('10/20/2004');...
        datenum('11/01/2004');datenum('11/10/2004')])

figure(5)
subplot(2,1,1), plot(day,y)
hold on
axis([datenum('09/30/2004') datenum('11/11/2004') -1.5 1.5])
set(gca,'XTick',XTick)
title('Site05 30Sept04 tide')


load Site06_30Sept04_tide.dat

x = Site06_30Sept04_tide(:,1)-274;
y = Site06_30Sept04_tide(:,2);

day = datenum(date)+datenum(x);
XTick = ([datenum('10/01/2004');datenum('10/10/2004');datenum('10/20/2004');...
        datenum('11/01/2004');datenum('11/10/2004')])

figure(6)
subplot(2,1,1), plot(day,y)
hold on
axis([datenum('09/30/2004') datenum('11/11/2004') -1.5 1.5])
set(gca,'XTick',XTick)
title('Site06 30Sept04 tide')


load Site07_30Sept04_tide.dat

x = Site07_30Sept04_tide(:,1)-274;
y = Site07_30Sept04_tide(:,2);

day = datenum(date)+datenum(x);
XTick = ([datenum('10/01/2004');datenum('10/10/2004');datenum('10/20/2004');...
        datenum('11/01/2004');datenum('11/10/2004')])

figure(7)
subplot(2,1,1), plot(day,y)
hold on
axis([datenum('09/30/2004') datenum('11/11/2004') -1.5 1.5])
set(gca,'XTick',XTick)
title('Site07 30Sept04 tide')


load Site08_30Sept04_tide.dat

x = Site08_30Sept04_tide(:,1)-274;
y = Site08_30Sept04_tide(:,2);

day = datenum(date)+datenum(x);
XTick = ([datenum('10/01/2004');datenum('10/10/2004');datenum('10/20/2004');...
        datenum('11/01/2004');datenum('11/10/2004')])

figure(8)
subplot(2,1,1), plot(day,y)
hold on
axis([datenum('09/30/2004') datenum('11/11/2004') -1.5 1.5])
set(gca,'XTick',XTick)
title('Site08 30Sept04 tide')


