const fs = require('fs');
const http = require('http');

//var pfx = await fs.promises.readFile('./test.pfx');
http.createServer((request, response) => {
		response.setHeader('Content-type', 'text/txt; charset=utf-8');
		response.setHeader('Content-Disposition', 'attachment; filename="doc.txt"')
		response.end(`hello text file with ${new Date()}`);
	}).listen(3000);

console.log("server started");
