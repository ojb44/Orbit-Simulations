set size ratio -1;
set size square;
plot 'planetOutput.dat' u 2:3:6 with l palette, 'planetOutput.dat' every 2000 u 2:3:4:5 w vector
