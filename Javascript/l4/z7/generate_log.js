const fs = require('fs')

const IPs = ['192.168.1.10', '192.168.1.13', '192.168.1.15', '192.168.0.7', '192.168.0.3', '8.8.8.8', '192.168.1.20']

const REQUESTS = ['POST', 'PUT', 'GET']

const SOME_DIRS = ['here', 'are', 'index', 'dirs']

const CODES = [200, 201, 202, 404]

function randint(a,b){
	return a + Math.floor(Math.random()*(b-a))
}

function random_choice(list){
	return list[randint(0, list.length)]
}

function generate_line(){
	time = `${randint(0,24)}:${randint(10,60)}:${randint(10,60)}`
	ip = random_choice(IPs)
	request = random_choice(REQUESTS)
	endpoint = `/${random_choice(SOME_DIRS)}/${random_choice(SOME_DIRS)}`
	return `${time} ${ip} ${request} ${endpoint} ${random_choice(CODES)}\n`
}
var stream = fs.createWriteStream('log.txt', {flags: 'a'});

function write_to_log(e){
	console.log(e)
	stream.write(generate_line())
}

[...Array(10**6).keys()].forEach(write_to_log)
// ofc codes won't match requests
// appendFile opens to many files (creates too many handlers) 
//
// streams are closed by default

