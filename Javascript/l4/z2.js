var Tree = function (left, right, value) {
	this.left = left,
	this.right = right,
	this.value = value
}
Tree.prototype[Symbol.iterator] = function* (){
	yield this.value
	if (this.left != null){
		yield* this.left
	}
	if (this.right != null){
		yield* this.right
	}
};

_3 = new Tree(null, null, 3)
_4 = new Tree(null, null, 4)
_10 = new Tree(null, null, 10)
plus = new Tree(_3, _4, '+')
mult = new Tree(plus, _10, '*')
_2 = new Tree(null, null, 2)
rooot = new Tree(_2, mult, '+')
console.log(Object.getPrototypeOf(rooot))

for (var e of rooot){
	console.log(e)
}

