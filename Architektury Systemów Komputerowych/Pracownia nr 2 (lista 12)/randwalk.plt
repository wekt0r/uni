set terminal png
plot "randwalk.dat" using 1:2 title "bare" with linespoints, \
"randwalk.dat" using 1:3 title "optimized" with linespoints
