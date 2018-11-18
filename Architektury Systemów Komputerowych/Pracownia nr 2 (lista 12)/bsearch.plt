set terminal png
plot "bsearch.dat" using 1:2 title "bare" with linespoints, \
"bsearch.dat" using 1:3 title "optimized" with linespoints
