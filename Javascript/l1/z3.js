function get_primes(n){
    var composite = new Set();
    var primes = new Set();
    for (var i = 2; i <= n; i++){
        if (!composite.has(i)) {
            primes.add(i)
            for (j = 2*i; j <= n; j += i){
                composite.add(j)
            }
        }
    }
    return primes
}

console.log(get_primes(50))

//to debug - go to debug on left,
// set breakpoints by clicking red dot near number of line
// run and fn + f5 to continue
// enjoy