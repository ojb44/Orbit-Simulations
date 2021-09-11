set size ratio -1;
set size square;
set xrange[-1.5:1.5]
set yrange[-1.5:1.5]
plot 'planetOutput.dat' u 4:5 with l
plot 'mercury.dat' u 4:5 with l title 'No impulse', 'earth.dat' u 4:5 with l title 'Radial in', 'mars.dat' u 4:5 with l title 'Parallel to velocity', 'venus.dat' u 4:5 with l title 'Radial out', 'jupiter.dat' u 4:5 with l title 'Antiparallel to velocity'