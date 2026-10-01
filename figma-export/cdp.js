// minimal Chrome DevTools driver (no deps)
const {spawn}=require('child_process');const sleep=ms=>new Promise(r=>setTimeout(r,ms));
module.exports=async function open(url,{w=1440,h=900}={}){
  const port=9333,prof=require('os').tmpdir()+'/ray-cdp-'+Date.now();
  const ch=spawn('C:/Program Files/Google/Chrome/Application/chrome.exe',['--headless=new','--remote-debugging-port='+port,'--user-data-dir='+prof,'--hide-scrollbars','--force-device-scale-factor=1','--window-size='+w+','+h,'about:blank'],{stdio:'ignore'});
  let tgt;for(let i=0;i<50&&!tgt;i++){await sleep(200);try{tgt=(await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find(t=>t.type==='page');}catch{}}
  const ws=new WebSocket(tgt.webSocketDebuggerUrl);await new Promise(r=>ws.onopen=r);
  let id=0;const pend={};ws.onmessage=m=>{const d=JSON.parse(m.data);if(d.id&&pend[d.id]){pend[d.id](d);delete pend[d.id];}};
  const send=(method,params={})=>new Promise((res,rej)=>{const i=++id;pend[i]=d=>d.error?rej(new Error(method+': '+d.error.message)):res(d.result);ws.send(JSON.stringify({id:i,method,params}));});
  await send('Emulation.setDeviceMetricsOverride',{width:w,height:h,deviceScaleFactor:1,mobile:false});
  const ev=async(expr)=>{const r=await send('Runtime.evaluate',{expression:expr,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error('eval: '+(r.exceptionDetails.exception?.description||r.exceptionDetails.text)+'\n  in: '+expr.slice(0,120));return r.result.value;};
  const go=async u=>{await send('Page.enable');await send('Page.navigate',{url:u});await sleep(1500);await ev('document.fonts.ready.then(()=>1)');};
  await go(url);
  return {send,ev,go,sleep,shot:async(f)=>{const r=await send('Page.captureScreenshot',{format:'png'});require('fs').writeFileSync(f,Buffer.from(r.data,'base64'));},close:()=>{ws.close();ch.kill();}};
};
