// Builds ray-word-addin-interactive-c4.html from the .src.html by inlining ../assets SVGs. Run: node ray-word-addin-interactive-c4.build.js
const fs=require('fs'),p=require('path');const here=__dirname;
const uri=f=>'data:image/svg+xml;base64,'+fs.readFileSync(p.join(here,'assets',f)).toString('base64');
let html=fs.readFileSync(p.join(here,'ray-word-addin-interactive-c4.src.html'),'utf8');
html=html.replace('"__RAY__"',JSON.stringify(uri('ray-avatar.svg'))).replace('"__WORDMARK__"',JSON.stringify(uri('tenderfy-wordmark.svg')));
fs.writeFileSync(p.join(here,'ray-word-addin-interactive-c4.html'),html);console.log('built',html.length,'bytes');
