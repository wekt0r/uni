var numbers = [...Array(10).keys()].map(n => n+1)
var filtered = numbers.filter(n => n % 2 === 0)
console.log(filtered)
