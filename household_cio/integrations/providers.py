"""Functional provider requests with bounded capability surface; never overwrite a household."""
from __future__ import annotations
import csv, io, json, os, re, sys, subprocess
from pathlib import Path
from urllib.parse import urlsplit
from .transport import Transport, Response, envelope
from ..core import InputError

def _identifier(value,label='identifier',pattern=r'[A-Za-z0-9_.+,:@()=-]+'):
    if not isinstance(value,str) or not re.fullmatch(pattern,value):raise InputError(f'Invalid {label}')
    return value

def _env(name):
    value=os.environ.get(name,'').strip()
    if not value:raise InputError(f'Missing environment variable: {name}')
    return value

def csv_records(data):
    text=data.decode('utf-8-sig')
    rows=list(csv.reader(io.StringIO(text)))
    # RBA has descriptive preamble above its Series ID / date header.
    for i,row in enumerate(rows):
        if row and row[0].strip().lower() in {'series id','date','time_period'}:
            rows=rows[i:];break
    if not rows:return []
    header=rows[0]
    return [{header[i] or f'column_{i}':v for i,v in enumerate(row) if i<len(header)} for row in rows[1:] if any(row)]

def fetch(provider,capability,query,*,allow_network=False,transport=None):
    """Network consent is mandatory even with OpenBB/Yahoo SDKs. query is a structured object."""
    if not isinstance(query,dict):raise InputError('query must be an object')
    if not allow_network and transport is None: raise InputError('Pass --allow-network to contact an external provider')
    t=transport or Transport(allow_network=True)
    p={};headers={};parser='json';rights='Provider/dataset terms must be reviewed; commercial redistribution is NOT granted by this adapter.'
    if provider=='sec-edgar':
        cik=_identifier(str(query.get('cik','')).zfill(10),'CIK',r'\d{10}')
        ua=_env('SEC_USER_AGENT')
        if '@' not in ua:raise InputError('SEC_USER_AGENT must identify a contact email, per SEC fair access guidance')
        headers={'User-Agent':ua,'Accept-Encoding':'identity'}
        if capability=='filings':url=f'https://data.sec.gov/submissions/CIK{cik}.json'
        elif capability=='companyfacts':url=f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
        else:raise InputError('SEC capability must be filings or companyfacts')
    elif provider=='fred':
        if capability!='series':raise InputError('FRED supports series')
        url='https://api.stlouisfed.org/fred/series/observations'
        p={'series_id':_identifier(query.get('series_id','')),'api_key':_env('FRED_API_KEY'),'file_type':'json'}
        for k in ('observation_start','observation_end','realtime_start','realtime_end','units','frequency'):
            if k in query:p[k]=query[k]
    elif provider=='rba':
        if capability!='table':raise InputError('RBA supports table; use series codes from table metadata')
        table=_identifier(query.get('table',''),'table',r'[a-z][0-9]{2}(?:hist)?')
        url=f'https://www.rba.gov.au/statistics/tables/csv/{table}-data.csv';parser='csv'
    elif provider in ('abs','oecd','imf'):
        if capability not in ('data','dataflows'):raise InputError('SDMX supports data and dataflows')
        bases={'abs':'https://data.api.abs.gov.au/rest','oecd':'https://sdmx.oecd.org/public/rest/v1','imf':'https://api.imf.org/external/sdmx/2.1'}
        if provider=='imf' and os.environ.get('IMF_API_KEY'):headers['Ocp-Apim-Subscription-Key']=os.environ['IMF_API_KEY']
        if capability=='dataflows':
            url=bases[provider]+'/dataflow/all/all/latest';p={'references':'none'};parser='text';headers['Accept']='application/vnd.sdmx.structure+xml;version=2.1'
        else:
            flow=_identifier(query.get('flow',''),'flow')
            key=_identifier(query.get('key','all'),'dimension key')
            url=f'{bases[provider]}/data/{flow}/{key}'
            p={k:query[k] for k in ('startPeriod','endPeriod','lastNObservations') if k in query}
            headers['Accept']='csvfile' if provider=='abs' else 'text/csv';parser='csv'
    elif provider=='coingecko':
        mode=query.get('mode','demo')
        if mode not in ('demo','pro'):raise InputError('CoinGecko mode must be demo or pro')
        base='https://pro-api.coingecko.com/api/v3' if mode=='pro' else 'https://api.coingecko.com/api/v3'
        headers['x-cg-pro-api-key' if mode=='pro' else 'x-cg-demo-api-key']=_env('COINGECKO_API_KEY')
        if capability=='quote':
            url=base+'/simple/price';p={'ids':_identifier(query.get('ids',''),pattern=r'[a-z0-9,-]+'),'vs_currencies':_identifier(query.get('currency','aud')),'include_last_updated_at':'true'}
        elif capability=='history':
            ident=_identifier(query.get('id',''),pattern=r'[a-z0-9-]+');url=base+f'/coins/{ident}/market_chart';p={'vs_currency':query.get('currency','aud'),'days':int(query.get('days',30))}
        else:raise InputError('CoinGecko supports quote/history')
    elif provider=='alpha-vantage':
        if capability!='history':raise InputError('Alpha Vantage supports daily adjusted history')
        url='https://www.alphavantage.co/query';p={'function':'TIME_SERIES_DAILY_ADJUSTED','symbol':_identifier(query.get('symbol','')),'apikey':_env('ALPHA_VANTAGE_API_KEY'),'outputsize':'compact'}
    elif provider=='finnhub':
        if capability!='quote':raise InputError('Finnhub supports quote')
        url='https://finnhub.io/api/v1/quote';p={'symbol':_identifier(query.get('symbol',''))};headers['X-Finnhub-Token']=_env('FINNHUB_API_KEY')
    elif provider=='marketdata':
        if capability!='quote':raise InputError('MarketData supports quote')
        url='https://api.marketdata.app/v1/stocks/quotes/'+_identifier(query.get('symbol',''))+'/'
        headers['Authorization']='Bearer '+_env('MARKETDATA_API_KEY')
    elif provider=='metalprice':
        if capability!='quote':raise InputError('Metalprice supports quote')
        url='https://api.metalpriceapi.com/v1/latest';p={'api_key':_env('METALPRICE_API_KEY'),'base':_identifier(query.get('base','AUD')),'currencies':_identifier(query.get('currencies','XAU,XAG'))}
    elif provider=='yahoo':
        if capability!='history':raise InputError('Yahoo supports history only in this bridge')
        if not allow_network:raise InputError('Yahoo requires explicit network consent')
        try:import yfinance as yf
        except ImportError:raise InputError('Install the market extra to enable yfinance') from None
        symbol=_identifier(query.get('symbol',''))
        try:
            frame=yf.download(symbol,start=query.get('start'),end=query.get('end'),auto_adjust=False,progress=False,threads=False,timeout=20)
        except Exception as e:raise InputError('Yahoo request failed; no fixture fallback') from None
        if frame.empty:raise InputError('Yahoo returned no observations')
        # Preserve dates and adjusted/unadjusted column names, not a falsely normalized price.
        frame=frame.copy()
        if getattr(frame.columns,'nlevels',1)>1:frame.columns=['|'.join(map(str,column)) for column in frame.columns]
        text=frame.reset_index().to_json(orient='records',date_format='iso')
        result=envelope(provider,capability,'https://finance.yahoo.com',query,Response(text.encode(),'application/json'),json.loads(text),'Personal research only by default; obtain the necessary data rights for hosting/redistribution.')
        result['warnings'].append('yfinance is an unofficial client; endpoint access can change. No guaranteed SLA.')
        return result
    elif provider=='openbb':
        if not allow_network:raise InputError('OpenBB requires explicit network consent')
        if capability not in ('history','quote','search','macro'):raise InputError('Unsupported OpenBB route')
        python=os.environ.get('OPENBB_PYTHON')
        if not python:raise InputError('Set OPENBB_PYTHON to the isolated OpenBB environment interpreter')
        worker=Path(__file__).with_name('openbb_worker.py')
        try:
            proc=subprocess.run([python,str(worker)],input=json.dumps({'capability':capability,'query':query}),capture_output=True,text=True,timeout=90,check=False)
        except (OSError,subprocess.TimeoutExpired):raise InputError('OpenBB worker unavailable or timed out') from None
        if proc.returncode:raise InputError('OpenBB worker failed. Check provider credentials and supported route; stderr withheld to avoid credential leaks.')
        try:data=json.loads(proc.stdout)
        except ValueError:raise InputError('OpenBB returned invalid JSON') from None
        return envelope(provider,capability,'https://docs.openbb.co/python/reference/',query,Response(proc.stdout.encode(),'application/json'),data)
    else:raise InputError('Unknown provider; use providers command for the supported registry')
    response=t.get(url,params=p,headers=headers)
    text=response.body.decode('utf-8-sig')
    if parser=='json':
        try:records=json.loads(text)
        except ValueError:raise InputError('Provider returned invalid JSON, possibly an authentication page') from None
        if isinstance(records,dict) and any(k in records for k in ('Error Message','error','error_message','Information','Note')):
            raise InputError('Provider returned an API error or quota/entitlement notice; not treated as data')
    elif parser=='csv':
        if text.lstrip().startswith(('<','{')):raise InputError('Expected CSV but received a structured error/unsupported format')
        records=csv_records(response.body)
    else:records={'sdmx_xml':text}
    return envelope(provider,capability,url,p,response,records,rights)
