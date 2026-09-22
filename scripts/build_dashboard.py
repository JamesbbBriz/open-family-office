#!/usr/bin/env python3
"""Build a truly standalone Tailwind + Plotly report, with no network requests."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import argparse, json, sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from open_family_office.core import snapshot,cashflow,stress,allocation,validate,active,fx_rate,number,month_start,iso
from open_family_office.io import REPO_ROOT,read_json,write_new
from open_family_office.integrations.registry import providers

def payload(h,scenarios=None,returns=None,simulation=None,policy=None):
    validate(h)
    cases={'baseline':{'label':'Baseline','snapshot':snapshot(h),'forecast':cashflow(h),'change':'0','explanation':'Current assets and dated cash budget; not a future balance sheet.','asset_shocks':{}}}
    for scenario in scenarios or []:
        result=stress(h,scenario)
        cases[scenario['id']]={'label':scenario['label'],'snapshot':result['instant_price_shock_snapshot'],'forecast':result['cashflow'],'change':result['instant_net_worth_change'],'explanation':scenario['note'],'asset_shocks':scenario['asset_shocks']}
    for key,c in cases.items():
        scenario=next((s for s in (scenarios or []) if s['id']==key),None)
        c['one_off_outflows']={}
        for i,row in enumerate(c['forecast']['months_table'],1):
            month=month_start(iso(h['as_of'],'as_of'),i)
            total=sum((number(f['amount'])*fx_rate(h,f['currency'])*number((scenario or {}).get('cashflow_multipliers',{}).get(f['id'],'1')) for f in h['cashflows'] if f['direction']=='out' and f['recurrence']=='one_off' and active(f,month)),number('0'))
            c['one_off_outflows'][row['month']]=float(total)
    quant=None
    if returns:
        import numpy as np
        from open_family_office.quant.allocation import optimize,frontier
        quant={'frontier':frontier(returns),'optimizers':{m:optimize(returns,'scipy',m) for m in ['min_variance','risk_parity','cvar']},'correlation':np.corrcoef(np.asarray(returns['returns']),rowvar=False).tolist(),'assets':returns['assets'],'synthetic':returns.get('synthetic',False)}
    sim=None
    if simulation:
        from open_family_office.quant.simulation import simulate
        sim=simulate(simulation)
    compare=allocation(h,policy) if policy else None
    regular=sum((number(f['amount'])*fx_rate(h,f['currency']) for f in h['cashflows'] if f['direction']=='out' and f['recurrence']=='monthly'),number('0'))
    return {'version':'0.3.0','household':h,'cases':cases,'quant':quant,'simulation':sim,'allocation':compare,
      'reserve':float(compare['reserve_excluded']) if compare else 0,'regular_monthly_outflows':float(regular),'providers':providers(),
      'disclosure':'Source data and chart scripts are embedded. No external network calls are required by this HTML.'}

def render(data):
    from plotly.offline import get_plotlyjs
    root=REPO_ROOT/'web/src';template=(root/'dashboard.html').read_text()
    values={'__TAILWIND_CSS__':(root/'tailwind.generated.css').read_text(),'__APP_CSS__':(root/'dashboard.css').read_text(),
      '__SHARED_CSS__':(root/'shared.css').read_text(),'__SANDBOX_MATH__':(root/'sandbox.js').read_text(),
      '__DASHBOARD_DATA__':json.dumps(data,ensure_ascii=True,allow_nan=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026'),
      '__PLOTLY_JS__':get_plotlyjs().replace('</script','<\\/script'), '__APP_JS__':(root/'dashboard.js').read_text()}
    # Replace in one pass: user data must never be reinterpreted as another placeholder.
    import re
    content=re.sub('|'.join(map(re.escape,values)),lambda m:values[m.group(0)],template)
    notice='\n'.join(p.read_text() for p in sorted((REPO_ROOT/'vendor/licenses').glob('*.txt')))
    return content+'\n<!-- THIRD PARTY LICENSES\n'+notice.replace('--','- -')+'\n-->\n'

def export_dashboard(h,out,scenarios=None,returns=None,simulation=None,policy=None):
    content=render(payload(h,scenarios,returns,simulation,policy));return write_new(out,content)

def main():
    h=read_json(REPO_ROOT/'examples/household.synthetic.json')
    if h.get('synthetic') is not True:raise ValueError('Public build requires an explicitly synthetic fixture')
    scenarios=[read_json(p) for p in sorted((REPO_ROOT/'examples/scenarios').glob('*.json'))]
    data=payload(h,scenarios,read_json(REPO_ROOT/'examples/returns.synthetic.json'),read_json(REPO_ROOT/'examples/simulation.synthetic.json'),read_json(REPO_ROOT/'examples/policy.synthetic.json'))
    (REPO_ROOT/'public').mkdir(exist_ok=True)
    (REPO_ROOT/'public/demo.html').write_text(render(data))
    (REPO_ROOT/'examples/dashboard-data.synthetic.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    print('Built offline Tailwind + Plotly dashboard:',(REPO_ROOT/'public/demo.html').stat().st_size,'bytes')
if __name__=='__main__':main()
