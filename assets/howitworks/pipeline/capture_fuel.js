const puppeteer = require('puppeteer-core');
const fs = require('fs');
const [,, W, H, outdir, mode, listArg] = process.argv;
(async () => {
  const cfg = JSON.parse(fs.readFileSync('/home/sandbox/reel/config_fuel.json'));
  const frames = mode === 'list' ? listArg.split(',').map(Number)
    : Array.from({length: cfg.frames}, (_, i) => i);
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome', headless: true,
    args: ['--no-sandbox','--disable-dev-shm-usage','--use-angle=swiftshader',
           '--enable-unsafe-swiftshader','--hide-scrollbars','--force-color-profile=srgb',
           '--force-device-scale-factor=1', `--window-size=${W},${H}`]
  });
  const page = await browser.newPage();
  await page.setViewport({width:+W, height:+H, deviceScaleFactor:1});
  page.on('console', m => console.log('PAGE:', m.text()));
  page.on('pageerror', e => console.log('PAGEERR:', e.message));
  await page.goto('http://127.0.0.1:8777/render_fuel.html');
  await page.waitForFunction('window.ready===true', {timeout:180000});
  const t0 = Date.now();
  for (const f of frames) {
    await page.evaluate(f => window.setFrame(f), f);
    await page.screenshot({path: `${outdir}/f_${String(f).padStart(5,'0')}.jpg`, type:'jpeg', quality:94,
      clip:{x:0,y:0,width:+W,height:+H}, captureBeyondViewport:true});
  }
  const dt = (Date.now()-t0)/1000;
  console.log('DONE', frames.length, 'frames in', dt.toFixed(1)+'s');
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
