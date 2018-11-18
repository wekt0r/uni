function Tree(left, right, value) {
	return {
		left: left,
		right: right,
		value: value
	}
}

//let's make tree  '+'
//		  /   \ 
//		 2     '*'
//		      /   \
//		    '+'    10
//		   /   \
//		  3     4
//
_3 = Tree(null, null, 3)
_4 = Tree(null, null, 4)
_10 = Tree(null, null, 10)
plus = Tree(_3, _4, '+')
mult = Tree(plus, _10, '*')
_2 = Tree(null, null, 2)
rooot = Tree(_2, mult, '+')
console.log(rooot)

