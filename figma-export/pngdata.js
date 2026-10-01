// pack a string into a valid PNG (tiny visible image + zTXt-like private chunk "rDAT")
const zlib=require('zlib'),fs=require('fs');
const crcT=new Int32Array(256).map((_,n)=>{let c=n;for(let k=0;k<8;k++)c=c&1?0xEDB88320^(c>>>1):c>>>1;return c;});
const crc=b=>{let c=-1;for(const x of b)c=crcT[(c^x)&255]^(c>>>8);return (c^-1)>>>0;};
const chunk=(t,d)=>{const l=Buffer.alloc(4);l.writeUInt32BE(d.length);const td=Buffer.concat([Buffer.from(t),d]);const c=Buffer.alloc(4);c.writeUInt32BE(crc(td));return Buffer.concat([l,td,c]);};
module.exports=(str)=>{const ihdr=Buffer.alloc(13);ihdr.writeUInt32BE(8,0);ihdr.writeUInt32BE(8,4);ihdr[8]=8;ihdr[9]=2;
  const raw=Buffer.alloc(8*(1+24));for(let y=0;y<8;y++){raw[y*25]=0;for(let x=0;x<8;x++){raw[y*25+1+x*3]=29;raw[y*25+2+x*3]=158;raw[y*25+3+x*3]=117;}}
  return Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),chunk('IHDR',ihdr),chunk('rDAT',Buffer.from(str,'utf8')),chunk('IDAT',zlib.deflateSync(raw)),chunk('IEND',Buffer.alloc(0))]);};
if(require.main===module){fs.writeFileSync(process.argv[3],module.exports(fs.readFileSync(process.argv[2],'utf8')));}
