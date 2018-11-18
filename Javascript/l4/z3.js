var Foo = (function() {
	var Qux = function(r){
		return 2*r*3.1415
	};

	return function(){

		this.Bar = function(d){
			return Qux(d/2)
		};
		
	}
})();


var foo = new Foo()
console.log(foo.Bar(10))
console.log(foo.Qux(5)) //should throw exception because Qux is not defined
