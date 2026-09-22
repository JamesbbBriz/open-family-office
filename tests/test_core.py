from __future__ import annotations
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest
from open_family_office.core import InputError, validate, snapshot, cashflow, stress, allocation, number
from open_family_office.io import read_json, write_new, REPO_ROOT
from open_family_office.cli import main

class CoreTests(unittest.TestCase):
    def setUp(self):
        self.h = read_json(REPO_ROOT/'examples/household.synthetic.json')
        self.sale = read_json(REPO_ROOT/'examples/scenarios/business-sale.json')
        self.recession = read_json(REPO_ROOT/'examples/scenarios/recession.json')
        self.policy = read_json(REPO_ROOT/'examples/policy.synthetic.json')
    def test_snapshot_totals(self):
        s=snapshot(self.h); self.assertEqual(s['gross_assets'],'2500000.00'); self.assertEqual(s['net_worth'],'1800000.00')
    def test_spendable_cash(self):
        self.assertEqual(snapshot(self.h)['spendable_cash'],'120000.00')
    def test_notice_cash_is_not_spendable_today(self):
        self.h['assets'][0]['liquidity_days']=30;self.assertEqual(snapshot(self.h)['spendable_cash'],'0.00')
    def test_reserve_cannot_use_notice_cash(self):
        self.h['assets'][0]['liquidity_days']=30;self.assertRaises(InputError,allocation,self.h,self.policy)
    def test_haircuts(self):
        self.assertEqual(snapshot(self.h)['available_within_7_days_after_haircuts'],'416000.00')
    def test_pension_not_extra_asset_class(self):
        s=snapshot(self.h);self.assertEqual(s['asset_classes']['equity'],'400000.00');self.assertNotIn('pension',s['asset_classes']);self.assertEqual(s['wrappers']['pension'],'180000.00')
    def test_baseline_cash(self):
        self.assertEqual(cashflow(self.h)['ending_cash'],'94000.00')
    def test_one_off_not_annualized(self):
        out=cashflow(self.h);self.assertEqual(out['months_table'][5]['outflows'],'35000.00');self.assertEqual(out['months_table'][17]['outflows'],'11000.00')
    def test_sales_replace_equity(self):
        out=cashflow(self.h,24,self.sale);b=out['event_bridges'][0];self.assertEqual(b['equity_asset_removed'],'600000.00');self.assertEqual(b['event_net_worth_delta'],'300000.00')
    def test_sale_stops_business_income(self):
        rows=cashflow(self.h,24,self.sale)['months_table'];self.assertEqual(rows[4]['variable_income'],'5000.00');self.assertEqual(rows[5]['variable_income'],'0.00')
    def test_sale_cash(self):
        self.assertEqual(cashflow(self.h,24,self.sale)['ending_cash'],'899000.00')
    def test_valuation_shocks_do_not_spend_cash(self):
        s=deepcopy(self.recession);s['cashflow_multipliers']={};self.assertEqual(stress(self.h,s)['cashflow']['ending_cash'],'94000.00')
    def test_stress_markdown(self):
        out=stress(self.h,self.recession);self.assertEqual(out['instant_net_worth_change'],'-578000.00');self.assertEqual(out['cashflow']['ending_cash'],'22000.00')
    def test_asset_rich_cash_poor(self):
        self.h['assets'][0]['value']='20000';out=cashflow(self.h);self.assertEqual(out['first_shortfall'],'2027-06')
    def test_duplicates_rejected(self):
        self.h['assets'].append(deepcopy(self.h['assets'][0]));self.assertRaises(InputError,validate,self.h)
    def test_nan_rejected(self):
        self.h['assets'][0]['value']='NaN';self.assertRaises(InputError,validate,self.h)
    def test_infinity_rejected(self):
        self.assertRaises(InputError,number,'Infinity')
    def test_float_rejected(self):
        self.assertRaises(InputError,number,1.01)
    def test_boolean_rejected(self):
        self.assertRaises(InputError,number,True)
    def test_negative_asset_rejected(self):
        self.h['assets'][0]['value']='-1';self.assertRaises(InputError,validate,self.h)
    def test_missing_fx_rejected(self):
        self.h['assets'][0]['currency']='USD';self.assertRaises(InputError,validate,self.h)
    def test_fx_direction(self):
        self.h['assets'][0]['currency']='USD';self.h['fx']['USD']={'base_per_unit':'1.5','as_of':'2026-09-21','evidence_id':'demo-input'};self.assertEqual(snapshot(self.h)['spendable_cash'],'180000.00')
    def test_ownership_share(self):
        self.h['assets'][0]['ownership_share']='0.5';self.assertEqual(snapshot(self.h)['spendable_cash'],'60000.00')
    def test_liability_share(self):
        self.h['liabilities'][0]['ownership_share']='0.5';self.assertEqual(snapshot(self.h)['liabilities'],'350000.00')
    def test_pledged_cash(self):
        self.h['assets'][0]['restriction']='pledged';self.assertEqual(snapshot(self.h)['spendable_cash'],'0.00')
    def test_enterprise_value_rejected(self):
        self.h['assets'][4]['valuation_basis']='enterprise';self.assertRaises(InputError,validate,self.h)
    def test_future_valuation_rejected(self):
        self.h['assets'][0]['valuation_date']='2026-09-22';self.assertRaises(InputError,validate,self.h)
    def test_stale_valuation_flagged(self):
        self.h['assets'][0]['valuation_date']='2025-01-01';self.assertTrue(validate(self.h))
    def test_zero_income_valid(self):
        self.h['cashflows'][0]['amount']='0';validate(self.h)
    def test_invalid_recurrence_rejected(self):
        self.h['cashflows'][0]['nature']='one_off';self.assertRaises(InputError,validate,self.h)
    def test_double_sale_rejected(self):
        self.sale['sales']*=2;self.assertRaises(InputError,cashflow,self.h,24,self.sale)
    def test_unknown_scenario_target_rejected(self):
        self.recession['asset_shocks']['missing']='-0.1';self.assertRaises(InputError,stress,self.h,self.recession)
    def test_loss_over_100_percent_rejected(self):
        self.recession['asset_shocks']['home']='-1.1';self.assertRaises(InputError,stress,self.h,self.recession)
    def test_scenario_does_not_mutate_input(self):
        before=deepcopy(self.h);stress(self.h,self.sale);self.assertEqual(before,self.h)
    def test_allocation_reserve(self):
        self.assertEqual(allocation(self.h,self.policy)['residual_capital'],'360000.00')
    def test_allocation_targets_exact(self):
        self.policy['targets']['equity']='0.7';self.assertRaises(InputError,allocation,self.h,self.policy)
    def test_allocation_needs_confirmation(self):
        self.policy['status']='draft';self.assertRaises(InputError,allocation,self.h,self.policy)
    def test_allocation_insufficient_cash(self):
        self.policy['minimum_cash_reserve_base']='999999';self.assertRaises(InputError,allocation,self.h,self.policy)
    def test_missing_evidence_rejected(self):
        self.h['assets'][0]['evidence_id']='nope';self.assertRaises(InputError,validate,self.h)
    def test_unknown_field_rejected(self):
        self.h['predicted_annual_return']='25%';self.assertRaises(InputError,validate,self.h)
    def test_end_date(self):
        self.h['cashflows'][1]['end_date']='2026-10-31';out=cashflow(self.h,2);self.assertEqual(out['months_table'][1]['variable_income'],'0.00')
    def test_month_limit(self):
        self.assertRaises(InputError,cashflow,self.h,0);self.assertRaises(InputError,cashflow,self.h,121)
    def test_duplicate_json_keys_rejected(self):
        with TemporaryDirectory() as td:
            p=Path(td)/'x.json';p.write_text('{"a":1,"a":2}');self.assertRaises(InputError,read_json,p)
    def test_private_writes_outside_repo(self):
        self.assertRaises(InputError,write_new,REPO_ROOT/'private.json','{}')
    def test_exclusive_write(self):
        with TemporaryDirectory() as td:
            p=Path(td)/'x.md';write_new(p,'first');self.assertRaises(FileExistsError,write_new,p,'second')
    def test_cli_import(self):
        with TemporaryDirectory() as td:
            out=Path(td)/'imported.json'
            self.assertEqual(main(['import-csv',str(REPO_ROOT/'examples/import.synthetic.csv'),'--household',str(REPO_ROOT/'examples/household.synthetic.json'),'--out',str(out)]),0)
            self.assertEqual(len(read_json(out)['cashflows']),7)

if __name__=='__main__':unittest.main()
