function sum(...args){
	return args.reduce((acc, next) => acc + next)
}
console.log(sum(1,2,3))
console.log(sum(1,2,3,4,5))
