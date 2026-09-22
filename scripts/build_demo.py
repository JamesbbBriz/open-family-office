#!/usr/bin/env python3
"""Regenerate public output ONLY from bundled synthetic fixtures; no networking."""
from pathlib import Path
import html
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from household_cio.io import REPO_ROOT,read_json
from household_cio.core import snapshot,cashflow,stress,allocation,InputError
from household_cio.reports import markdown


def main():
    h=read_json(REPO_ROOT/'examples/household.synthetic.json')
    if h.get('synthetic') is not True:
        raise InputError('Public demo can only be generated from an explicitly synthetic fixture')
    base=snapshot(h)
    cases={'baseline':{'label':'Baseline','snapshot':base,'forecast':cashflow(h),'change':'0.00','explanation':'A current balance sheet and a dated cash budget. The one-off school payment and fund capital call are not averaged away.'}}
    descriptions={
        'recession':'User-specified markdowns across assets, with business receipts 60% lower. Price losses change wealth; reduced receipts change cash. No probability is assigned.',
        'business-sale':'A one-off equity sale brings in cash in month six. The business asset is removed in the event bridge and its recurring distributions stop.',
        'income-stop':'Business distributions stop with no sale proceeds. A household can remain asset-rich while the budget develops an unfunded cash gap.'}
    for name in ['recession','business-sale','income-stop']:
        s=read_json(REPO_ROOT/f'examples/scenarios/{name}.json')
        result=stress(h,s)
        cases[name]={'label':{'recession':'Recession stress','business-sale':'Business sale','income-stop':'Income stops'}[name],'snapshot':result['instant_price_shock_snapshot'],'forecast':result['cashflow'],'change':result['instant_net_worth_change'],'explanation':descriptions[name]}
    expected=REPO_ROOT/'examples/expected';expected.mkdir(exist_ok=True)
    for name,data in cases.items():
        (expected/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n')
        (expected/f'{name}.md').write_text(markdown(data['snapshot'])+'\n'+markdown(data['forecast']))
    (expected/'allocation.json').write_text(json.dumps(allocation(h,read_json(REPO_ROOT/'examples/policy.synthetic.json')),indent=2)+'\n')
    template=(REPO_ROOT/'site/template.html').read_text()
    # Escape script closers: input is synthetic but do not build an injection-prone renderer.
    payload=json.dumps(cases,ensure_ascii=True).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    (REPO_ROOT/'site/legacy-demo.html').write_text(template.replace('__DEMO_DATA__',payload),encoding='utf-8')
    print('Generated four synthetic cases, allocation output and site/legacy-demo.html (historical UI)')

if __name__=='__main__':main()
