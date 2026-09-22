from __future__ import annotations
import numpy as np
from scipy.optimize import minimize, linprog
from ..core import InputError

def inputs(spec):
    labels=spec.get('assets',[]); x=np.asarray(spec.get('returns',[]),dtype=float)
    if spec.get('universe_type')!='liquid_proxy_research':
        raise InputError('Declare universe_type=liquid_proxy_research. Private assets/pensions must not be silently optimized as liquid assets.')
    if x.ndim!=2 or x.shape[0]<24 or x.shape[1]!=len(labels) or len(labels)<2 or len(set(labels))!=len(labels):
        raise InputError('Need at least 24 complete periods and two uniquely named liquid assets')
    if len(labels)>50 or len(x)>10000:raise InputError('Research size limit: 50 assets, 10,000 observations')
    if not np.isfinite(x).all() or (x<=-1).any():raise InputError('Returns must be finite decimal simple returns greater than -1')
    f=spec.get('periods_per_year')
    if type(f) is not int or f not in (12,52,252):raise InputError('Set periods_per_year to 12, 52 or 252; no implicit frequency')
    dates=spec.get('dates')
    if dates is not None:
        if len(dates)!=len(x) or dates!=sorted(set(dates)):raise InputError('Dates must be unique, chronological and match return rows')
        asof=spec.get('as_of')
        if asof and dates[-1]>asof:raise InputError('Future returns cannot enter an as-of research run')
    maximum=float(spec.get('max_weight',1))
    if not np.isfinite(maximum) or not 0<maximum<=1 or maximum*len(labels)<1-1e-12:raise InputError('Infeasible max_weight constraint')
    mu=x.mean(axis=0)*f
    from sklearn.covariance import LedoitWolf
    cov=LedoitWolf().fit(x).covariance_*f
    return labels,x,f,maximum,mu,cov

