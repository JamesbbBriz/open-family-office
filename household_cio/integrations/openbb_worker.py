"""Isolated OpenBB process. Only allowlisted read routes; no eval/arbitrary traversal."""
import contextlib, json, sys

def main():
    message=json.load(sys.stdin);q=message['query'];cap=message['capability']
    with contextlib.redirect_stdout(sys.stderr):
        from openbb import obb
        provider=q.get('provider','yfinance')
        if cap=='history':result=obb.equity.price.historical(symbol=q['symbol'],start_date=q.get('start'),end_date=q.get('end'),provider=provider)
        elif cap=='quote':result=obb.equity.price.quote(symbol=q['symbol'],provider=provider)
        elif cap=='search':result=obb.equity.search(query=q['query'],provider=provider)
        elif cap=='macro':result=obb.economy.fred_series(symbol=q['series_id'],provider='fred')
        else:raise ValueError('Unknown route')
    print(result.model_dump_json())
if __name__=='__main__':main()
