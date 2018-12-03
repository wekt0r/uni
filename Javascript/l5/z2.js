/*
openssl req -x509 -out localhost.crt -keyout localhost.key \
  -newkey rsa:2048 -nodes -sha256 \
*/
// openssl pkcs12 -export -out test.pfx -inkey localhost.key -in localhost.crt
//

const fs = require('fs');
const https = require('https');

//var pfx = await fs.promises.readFile('./test.pfx');
https.createServer({
	   pfx: fs.readFileSync('test.pfx'),
	   passphrase: 'test'
	},
	(request, response) => {
		response.setHeader('Content-type', 'text/html; charset=utf-8');
		response.end(`hello world ${new Date()}`);
	}).listen(3000);

console.log("server started");
