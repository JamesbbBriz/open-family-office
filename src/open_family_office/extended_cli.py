"""Optional commands; lazy imports keep offline accounting dependency-free."""
from __future__ import annotations
import argparse, importlib.metadata, importlib.util, json, os, sys
from pathlib import Path
from .core import InputError
from .io import read_json, write_new, REPO_ROOT

def add_commands(sub):
    sub.add_parser('doctor',help='Report installed dependencies and missing keys without disclosing secrets')
    sub.add_parser('providers',help='List implemented provider capabilities and verification status')
    f=sub.add_parser('fetch',help='Explicit, read-only external data retrieval to an evidence envelope')
    f.add_argument('provider');f.add_argument('capability');f.add_argument('--query',required=True)
    f.add_argument('--allow-network',action='store_true');f.add_argument('--out')
    for name in ('optimize','simulate','lookthrough','exposures','extract-pdf','import-ofx','import-holdings'):
        p=sub.add_parser(name);p.add_argument('input');p.add_argument('--out')
        if name=='optimize':
            p.add_argument('--engine',choices=['scipy','skfolio','pypfopt'],default='scipy')
            p.add_argument('--method',choices=['min_variance','risk_parity','cvar','hrp','black_litterman'],default='min_variance')
    s=sub.add_parser('mcp',help='Start read-only stdio MCP server; explicit OFO_WORKSPACE required')
    p=sub.add_parser('dashboard',help='Export an offline HTML dashboard outside the repository')
    p.add_argument('input');p.add_argument('--out',required=True)
    p.add_argument('--scenario',action='append',default=[])
    p.add_argument('--returns');p.add_argument('--simulation');p.add_argument('--policy')

def execute(args):
    command=args.command
    if command in ('providers','doctor'):
        from .integrations.registry import providers
        data={'providers':providers()}
        if command=='doctor':
            packages={'numpy':'numpy','pandas':'pandas','scipy':'scipy','scikit-learn':'sklearn','skfolio':'skfolio','PyPortfolioOpt':'pypfopt','mcp':'mcp','pypdf':'pypdf','ofxparse':'ofxparse','yfinance':'yfinance','plotly':'plotly'}
            data['dependencies']={}
            for package,module in packages.items():
                try:version=importlib.metadata.version(package)
                except importlib.metadata.PackageNotFoundError:version=None
                data['dependencies'][package]={'installed':importlib.util.find_spec(module) is not None,'version':version}
            data['network']='off until explicitly requested';data['openbb_process']='configured' if os.environ.get('OPENBB_PYTHON') else 'not configured'
    elif command=='fetch':
        from .integrations.providers import fetch
        data=fetch(args.provider,args.capability,json.loads(args.query),allow_network=args.allow_network)
    elif command=='optimize':
        from .quant.allocation import optimize
        data=optimize(read_json(args.input),args.engine,args.method)
    elif command=='simulate':
        from .quant.simulation import simulate
        data=simulate(read_json(args.input))
    elif command=='lookthrough':
        from .quant.ownership import consolidate
        data=consolidate(read_json(args.input))
    elif command=='exposures':
        from .quant.ownership import exposures
        data=exposures(read_json(args.input)['positions'])
    elif command in ('extract-pdf','import-ofx','import-holdings'):
        from .integrations.documents import extract_pdf,import_ofx,holdings_csv
        data={'extract-pdf':extract_pdf,'import-ofx':import_ofx,'import-holdings':holdings_csv}[command](args.input)
    elif command=='mcp':
        from .integrations.mcp_server import main
        main();return True
    elif command=='dashboard':
        sys.path.insert(0,str(REPO_ROOT/'scripts'))
        from build_dashboard import export_dashboard
        output=export_dashboard(read_json(args.input),Path(args.out),[read_json(s) for s in args.scenario],
           returns=read_json(args.returns) if args.returns else None,simulation=read_json(args.simulation) if args.simulation else None,policy=read_json(args.policy) if args.policy else None)
        print(output);return True
    else:return False
    text=json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n'
    if getattr(args,'out',None):print(write_new(args.out,text))
    else:print(text,end='')
    return True
