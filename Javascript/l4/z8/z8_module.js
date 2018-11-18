const fs = require('fs');
const util = require('util');
const fs_promises = require('fs.promises')

//2 część:
//- ręcznie napisana funkcja fs::readFile z Promise
//- util.promisfy
//- fs.promises.readFile

function read_file_a(file_path, encoding='utf-8'){
	return new Promise( (resolve, reject) => {
		fs.readFile(file_path, encoding, (err, data) => {
			if (err) 
				reject(err); 
			
			resolve(data);
			})   
	} );
}

const read_file_b = util.promisify(fs.readFile);

const read_file_c = fs_promises.readFile


module.exports = {read_file_a, read_file_b, read_file_c}



