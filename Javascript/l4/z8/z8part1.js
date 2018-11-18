const fs = require('fs');

//1 część: wykład po prostu fs.readFile z callbackiem

fs.readFile('./test.txt', (_, data) => { console.log(`I have read: ${data}`) })


