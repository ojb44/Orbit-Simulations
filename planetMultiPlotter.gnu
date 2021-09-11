set size ratio -1;
set size square;
set xrange[-1.5:1.5]
set yrange[-1.5:1.5]
plot 'mercury.dat' u 2:3 with l title 'No impulse', 'earth.dat' u 2:3 with l title 'Radial in', 'mars.dat' u 2:3 with l title 'Parallel to velocity', 'venus.dat' u 2:3 with l title 'Radial out', 'jupiter.dat' u 2:3 with l title 'Antiparallel to velocity'
