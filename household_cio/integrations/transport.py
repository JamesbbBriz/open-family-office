"""Bounded read-only HTTPS transport. No redirects, secrets in logs or implicit network."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib, json, os, time
from pathlib import Path
from urllib.parse import urlsplit, urlencode
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError, URLError
from ..core import InputError
from ..io import outside_repo, write_new
ALLOWED_HOSTS = frozenset({
 'data.sec.gov','www.sec.gov','api.stlouisfed.org','www.rba.gov.au',
 'data.api.abs.gov.au','sdmx.oecd.org','api.imf.org',
 'api.coingecko.com','pro-api.coingecko.com','www.alphavantage.co',
 'finnhub.io','api.marketdata.app','api.metalpriceapi.com'})
SECRET_NAMES = {'api_key','apikey','token','key','access_token'}
class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):
        raise InputError('Redirect refused; review and explicitly update the provider endpoint')
@dataclass
class Response:
    body: bytes
    content_type: str = ''
    status: int = 200
class Transport:
    def __init__(self, allow_network=False, timeout=20, max_bytes=15_000_000):
        self.allow_network=allow_network; self.timeout=timeout; self.max_bytes=max_bytes
        self._last=0.0
    def get(self,url,params=None,headers=None):
        if not self.allow_network: raise InputError('Network disabled. Pass --allow-network explicitly.')
        parsed=urlsplit(url)
        if parsed.scheme!='https' or parsed.hostname not in ALLOWED_HOSTS or parsed.username or parsed.password or parsed.port not in (None,443):
            raise InputError('Endpoint not in the reviewed HTTPS provider allowlist')
        full=url + ('&' if '?' in url else '?') + urlencode(params or {}) if params else url
        h={'User-Agent':'HouseholdCIO/0.2 (local research; read-only)','Accept':'application/json'}
        h.update(headers or {})
        for attempt in range(3):
            time.sleep(max(0,1.0-(time.monotonic()-self._last)))
            self._last=time.monotonic()
            try:
                with build_opener(NoRedirect).open(Request(full,headers=h),timeout=self.timeout) as resp:
                    data=resp.read(self.max_bytes+1)
                    if len(data)>self.max_bytes: raise InputError('Provider response exceeds configured size limit')
                    return Response(data,resp.headers.get('Content-Type',''),resp.status)
            except HTTPError as exc:
                if exc.code in (429,500,502,503,504) and attempt<2:
                    delay=exc.headers.get('Retry-After','2')
                    time.sleep(min(float(delay) if delay.isdigit() else 2,10));continue
                raise InputError(f'Provider HTTP {exc.code}; response/body/credentials deliberately not logged') from None
            except (URLError,TimeoutError,OSError):
                if attempt<2: time.sleep(2**attempt);continue
                raise InputError('Provider network request failed; not replaced with demo data') from None
        raise InputError('Retry limit exceeded')
def envelope(provider,capability,url,params,response,records,rights='Review provider and underlying dataset terms; no redistribution permission assumed'):
    safe={k:v for k,v in (params or {}).items() if k.lower() not in SECRET_NAMES}
    return {'schema_version':'1.0','provider':provider,'capability':capability,
      'retrieved_at':datetime.now(timezone.utc).isoformat(),'source_url':url,'request_parameters':safe,
      'response_sha256':hashlib.sha256(response.body).hexdigest(),'content_type':response.content_type,
      'synthetic':False,'live_status':'response_received','rights':rights,
      'records':records,'warnings':['Retrieval time is not observation date. Units and periodicity must be verified before use.']}
def save_envelope(result,path):
    return write_new(path,json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
