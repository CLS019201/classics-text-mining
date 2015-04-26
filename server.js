var express  = require('express');
var app = express();
app.use(express.static(__dirname+'/wiki_proj/viz'));
console.log("Visualizing the world on port 8000");
app.listen(process.env.port || 8000);