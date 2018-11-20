function recursive_fib(n){
    if (n <= 1) 
        return n
    return recursive_fib(n-1) + recursive_fib(n-2)
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
});