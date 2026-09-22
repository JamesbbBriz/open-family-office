# Development-only browser test. Requires playwright + Chromium. Rebuild public pages first.
from playwright.sync_api import sync_playwright
from pathlib import Path
import json,urllib.request,tempfile,os
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'artifacts/browser';ASSETS.mkdir(parents=True,exist_ok=True)
report={'engine':'Chromium via Playwright; inline document loading','checks':[],'errors':[],'external_requests':[],'limitations':['Managed Chromium blocks file:// and localhost navigation. Render/interaction tests load exact generated HTML bytes with page.set_content in an offline browser context, not a live deployed URL.','Safari and iOS file preview not tested.']}
def ok(label,condition=True):
 if not condition:raise AssertionError(label)
 report['checks'].append(label)
with sync_playwright() as p:
 browser=p.chromium.launch(**({'executable_path':os.environ.get('CHROMIUM_PATH','/usr/bin/chromium')} if Path(os.environ.get('CHROMIUM_PATH','/usr/bin/chromium')).exists() else {}),headless=True,args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1440,'height':1040},device_scale_factor=1,offline=True,accept_downloads=True)
 def doc(name,width=1440,height=1040):
  page=context.new_page();page.set_viewport_size({'width':width,'height':height})
  page.on('pageerror',lambda e:report['errors'].append(str(e)))
  page.on('console',lambda m:report['errors'].append(m.text) if m.type=='error' else None)
  page.on('request',lambda req:report['external_requests'].append(req.url) if req.url.startswith(('https:','http:')) else None)
  page.set_content((ROOT/'public'/name).read_text(),wait_until='load');return page
 landing=doc('index.html');ok('landing brand',landing.title().startswith('Open Family Office'))
 primary=landing.locator('.hero-copy .btn-primary')
 ok('primary contrast white text',primary.evaluate('(e)=>getComputedStyle(e).color')=='rgb(255, 255, 255)')
 for link in landing.locator('a[href]').all():
  href=link.get_attribute('href').split('#')[0]
  if href and not href.startswith('https:') and not href.startswith('downloads/'):
   ok('relative link resolves: '+href,(ROOT/'public'/href).is_file())
 landing.screenshot(path=str(ASSETS/'landing-full.png'),full_page=True)
 landing.screenshot(path=str(ASSETS/'landing-preview.png'))
 landing.locator('#landingLang').click();ok('landing Chinese language',landing.locator('html').get_attribute('lang')=='zh-CN')
 landing.locator('#landingTheme').click();ok('landing dark theme',landing.locator('html').get_attribute('data-theme')=='ofo-dark')
 landing.locator('details').first.locator('summary').click();ok('FAQ expands',landing.locator('details').first.get_attribute('open')=='')
 landing.close()
 demo=doc('demo.html');demo.wait_for_function('window.__OFO_RENDERED__===true')
 ok('four synthetic household cases',demo.evaluate('Object.keys(__OFO_DATA__.cases).length')==4)
 demo.evaluate('window.scrollTo(0,0)');demo.screenshot(path=str(ASSETS/'dashboard-preview.png'),full_page=True)
 seen=0
 for tab,count in [('overview',2),('cashflow',4),('allocation',4),('scenarios',3),('sources',0),('playground',1)]:
  demo.locator('[data-tab='+tab+']').click();demo.wait_for_timeout(150)
  actual=demo.locator('#tab-'+tab+' .js-plotly-plot').count()
  ok(f'{tab}: {count} rendered charts',actual==count);seen+=actual
  ok(tab+' desktop body width',demo.evaluate('document.documentElement.scrollWidth<=innerWidth'))
 ok('14 rendered chart areas',seen==14)
 demo.locator('[data-tab=overview]').click()
 for scenario in ['baseline','recession','business-sale','income-stop']:
  demo.locator('#scenarioSelect').select_option(scenario);demo.wait_for_timeout(100)
  equal=demo.evaluate('''()=>{const c=__OFO_DATA__.cases[__OFO_STATE__.scenario];const plot=document.getElementById('cashChart');return Math.abs(Number(c.forecast.ending_cash)-plot.data[0].y.at(-1))<0.01;}''')
  ok('cash chart matches Python case '+scenario,equal)
 demo.locator('#scenarioSelect').select_option('baseline')
 demo.locator('[data-tab=allocation]').click();demo.evaluate('window.scrollTo(0,0)');demo.screenshot(path=str(ASSETS/'allocation-preview.png'),full_page=True)
 demo.locator('[data-tab=scenarios]').click();demo.evaluate('window.scrollTo(0,0)');demo.screenshot(path=str(ASSETS/'scenarios-preview.png'),full_page=True)
 demo.locator('[data-tab=playground]').click()
 ok('sandbox independent defaults',demo.evaluate('__OFO_SANDBOX__.ending_cash')==180000)
 demo.locator('#oneoff').fill('900000');demo.locator('#sandboxForm button[type=submit]').click()
 ok('windfall keeps recurring income',demo.evaluate('__OFO_SANDBOX__.ending_cash')==1080000)
 demo.locator('#eventKind').select_option('business-sale');demo.locator('#sandboxForm button[type=submit]').click()
 ok('business sale removes variable income',demo.evaluate('__OFO_SANDBOX__.ending_cash')==985000)
 ok('research data remains independent',demo.evaluate('__OFO_DATA__.cases.baseline.forecast.ending_cash')=='94000.00')
 with demo.expect_download() as info:demo.locator('#exportSandbox').click()
 download=info.value;ok('sandbox JSON download',download.suggested_filename=='open-family-office-cash-scenario.json')
 saved=Path(tempfile.gettempdir())/'ofo-sandbox-export.synthetic.test.json';download.save_as(str(saved));data=json.loads(saved.read_text());ok('export reconciles current scenario',data['ending_cash']==985000)
 demo.evaluate('window.scrollTo(0,0)');demo.screenshot(path=str(ASSETS/'playground-preview.png'),full_page=True)
 demo.locator('#resetSandbox').click();ok('reset restores defaults',demo.evaluate('__OFO_SANDBOX__.ending_cash')==180000)
 demo.locator('#startCash').fill('-1');demo.locator('#sandboxForm button[type=submit]').click();ok('invalid input does not update budget',demo.evaluate('__OFO_SANDBOX__.ending_cash')==180000)
 demo.locator('#resetSandbox').click();demo.locator('#langButton').click();ok('dashboard Chinese',demo.locator('html').get_attribute('lang')=='zh-CN')
 ok('sandbox Chinese labels',demo.locator('#pageTitle').inner_text()=='试算另一种财务情景。')
 demo.locator('#themeButton').click();ok('dashboard dark theme',demo.locator('html').get_attribute('data-theme')=='ofo-dark')
 demo.evaluate('window.scrollTo(0,0)');demo.screenshot(path=str(ASSETS/'playground-dark-preview.png'),full_page=True)
 demo.evaluate('window.print=()=>{window.__PRINT_TEST__=true;}');demo.locator('#printButton').click();demo.wait_for_function('window.__PRINT_TEST__===true');ok('print hook includes all six views',demo.locator('.tab-panel.active').count()==6)
 demo.evaluate("window.dispatchEvent(new Event('afterprint'))");ok('afterprint restores selected view',demo.locator('.tab-panel.active').count()==1)
 demo.close()
 for width in [320,390,768]:
  for name in ['index.html','demo.html']:
   page=doc(name,width,844);page.wait_for_timeout(250)
   ok(f'{name}: no page overflow at {width}',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
   if name=='demo.html':
    for tab in ['overview','cashflow','allocation','scenarios','sources','playground']:
     page.locator('[data-tab='+tab+']').click();page.wait_for_timeout(50)
     ok(f'{tab}: no overflow at {width}',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    if width==390:page.screenshot(path=str(ASSETS/'playground-mobile.png'),full_page=True)
   elif width==390:page.screenshot(path=str(ASSETS/'landing-mobile.png'),full_page=True)
   page.close()
 ok('no browser script or console errors',not report['errors']);ok('no external resource requests',not report['external_requests'])
 browser.close()
# Browser admin restrictions do not prevent verifying a real static HTTP response separately.
try:
 for name in ['index.html','demo.html']:
  data=urllib.request.urlopen('http://127.0.0.1:8765/'+name,timeout=5).read()
  ok('local static HTTP serves exact '+name,data==(ROOT/'public'/name).read_bytes())
except Exception as e:report['limitations'].append('Local HTTP response check unavailable: '+str(e))
report['passed']=len(report['checks'])
(ROOT/'docs/web-validation-v0.3.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'passed':report['passed'],'errors':report['errors'],'external_requests':report['external_requests'],'limitations':report['limitations']},indent=2))
