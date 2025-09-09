% Plot Merimbula tide data

clear all;

desc = {'Recorded Tide Data at Eden (Site 0), and Sites 1, 2, 3, 4, 5, 6, 7',
        'Merimbula Lake',
        'Sept. through',
        'Nov. 2003'};
text(-400,350,desc)

date = '09-21-2003'

load Site00tide.txt

x = Site00tide(:,1)-265;
y = Site00tide(:,2);

day = datenum(date)+datenum(x);
XTick = ([datenum('10/01/2003');datenum('11/01/2003');datenum('12/01/2003')])

figure(1)
subplot(2,1,1), plot(day,y)
hold on
axis([datenum('09/23/2003') datenum('12/01/2003') -1.5 1.5])
set(gca,'XTick',XTick)
hold on

load Site02tide.txt

x = Site02tide(:,1)-265;
y = Site02tide(:,2);

day = datenum(date)+datenum(x);

figure(2)
subplot(2,1,1), plot(day,y)
hold on
axis([datenum('09/23/2003') datenum('12/01/2003') -1.5 1.5])
set(gca,'XTick',XTick)

load Site03tide.txt

x = Site03tide(:,1)-265;
y = Site03tide(:,2);

day = datenum(date)+datenum(x);

figure(3)
subplot(2,1,1), plot(day,y)
hold on
axis([datenum('09/23/2003') datenum('12/01/2003') -1.5 1.5])
set(gca,'XTick',XTick)

load Site05tide.txt

x = Site05tide(:,1)-265;
y = Site05tide(:,2);

day = datenum(date)+datenum(x);

figure(4)
subplot(2,1,1), plot(day,y)
hold on
axis([datenum('09/23/2003') datenum('12/01/2003') -1.5 1.5])
set(gca,'XTick',XTick)

load Site06tide.txt

x = Site06tide(:,1)-265;
y = Site06tide(:,2);

day = datenum(date)+datenum(x);

figure(5)
subplot(2,1,1), plot(day,y)
hold on
axis([datenum('09/23/2003') datenum('12/01/2003') -1.5 1.5])
set(gca,'XTick',XTick)

load Site05tide.txt

x = Site05tide(:,1)-265;
y = Site05tide(:,2);

day = datenum(date)+datenum(x);

figure(6)
subplot(2,1,1), plot(day,y)
hold on
axis([datenum('09/23/2003') datenum('12/01/2003') -1.5 1.5])
set(gca,'XTick',XTick)

load Site07tide.txt

x = Site07tide(:,1)-265;
y = Site07tide(:,2);

day = datenum(date)+datenum(x);

figure(7)
subplot(2,1,1), plot(day,y)
hold on
axis([datenum('09/23/2003') datenum('12/01/2003') -1.5 1.5])
set(gca,'XTick',XTick)

load Site08tide.txt

x = Site08tide(:,1)-265;
y = Site08tide(:,2);

day = datenum(date)+datenum(x);

figure(8)
subplot(2,1,1), plot(day,y)
axis([datenum('09/23/2003') datenum('12/01/2003') -1.5 1.5])
set(gca,'XTick',XTick)


