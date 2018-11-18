function createFs(n) { // tworzy tablicę n funkcji
    var fs = []; // i-ta funkcja z tablicy ma zwrócić i
    for ( let i=0; i<n; i++ ) {
        fs[i] = function() { return i; };
    };
    return fs; 
}

function createFsVar(n) { // tworzy tablicę n funkcji
    var fs = []; // i-ta funkcja z tablicy ma zwrócić i
    for ( var i=0; i<n; i++ ) {
        fs[i] = (function () {var _i = i; return function (){ return _i; }})();
    };
    return fs; 
}

// var działa na całej funkcji
// let działa tylko na tym kawałku pętli (na {}), więc let i = 0 jest stworzony, zniszczony, let i = 1, ...
// a var i = 0, i = 1, i = 2, ... przy czym cały czas mamy referencję do zmiennej i 

//babel zmienia nazwę zmiennej w jej scopie (np. zamiast a jest _a)

var myfs = createFsVar(10);
console.log( myfs[0]() ); // zerowa funkcja miała zwrócić 0
console.log( myfs[2]() ); // druga miała zwrócić 2
console.log( myfs[7]() );
