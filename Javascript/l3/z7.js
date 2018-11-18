function fib_obj() {
    var _fib_0 = 0;
    var _fib_1 = 1;
    return {
        next : function() {
            var res = _fib_0
            _fib_0 = _fib_1
            _fib_1 = res + _fib_1
            return {
                value : res
            }
        }
    }
}

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
var fib_gen = {
    [Symbol.iterator] : fib_obj
};

//var _it = fib();
//   for ( var _result; _result = _it.next(), !_result.done; ) {
//       console.log( _result.value );
//   }

for ( var f of fib() )
    console.log(f);

//w obu przypadkach się da