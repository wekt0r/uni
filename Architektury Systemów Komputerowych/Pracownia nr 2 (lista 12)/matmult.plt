set terminal png
plot "matmult.dat" using 1:2 title "multiply0" with linespoints, \
"matmult.dat" using 1:3 title "multiply1" with linespoints,\
"matmult.dat" using 1:4 title "multiply2" with linespoints,\
"matmult.dat" using 1:5 title "multiply3" with linespoints
