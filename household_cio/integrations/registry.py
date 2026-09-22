"""Capability metadata, not a claim of live service availability."""
import importlib.util, os
SPECS = [
 ('sec-edgar',['filings','companyfacts'],['SEC_USER_AGENT'],None),
 ('fred',['series'],['FRED_API_KEY'],None),('rba',['table'],[],None),
 ('abs',['data','dataflows'],[],None),('oecd',['data','dataflows'],[],None),
 ('imf',['data','dataflows'],[],None),('coingecko',['quote','history'],['COINGECKO_API_KEY'],None),
 ('yahoo',['history'],[],'yfinance'),('openbb',['history','quote','search','macro'],['OPENBB_PYTHON'],None),
 ('alpha-vantage',['history'],['ALPHA_VANTAGE_API_KEY'],None),('finnhub',['quote'],['FINNHUB_API_KEY'],None),
 ('marketdata',['quote'],['MARKETDATA_API_KEY'],None),('metalprice',['quote'],['METALPRICE_API_KEY'],None)]
def providers():
    return [{'id':name,'capabilities':caps,'implementation':'adapter_written',
      'validation':'contract_fixture_tests; live_connection_not_verified_in_delivery',
      'required_environment':env,'missing_environment':[e for e in env if not os.environ.get(e)],
      'dependency':dep,'dependency_available':(importlib.util.find_spec(dep) is not None) if dep else True,
      'network_default':'off','redistribution':'not_assumed',
      'note':'IMF endpoint, dimensions and beta access must be confirmed against your portal' if name=='imf' else ''}
      for name,caps,env,dep in SPECS]
