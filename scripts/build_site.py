#!/usr/bin/env python3
"""Build public-only landing/demo; no account, upload, telemetry or private input."""
from pathlib import Path
import html,json,re,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.build_dashboard import main as build_dashboard
ROOT=Path(__file__).resolve().parents[1]
def preview_svg(data):
    """Use the same explicit synthetic monthly cash budget as the demo."""
    forecast=data['cases']['baseline']['forecast']
    values=[float(forecast['opening_cash'])]+[float(r['closing_cash']) for r in forecast['months_table']]
    low=min(0,min(values)); high=max(values)*1.15 or 1
    points=[(8+i*418/(len(values)-1),140-(v-low)/(high-low)*127) for i,v in enumerate(values)]
    line='M '+' L '.join(f'{x:.2f},{y:.2f}' for x,y in points)
    fill=line+' L 426,140 L 8,140 Z'
    return f'''<svg viewBox="0 0 435 150" role="img" aria-label="Synthetic baseline cash budget starts at 120,000 Australian dollars and ends at 94,000 after 24 months"><defs><linearGradient id="cash-fill" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#72a78c" stop-opacity=".25"/><stop offset="1" stop-color="#72a78c" stop-opacity=".02"/></linearGradient></defs><path d="M 8,22 H 426 M 8,61 H 426 M 8,100 H 426 M 8,139 H 426" fill="none" stroke="var(--line)" stroke-dasharray="3 5"/><path d="{fill}" fill="url(#cash-fill)"/><path d="{line}" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/><circle cx="{points[-1][0]:.2f}" cy="{points[-1][1]:.2f}" r="3.5" fill="var(--accent)"/></svg>'''
def main():
    build_dashboard()
    data=json.loads((ROOT/'examples/dashboard-data.synthetic.json').read_text())
    if data['household'].get('synthetic') is not True:raise ValueError('Landing preview must be synthetic')
    cfg=json.loads((ROOT/'web/config/site.json').read_text())
    # Only a vetted HTTPS GitHub URL may replace the locally generated download.
    repo=cfg.get('repository_url')
    if repo is not None and not re.fullmatch(r'https://github\.com/[\w.-]+/[\w.-]+/?',repo):raise ValueError('repository_url must be a GitHub repository HTTPS URL')
    source=repo or 'downloads/open-family-office-kit.zip'
    values={'__TAILWIND_CSS__':(ROOT/'web/src/tailwind.generated.css').read_text(),
      '__SHARED_CSS__':(ROOT/'web/src/shared.css').read_text(),'__LANDING_CSS__':(ROOT/'web/src/landing.css').read_text(),
      '__LANDING_JS__':(ROOT/'web/src/landing.js').read_text(),'__PREVIEW_CHART__':preview_svg(data),'__SOURCE_HREF__':html.escape(source,quote=True)}
    template=(ROOT/'web/src/landing.html').read_text()
    if repo:
        template=template.replace('download="open-family-office-kit.zip"','rel="noopener noreferrer"')
        template=template.replace('Download source kit ↓','View source on GitHub ↗').replace('下载项目包 ↓','在GitHub查看源码 ↗')
    result=re.sub('|'.join(map(re.escape,values)),lambda m:values[m.group(0)],template)
    notice='\n'.join(p.read_text() for p in sorted((ROOT/'vendor/licenses').glob('*.txt')))
    result+='\n<!-- THIRD PARTY NOTICES\n'+notice.replace('--','- -')+'\n-->\n'
    (ROOT/'public/index.html').write_text(result)
    (ROOT/'public/.nojekyll').write_text('')
    (ROOT/'public/_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: no-referrer\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n  X-Frame-Options: DENY\n')
    print('Built public/index.html and public/demo.html; run scripts/package_web.py before publishing to add the source download.')
if __name__=='__main__':main()
