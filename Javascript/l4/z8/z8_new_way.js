const prf = require('./z8_module')
// promisifed_read_files
//

// a -- my function returning promise
// b -- util.promisfy
// c -- fs.promises.readFile


async function main() {
	try {
		var data = await prf.read_file_a("./test.txt", 'utf-8')
		console.log('I have read it, yay!\n', data)
	}
	catch (err){
		console.log('Ooops! Error:', err)
	}

}

main()
