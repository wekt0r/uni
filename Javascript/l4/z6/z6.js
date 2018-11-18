const fs = require('fs');

fs.readFile('./test.txt', (_, data) => { console.log(`I have read: ${data}`) })
