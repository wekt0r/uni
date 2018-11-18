const fs = require('fs');
const readline = require('readline');
const FILEPATH = 'log.txt';

function parse_line(line){
	return line.split(" ")[1];
}

var counter = {}
var line_counter = 0

const rl = readline.createInterface({
	input: fs.createReadStream(FILEPATH),
});

rl.on('line', (input) => {
	line_counter += 1
	var ip = parse_line(input);
	counter[ip] = (counter[ip] + 1)||1
})

rl.on('close', (_) => {
	console.log(line_counter)
	console.log(counter)
		
	var most_visitors = Object.keys(counter).map((e) => [e, counter[e]])
	most_visitors.sort((a,b) => a[1] < b[1]) 
	
	console.log(most_visitors.slice(0,3))
})

