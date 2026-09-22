"""Correlated lognormal liquid-sleeve simulations with explicit assumptions and cash flows."""
import numpy as np
from ..core import InputError

def simulate(spec):
    names=spec.get('assets',[]);n=len(names)
    mu=np.asarray(spec.get('annual_drift',[]),float);vol=np.asarray(spec.get('annual_volatility',[]),float)
    corr=np.asarray(spec.get('correlation',[]),float);weights=np.asarray(spec.get('weights',[]),float)
    months=spec.get('months',120);paths=spec.get('paths',2000);capital=float(spec.get('initial_capital',0));seed=spec.get('seed',42)
    if spec.get('scope')!='liquid_sleeve':raise InputError('Simulation scope must be liquid_sleeve; not a whole-household net worth forecast')
    if n<1 or any(v.shape!=(n,) for v in (mu,vol,weights)) or corr.shape!=(n,n):raise InputError('Simulation dimensions do not match asset list')
    if not all(np.isfinite(a).all() for a in (mu,vol,weights,corr)) or not np.isfinite(capital) or capital<0:raise InputError('Simulation inputs must be finite; capital nonnegative')
    if (vol<0).any() or (weights<0).any() or not np.isclose(weights.sum(),1):raise InputError('Invalid volatility or long-only weights')
    if not np.allclose(corr,corr.T) or not np.allclose(np.diag(corr),1) or np.linalg.eigvalsh(corr).min()<-1e-9:raise InputError('Correlation must be symmetric positive semidefinite with unit diagonal')
    if type(months) is not int or not 1<=months<=600 or type(paths) is not int or not 100<=paths<=20000 or n>30:raise InputError('Simulation limits: 1..600 months, 100..20000 paths, <=30 assets')
    flows=np.asarray(spec.get('monthly_net_cashflows',[0]*months),float)
    if flows.shape!=(months,) or not np.isfinite(flows).all():raise InputError('Provide one finite net cash flow per simulated month')
    covariance=np.outer(vol,vol)*corr/12
    eig,vec=np.linalg.eigh(covariance);factor=vec@np.diag(np.sqrt(np.maximum(eig,0)))
    rng=np.random.default_rng(seed);values=np.full(paths,capital);history=np.zeros((paths,months+1));history[:,0]=capital
    first_gap=np.zeros(paths,dtype=bool);gap_amount=np.zeros(paths)
    for m in range(months):
        shocks=rng.standard_normal((paths,n))@factor.T
        gross=np.exp((mu-.5*vol**2)/12+shocks)
        values=values*(gross@weights)+flows[m]
        gap=values<0;first_gap|=gap;gap_amount+=np.maximum(-values,0);values=np.maximum(values,0)
        history[:,m+1]=values
    quantiles=np.percentile(history,[5,25,50,75,95],axis=0)
    return {'scope':'liquid_sleeve','seed':seed,'paths':paths,'months':months,
      'assumptions':spec,'percentiles':[{'month':i,'p05':float(quantiles[0,i]),'p25':float(quantiles[1,i]),'p50':float(quantiles[2,i]),'p75':float(quantiles[3,i]),'p95':float(quantiles[4,i])} for i in range(months+1)],
      'simulated_paths_with_unfunded_gap_fraction':float(first_gap.mean()),'mean_unfunded_amount':float(gap_amount.mean()),
      'terminal_histogram':{'counts':np.histogram(history[:,-1],bins=24)[0].tolist(),'edges':np.histogram(history[:,-1],bins=24)[1].tolist()},
      'warnings':['Model-implied frequency, NOT an empirically calibrated real-world probability.','Constant drift, volatility and correlation; monthly rebalancing; ignores jumps, taxes, fees and transaction costs.',
      'Drift is an annualized continuous arithmetic drift parameter. All cashflows enter at month-end.',
      'Values are nominal, not inflation-adjusted. Insolvency is recorded as an unfunded gap, not credit.',
      'Do not extend this liquid-sleeve model to private businesses, property, pensions or total household net worth without appropriate assumptions.']}
