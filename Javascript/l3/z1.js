var obj = {
	field : 10,
	method : function(){
		return obj.field + 1
	},

	get value(){
		return obj.field
	},
	set value(i){
		obj.field = i
	}
};

// merging two objects can be made by var obj3 = {...obj1, ...obj2}
console.log(obj.method());
obj.value = 100;
console.log(obj.value);
// define field
Object.defineProperty(obj, "field2", {value: 20} );
// define method
Object.defineProperty(obj, "method2", {value: () => obj.field2*3.14});

// define getter and setter
Object.defineProperty(obj, "value2", {get : function () { 
						return obj.field2;
					    },
				      set : function (x){ 
					        obj.field2 = x*11; 
				      	    }
                                      });

console.log(obj.field2);
console.log(obj.method2());
console.log(obj.value2);
obj.value2 = 7;
console.log(obj.value2);

// Które mogą? -- wszystkie, no ale nie na raz - nie da rady dopisać jednocześnie value do getter i setter
//
// da się też wszystkie dodać normalnie po prostu definiując obiekt albo korzystając ze składni
// let merged = {...obj1, ...obj2}