def optimize(spec,engine='scipy',method='min_variance'):
    labels,x,f,cap,mu,cov=inputs(spec); n=len(labels)
    beta=float(spec.get('confidence',.95))
    if not np.isfinite(beta) or not .5<beta<1:raise InputError('CVaR confidence must be between .5 and 1')
    if engine=='scipy':
        bounds=[(0,cap)]*n; cons=[{'type':'eq','fun':lambda w:w.sum()-1}]
        if method=='min_variance':
            result=minimize(lambda w:float(w@cov@w),np.ones(n)/n,jac=lambda w:2*cov@w,bounds=bounds,constraints=cons,method='SLSQP',options={'ftol':1e-12,'maxiter':1000})
            if not result.success:raise InputError('Optimization failed: '+result.message)
            weights=result.x
        elif method=='risk_parity':
            def loss(w):
                rc=w*(cov@w);return float(np.sum((rc-rc.sum()/n)**2))*10000
            result=minimize(loss,np.ones(n)/n,bounds=bounds,constraints=cons,method='SLSQP',options={'ftol':1e-12,'maxiter':1000})
            if not result.success:raise InputError('Risk parity failed')
            weights=result.x
        elif method=='cvar':
            beta=float(spec.get('confidence',.95))
            if not .5<beta<1:raise InputError('CVaR confidence must be between .5 and 1')
            t=len(x)
            if t>2500:raise InputError('SciPy dense CVaR wrapper is limited to 2,500 periods; use a sparse/native solver for larger research')
            objective=np.r_[np.zeros(n),1,np.ones(t)/((1-beta)*t)]
            # u_t >= -r_t.w - VaR. Minimize VaR + average positive tail excess.
            A=np.c_[-x,-np.ones(t),-np.eye(t)]; b=np.zeros(t)
            equality=np.zeros((1,n+1+t));equality[0,:n]=1
            result=linprog(objective,A_ub=A,b_ub=b,A_eq=equality,b_eq=[1],bounds=bounds+[(None,None)]+[(0,None)]*t,method='highs')
            if not result.success:raise InputError('CVaR optimization is infeasible')
            weights=result.x[:n]
        else:raise InputError('Scipy methods: min_variance, risk_parity, cvar')
    elif engine=='pypfopt':
        try:
            import pandas as pd
            from pypfopt import EfficientFrontier, HRPOpt, EfficientCVaR, BlackLittermanModel
        except ImportError:raise InputError('Install quant extra to run PyPortfolioOpt') from None
        frame=pd.DataFrame(x,columns=labels); covariance=pd.DataFrame(cov,index=labels,columns=labels)
        if method=='hrp':
            if cap<1:raise InputError('HRP wrapper does not enforce max_weight; use another method')
            model=HRPOpt(returns=frame);solved=model.optimize();weights=np.array([solved[a] for a in labels])
        elif method=='cvar':
            model=EfficientCVaR(mu,frame,beta=float(spec.get('confidence',.95)),weight_bounds=(0,cap));model.min_cvar();weights=np.array(model.weights)
        else:
            expected=mu
            if method=='black_litterman':
                views=spec.get('views');prior=spec.get('prior_returns')
                if not views or prior is None or len(prior)!=n:raise InputError('Black-Litterman requires explicit annual prior_returns and user views with confidence; no AI-invented inputs')
                keys=list(views)
                if not set(keys)<=set(labels):raise InputError('Unknown asset in views')
                confidences=[float(views[k]['confidence']) for k in keys]
                if any(not 0<c<=1 for c in confidences):raise InputError('View confidence must be in (0,1]')
                bl=BlackLittermanModel(covariance,pi=pd.Series(prior,index=labels),absolute_views={k:float(views[k]['annual_return']) for k in keys},omega='idzorek',view_confidences=confidences)
                expected=bl.bl_returns()
            elif method!='min_variance':raise InputError('PyPortfolioOpt methods: min_variance, cvar, hrp, black_litterman')
            model=EfficientFrontier(expected,covariance,weight_bounds=(0,cap))
            if method=='black_litterman':model.max_quadratic_utility(risk_aversion=float(spec.get('risk_aversion',3)))
            else:model.min_volatility()
            weights=np.array(model.weights)
    elif engine=='skfolio':
        try:
            from skfolio import RiskMeasure
            from skfolio.optimization import MeanRisk, ObjectiveFunction, RiskBudgeting
        except ImportError:raise InputError('Install quant extra to run skfolio') from None
        if method=='risk_parity':model=RiskBudgeting(min_weights=0,max_weights=cap)
        elif method in ('cvar','min_variance'):
            model=MeanRisk(risk_measure=RiskMeasure.CVAR if method=='cvar' else RiskMeasure.VARIANCE,objective_function=ObjectiveFunction.MINIMIZE_RISK,min_weights=0,max_weights=cap,cvar_beta=beta)
        else:raise InputError('skfolio methods: cvar, min_variance, risk_parity')
        model.fit(x);weights=np.asarray(model.weights_)
    else:raise InputError('Unknown optimization engine')
    if not np.isfinite(weights).all() or abs(weights.sum()-1)>1e-5 or weights.min()<-1e-6 or weights.max()>cap+1e-5:raise InputError('Solver output failed feasibility checks')
    actual=x@weights; loss=-actual; var=float(np.quantile(loss,.95));tail=loss[loss>=var]
    return {'engine':engine,'method':method,'weights':dict(zip(labels,map(float,weights))),
      'annualized_in_sample_return':float(mu@weights),'annualized_in_sample_volatility':float(np.sqrt(weights@cov@weights)),
      'period_var_95':var,'period_cvar_95':float(tail.mean()),'periods_per_year':f,'observations':len(x),
      'synthetic':spec.get('synthetic',False),'warnings':['In-sample research, not a forecast or recommended household allocation.',
      'No tax, transaction costs, suitability or private-asset tradability is inferred.','Weights cover the liquid proxy sleeve only; ring-fence household reserves first.',
      'Mean estimates are arithmetic annualized; covariance uses Ledoit-Wolf shrinkage for reported metrics. Engine objectives may estimate covariance differently.']}

def frontier(spec,points=20):
    labels,x,f,cap,mu,cov=inputs(spec)
    base=optimize(spec);w0=np.array(list(base['weights'].values()));minimum=float(mu@w0)
    maximum_result=linprog(-mu,A_eq=np.ones((1,len(labels))),b_eq=[1],bounds=[(0,cap)]*len(labels),method='highs')
    if not maximum_result.success:raise InputError('No feasible frontier')
    maximum=float(mu@maximum_result.x)
    out=[]
    for target in np.linspace(minimum,maximum,points):
        result=minimize(lambda w:float(w@cov@w),w0,bounds=[(0,cap)]*len(labels),constraints=[{'type':'eq','fun':lambda w:w.sum()-1},{'type':'eq','fun':lambda w,t=target:mu@w-t}],method='SLSQP',options={'ftol':1e-11,'maxiter':1000})
        if result.success:out.append({'return':float(mu@result.x),'volatility':float(np.sqrt(result.x@cov@result.x)),'weights':dict(zip(labels,map(float,result.x)))})
    return {'points':out,'label':'In-sample efficient frontier; synthetic proxy returns' if spec.get('synthetic') else 'In-sample efficient frontier; not forward expected performance'}
