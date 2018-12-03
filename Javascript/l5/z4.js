const fs = require('fs');
const http = require('http');
const express = require('express');
const url = require('url');

var app = express();
app.set('view engine', 'ejs');
app.set('views', 'views')
app.use(express.urlencoded({ extended: true }));



app.get('/', (req, res) => {
    res.render('index');
});

app.post('/', (req, res) => {
    res.redirect(url.format({
        pathname: '/print',
        query: req.body
    }))
});

app.get('/print', (req, res) => {
    req.query.z = req.query.z.map((a) => a?a:'0')
    res.render('print', req.query)
    res.end();
});

http.createServer(app).listen(3000);
