function memoize(fn) {
    var cache = {};
    return function(n) {
        if ( n in cache ) {
            return cache[n]
        } else {
            var result = fn(n);
            cache[n] = result;
            return result;
        }
    } 
}

function recursive_fib(n){
    if (n <= 1) 
        return n
    return recursive_fib(n-1) + recursive_fib(n-2)
}
var recursive_fib = memoize(recursive_fib)
//this does work since name recursive_fib used in function body is replaced by memoised version
//
//var memoized_fib_wrong = memoize(recursive_fib)
//This version won't work -- reason: calling fn(n) in line 11 e.g. fib(40) will make it recursively 2^40 calls (suuuper long) -- caching only value of f(40), not f(39) nor ... nor f(1)

function memoized_fib(n){
    memoized_fib.cache = memoized_fib.cache?memoized_fib.cache:{'0': 0, '1': 1}
    if (n in memoized_fib.cache)
        return memoized_fib.cache[n]
    memoized_fib.cache[n] = memoized_fib(n - 1) + memoized_fib(n-2)
    return memoized_fib.cache[n]
}

function iterative_fib(n){
    if (n <= 1)
        return n
    return [...Array(n-1).keys()].reduce((a,_) => [a[1], a[0] + a[1]], [0,1])[1]
}

function timer(func, arg){
    var timer_id = `${func.name.toString()}(${arg.toString()})`
    console.time(timer_id)
    func(arg)
    console.timeEnd(timer_id)
}

[...Array(30).keys()].forEach(n => {
    timer(recursive_fib, n + 10)
    timer(iterative_fib, n + 10)
    timer(memoized_fib,  n + 10)
    //timer(memoized_fib_wrong, n + 10)
});
