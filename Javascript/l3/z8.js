function *fib(){
    var fib_0 = 0;
    var fib_1 = 1;
    while(true){
        yield fib_0

        res = fib_0
        fib_0 = fib_1
        fib_1 = res + fib_1
    }

}

function *take(_it, top){
    var counter = 0;
    for ( var _result; 
          _result = _it.next(), !_result.done, counter < top; 
          counter++) {
       yield _result.value;
   }
}


for (let num of take( fib(), 10 ) ) {
    console.log(num);
}