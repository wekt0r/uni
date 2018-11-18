function forEach( a, f ) {
   a.reduce((_, n) => f(n), [])
}
function map( a, f ) {
   return a.reduce((mapped, next) => mapped.concat([f(next)]), [])
}
function filter( a, f ) {
   return a.reduce((filtered, next) => filtered.concat(f(next)?[next]:[]), [])
}
var a = [1,2,3,4];
forEach( a, _ => { console.log( _ ); } );
// [1,2,3,4]
console.log( filter( a, _ => _ < 3 ));
// [1,2]
console.log(map( a, _ => _ * 2 ));
// [2,4,6,8]