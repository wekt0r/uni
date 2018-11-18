function createRangeGenerator(n){
    return function createGenerator() {
        var _state = 0;
        return {
            next : function() {
                return {
                    value : _state,
                    done : _state++ >= n
                }
            }
        }
    }
}

var foo = {
    [Symbol.iterator] : createRangeGenerator(10)
};
var foo1 = {
    [Symbol.iterator] : createRangeGenerator(20)
};

for ( var f of foo1 )
    console.log(f);