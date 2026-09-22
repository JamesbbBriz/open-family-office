#!/usr/bin/env python3
"""Browser verification + actual screenshots. Optional: pip install playwright; install Chromium.
No generated/private workspace is opened. Only checked-in synthetic public/demo.html is used.
"""
import asyncio,json,os,shutil,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        executable=os.environ.get('CHROMIUM_EXECUTABLE') or shutil.which('chromium') or shutil.which('google-chrome')
        options={'headless':True,'args':['--no-sandbox']}
        if executable: options['executable_path']=executable
        browser=await p.chromium.launch(**options)
        page=await browser.new_page(viewport={'width':1500,'height':1120},device_scale_factor=1)
        errors=[];requests=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('request',lambda r:requests.append(r.url) if r.url.startswith('http') else None)
        await page.set_content((ROOT/'public/demo.html').read_text(),wait_until='load')
        await page.wait_for_function('window.__HH_RENDERED__===true')
        await page.wait_for_timeout(700)
        assert await page.evaluate('window.__HH_DATA__.household.synthetic===true')
        checks={}
        for tab in ['overview','cashflow','allocation','scenarios','sources']:
            await page.locator(f'[data-tab="{tab}"]').click();await page.wait_for_timeout(400)
            checks[tab]=await page.evaluate("({charts:document.querySelectorAll('.tab-panel.active .js-plotly-plot').length,overflow:document.documentElement.scrollWidth>window.innerWidth})")
            assert not checks[tab]['overflow'],tab+' overflow'
            await page.screenshot(path=str(ROOT/f'assets/demo-{tab}.png'),full_page=True)
        assert sum(checks[t]['charts'] for t in checks)==13
        await page.locator('[data-tab="overview"]').click()
        scenario_checks={}
        for scenario in ['baseline','recession','business-sale','income-stop']:
            await page.select_option('#scenarioSelect',scenario);await page.wait_for_timeout(220)
            assert await page.evaluate('window.__HH_STATE__.scenario')==scenario
            displayed=await page.evaluate("document.getElementById('cashChart').data[0].y.at(-1)")
            expected=await page.evaluate("Number(window.__HH_DATA__.cases[window.__HH_STATE__.scenario].forecast.ending_cash)")
            assert abs(displayed-expected)<.01
            scenario_checks[scenario]={'ending_cash':displayed,'reconciles':True}
        await page.select_option('#scenarioSelect','business-sale');await page.wait_for_timeout(220)
        await page.screenshot(path=str(ROOT/'assets/demo-business-sale.png'),full_page=True)
        await page.locator('[data-horizon="12"]').click()
        assert await page.evaluate("document.getElementById('cashChart').data[0].y.length")==12
        await page.locator('[data-horizon="24"]').click()
        async with page.expect_download() as info:await page.click('#exportButton')
        download=await info.value
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)/'research.json';await download.save_as(str(target))
            exported=json.loads(target.read_text());assert exported['household']['synthetic'] is True
            assert exported['selected_scenario']['forecast']['ending_cash']=='899000.00'
        await page.click('#themeButton');await page.wait_for_timeout(300)
        assert await page.evaluate("document.documentElement.classList.contains('dark')")
        await page.screenshot(path=str(ROOT/'assets/demo-dark.png'),full_page=True)
        await page.click('#langButton');await page.wait_for_timeout(250)
        assert await page.evaluate('document.documentElement.lang')=='zh-CN'
        await page.screenshot(path=str(ROOT/'assets/demo-chinese.png'),full_page=True)
        await page.set_viewport_size({'width':390,'height':844});await page.wait_for_timeout(300)
        checks['mobile']={}
        for tab in ['overview','cashflow','allocation','scenarios','sources']:
            await page.locator(f'[data-tab="{tab}"]').click();await page.wait_for_timeout(180)
            overflow=await page.evaluate('document.documentElement.scrollWidth>window.innerWidth')
            assert not overflow,'Mobile '+tab+' overflow'
            checks['mobile'][tab]={'horizontal_overflow':overflow}
        await page.locator('[data-tab="overview"]').click();await page.wait_for_timeout(250)
        await page.screenshot(path=str(ROOT/'assets/demo-mobile.png'),full_page=True)
        await page.set_viewport_size({'width':1500,'height':1120})
        await page.evaluate('window.print=()=>{window.__printCalled=true}')
        await page.click('#printButton');await page.wait_for_timeout(850)
        assert await page.evaluate('window.__printCalled===true')
        assert await page.locator('.tab-panel.active').count()==5
        await page.evaluate("window.dispatchEvent(new Event('afterprint'))")
        assert await page.locator('.tab-panel.active').count()==1
        assert not errors,errors
        assert not requests,requests
        results={'browser':browser.version,'load_mode':'standalone file contents via set_content; file navigation blocked by environment policy','javascript_errors':errors,'external_http_requests':requests,'checks':checks,'scenarios':scenario_checks,'chart_count':13,'json_export':True,'print_handler':True,'theme_switch':True,'core_language_switch':True,'source':'synthetic checked-in report'}
        (ROOT/'evals/browser-results.json').write_text(json.dumps(results,indent=2)+'\n')
        print(json.dumps(results,indent=2))
        await browser.close()
if __name__=='__main__':asyncio.run(main())
