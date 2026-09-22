import copy,importlib.util,unittest
import numpy as np
from pathlib import Path
from household_cio.io import read_json
from household_cio.core import InputError
from household_cio.quant.allocation import optimize,frontier,inputs
from household_cio.quant.simulation import simulate
from household_cio.quant.ownership import consolidate,exposures
ROOT=Path(__file__).resolve().parents[1]
class QuantTests(unittest.TestCase):
    def setUp(self):self.spec=read_json(ROOT/'examples/returns.synthetic.json')
    def test_min_variance_feasible(self):
        r=optimize(self.spec);self.assertAlmostEqual(sum(r['weights'].values()),1,6);self.assertLessEqual(max(r['weights'].values()),.600001)
    def test_cvar_feasible(self):
        r=optimize(self.spec,method='cvar');self.assertAlmostEqual(sum(r['weights'].values()),1,6)
        self.assertGreaterEqual(r['period_cvar_95'],r['period_var_95'])
    def test_risk_parity_feasible(self):
        r=optimize(self.spec,method='risk_parity');self.assertAlmostEqual(sum(r['weights'].values()),1,6)
    def test_min_variance_beats_equal_weight_for_objective(self):
        labels,x,f,cap,mu,cov=inputs(self.spec);r=optimize(self.spec);w=np.array(list(r['weights'].values()));e=np.ones(len(w))/len(w)
        self.assertLessEqual(float(w@cov@w),float(e@cov@e)+1e-8)
    def test_frontier_monotone(self):
        rows=frontier(self.spec,12)['points'];self.assertGreaterEqual(len(rows),10)
        self.assertTrue(all(b['return']>=a['return']-1e-7 for a,b in zip(rows,rows[1:])))
        self.assertTrue(all(b['volatility']>=a['volatility']-1e-6 for a,b in zip(rows,rows[1:])))
    def test_nonliquid_universe_rejected(self):
        self.spec['universe_type']='entire_household';self.assertRaises(InputError,optimize,self.spec)
    def test_frequency_required(self):
        del self.spec['periods_per_year'];self.assertRaises(InputError,optimize,self.spec)
    def test_no_nan(self):
        self.spec['returns'][0][0]=float('nan');self.assertRaises(InputError,optimize,self.spec)
    def test_total_loss_return_rejected(self):
        self.spec['returns'][0][0]=-1;self.assertRaises(InputError,optimize,self.spec)
    def test_infeasible_cap(self):
        self.spec['max_weight']=.1;self.assertRaises(InputError,optimize,self.spec)
    def test_duplicate_dates_rejected(self):
        self.spec['dates'][1]=self.spec['dates'][0];self.assertRaises(InputError,optimize,self.spec)
    def test_future_data_rejected(self):
        self.spec['as_of']='2019-01-01';self.assertRaises(InputError,optimize,self.spec)
    @unittest.skipUnless(importlib.util.find_spec('pypfopt'),'PyPortfolioOpt not installed: native optimizer not verified')
    def test_pypfopt_native_methods(self):
        for method in ('min_variance','cvar','black_litterman'):
            self.assertAlmostEqual(sum(optimize(self.spec,'pypfopt',method)['weights'].values()),1,5)
    @unittest.skipUnless(importlib.util.find_spec('skfolio'),'skfolio not installed: native optimizer not verified')
    def test_skfolio_native_methods(self):
        for method in ('min_variance','cvar','risk_parity'):
            self.assertAlmostEqual(sum(optimize(self.spec,'skfolio',method)['weights'].values()),1,5)
class SimulationTests(unittest.TestCase):
    def setUp(self):
        self.spec=read_json(ROOT/'examples/simulation.synthetic.json');self.spec['months']=24;self.spec['paths']=100;self.spec['monthly_net_cashflows']=[1000]*24
    def test_reproducible_seed(self):
        self.assertEqual(simulate(self.spec),simulate(self.spec))
    def test_percentiles_ordered(self):
        r=simulate(self.spec)
        for p in r['percentiles']:self.assertTrue(p['p05']<=p['p25']<=p['p50']<=p['p75']<=p['p95'])
    def test_initial_value_exact(self):
        p=simulate(self.spec)['percentiles'][0];self.assertEqual(p['p50'],self.spec['initial_capital'])
    def test_zero_vol_zero_drift_reconciles_cash(self):
        self.spec['annual_drift']=[0]*5;self.spec['annual_volatility']=[0]*5
        r=simulate(self.spec);self.assertAlmostEqual(r['percentiles'][-1]['p50'],344000)
    def test_overspend_does_not_create_overdraft(self):
        self.spec['initial_capital']=1;self.spec['monthly_net_cashflows']=[-10000]*24
        r=simulate(self.spec);self.assertEqual(r['simulated_paths_with_unfunded_gap_fraction'],1);self.assertGreaterEqual(r['percentiles'][-1]['p05'],0)
    def test_invalid_correlation_rejected(self):
        self.spec['correlation'][0][1]=4;self.assertRaises(InputError,simulate,self.spec)
    def test_whole_household_sim_rejected(self):
        self.spec['scope']='whole_household';self.assertRaises(InputError,simulate,self.spec)
    def test_cashflow_length_rejected(self):
        self.spec['monthly_net_cashflows']=[];self.assertRaises(InputError,simulate,self.spec)
class OwnershipTests(unittest.TestCase):
    def setUp(self):self.graph=read_json(ROOT/'examples/ownership.synthetic.json')
    def test_attribution_and_debt(self):
        self.assertEqual(consolidate(self.graph)['net_value_base'],'820000.00')
    def test_parent_and_child_not_counted_twice(self):
        self.graph['nodes'][1]['value_base']='1000000';self.assertRaises(InputError,consolidate,self.graph)
    def test_cycle_rejected(self):
        self.graph['edges'].append({'owner':'trust','owned':'holding','share':'0.1'});self.assertRaises(InputError,consolidate,self.graph)
    def test_multiple_ownership_above_one_rejected(self):
        self.graph['edges'].append({'owner':'family','owned':'trust','share':'0.5'});self.assertRaises(InputError,consolidate,self.graph)
    def test_unknown_exposure_is_preserved(self):
        r=exposures(read_json(ROOT/'examples/exposures.synthetic.json')['positions']);self.assertGreater(float(r['dimensions']['geography']['unknown']['amount']),0)
    def test_overlapping_dimensions_not_summed(self):
        r=exposures(read_json(ROOT/'examples/exposures.synthetic.json')['positions']);self.assertEqual(r['gross_assets'],'2200000.00')
if __name__=='__main__':unittest.main()
