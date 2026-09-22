from pathlib import Path
from copy import deepcopy
import json
import re
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
sys.path.insert(0,str(ROOT/'scripts'))
from release_check import check
from open_family_office.core import InputError,cashflow,allocation,snapshot,stress
from open_family_office.io import read_json

class ArtifactTests(unittest.TestCase):
    def test_skills_have_frontmatter_and_workflow(self):
        paths=list((ROOT/'.agents/skills').glob('*/SKILL.md'))
        self.assertEqual(len(paths),10)
        for p in paths:
            content=p.read_text();self.assertTrue(content.startswith('---\n'));self.assertIn(f'name: {p.parent.name}\n',content)
            self.assertIn('agent/workflows/',content)
            self.assertTrue((ROOT/'.claude/skills'/p.parent.name/'SKILL.md').exists())
            self.assertTrue((ROOT/'.claude/commands'/f'{p.parent.name}.md').exists())
    def test_release_hygiene(self):
        self.assertEqual(check(),[])
    def test_all_examples_are_synthetic(self):
        for p in (ROOT/'examples').glob('household*.json'):
            self.assertIs(read_json(p)['synthetic'],True)
    def test_registry_truth(self):
        implemented=[p['id'] for p in read_json(ROOT/'docs/integrations/provider-registry.json')['providers'] if p['status']=='implemented']
        self.assertIn('manual-json',implemented);self.assertIn('cashflow-csv',implemented)
    def test_no_network_import_in_engine(self):
        for p in (ROOT/'src/open_family_office').glob('*.py'):
            self.assertNotRegex(p.read_text(),r'(?m)^\s*(?:from|import)\s+(?:requests|httpx|urllib|socket|aiohttp)\b')
    def test_schema_loads(self):
        schema=read_json(ROOT/'agent/schemas/household.schema.json');self.assertIn('$schema',schema);self.assertIs(schema['additionalProperties'],False)
    def test_recession_golden_output(self):
        h=read_json(ROOT/'examples/household.synthetic.json');s=read_json(ROOT/'examples/scenarios/recession.json')
        expected=read_json(ROOT/'examples/expected/recession.json');actual=stress(h,s)
        self.assertEqual(expected['snapshot'],actual['instant_price_shock_snapshot']);self.assertEqual(expected['forecast'],actual['cashflow'])
    def test_sale_golden_output(self):
        h=read_json(ROOT/'examples/household.synthetic.json');s=read_json(ROOT/'examples/scenarios/business-sale.json')
        self.assertEqual(read_json(ROOT/'examples/expected/business-sale.json')['forecast'],cashflow(h,24,s))
    def test_empty_scenario_maps_not_lists(self):
        h=read_json(ROOT/'examples/household.synthetic.json');s=read_json(ROOT/'examples/scenarios/recession.json');s['asset_shocks']=[]
        self.assertRaises(InputError,cashflow,h,24,s)
    def test_targets_not_list(self):
        h=read_json(ROOT/'examples/household.synthetic.json');p=read_json(ROOT/'examples/policy.synthetic.json');p['targets']=[]
        self.assertRaises(InputError,allocation,h,p)
    def test_months_table_in_embedded_demo(self):
        content=(ROOT/'public/demo.html').read_text();self.assertNotIn('__DEMO_DATA__',content);self.assertIn('"closing_cash": "899000.00"',content);self.assertIn('plotly.js v3.3.1',content)
    def test_readme_does_not_claim_live_adapters(self):
        self.assertIn('No API key, model account or network call is needed for the synthetic demo.',(ROOT/'README.md').read_text())

if __name__=='__main__':unittest.main()
