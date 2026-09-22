from pathlib import Path
import json,sys,tempfile,unittest
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
sys.path.insert(0,str(ROOT/'scripts'))
from build_dashboard import payload,render,export_dashboard
from open_family_office.io import read_json
from open_family_office.core import InputError

class DashboardTests(unittest.TestCase):
    def setUp(self):self.h=read_json(ROOT/'examples/household.synthetic.json')
    def test_no_optional_data_is_not_fabricated(self):
        data=payload(self.h)
        self.assertIsNone(data['quant']);self.assertIsNone(data['simulation']);self.assertIsNone(data['allocation'])
    def test_untrusted_text_cannot_close_data_script(self):
        self.h['name']='</script><script>window.injected=true</script>'
        html=render(payload(self.h))
        self.assertNotIn(self.h['name'],html)
        self.assertIn('\\u003c/script\\u003e',html)
        self.assertIn('THIRD PARTY LICENSES',html)
    def test_private_output_outside_repo_and_no_overwrite(self):
        self.h['synthetic']=False
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'report.html';export_dashboard(self.h,p)
            html=p.read_text();self.assertIn('"synthetic": false',html)
            with self.assertRaises((InputError,FileExistsError)):export_dashboard(self.h,p)
    def test_private_output_inside_repo_rejected(self):
        self.assertRaises(InputError,export_dashboard,self.h,ROOT/'workspace-report.html')
    def test_currency_not_fixed_in_runtime_code(self):
        script=(ROOT/'web/src/dashboard.js').read_text()
        self.assertIn('const currency=DATA.household.base_currency',script)
        self.assertNotIn("const money=n=>'A$'",script)
    def test_disposal_data_reconciles(self):
        scenario=read_json(ROOT/'examples/scenarios/business-sale.json')
        data=payload(self.h,[scenario]);b=data['cases']['business-sale']['forecast']['event_bridges'][0]
        self.assertEqual(float(b['net_cash_received'])-float(b['equity_asset_removed']),float(b['event_net_worth_delta']))
if __name__=='__main__':unittest.main()
