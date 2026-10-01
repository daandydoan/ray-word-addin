// pack.js <in> <out.png> : ASCII-escape and wrap a text/JSON file into a PNG data chunk
const fs = require('fs');
const s = fs.readFileSync(process.argv[2], 'utf8').replace(/[^\x00-\x7f]/g, c => '\\u' + c.charCodeAt(0).toString(16).padStart(4, '0'));
fs.writeFileSync(process.argv[3], require('./pngdata')(s));
