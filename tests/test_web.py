from pathlib import Path
import json,re,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_dashboard import render,payload
from household_cio.io import read_json

class StaticWebTests(unittest.TestCase):
    def test_landing_and_demo_are_distinct(self):
        landing=(ROOT/'public/index.html').read_text();demo=(ROOT/'public/demo.html').read_text()
        self.assertIn('Your whole',landing);self.assertIn('id="sandboxForm"',demo)
        self.assertNotIn('id="sandboxForm"',landing)
    def test_built_placeholders_resolved(self):
        for name in ['index.html','demo.html']:
            s=(ROOT/'public'/name).read_text()
            self.assertNotRegex(s,r'__(?:TAILWIND_CSS|SHARED_CSS|APP_CSS|APP_JS|SANDBOX_MATH|LANDING_JS|SOURCE_HREF|PREVIEW_CHART)__')
    def test_no_runtime_cdn_or_remote_styles(self):
        for name in ['index.html','demo.html']:
            s=(ROOT/'public'/name).read_text()
            self.assertNotRegex(s,r'<script[^>]+src=')
            self.assertNotRegex(s,r'<link[^>]+rel=["\']stylesheet')
            self.assertIn("connect-src 'none'",s)
    def test_privacy_no_persist_or_fetch_in_app_source(self):
        for name in ['sandbox.js','landing.js','dashboard.js']:
            s=(ROOT/'site'/name).read_text()
            self.assertNotRegex(s,r'\b(?:fetch|XMLHttpRequest|WebSocket|localStorage|sessionStorage|indexedDB)\b')
    def test_six_views_and_fourteen_chart_nodes(self):
        s=(ROOT/'site/dashboard.html').read_text()
        self.assertEqual(len(re.findall(r'id="tab-[^" ]+"',s)),6)
        self.assertEqual(len(re.findall(r'id="[A-Za-z]+Chart"',s)),14)
    def test_new_upstream_notice_present(self):
        self.assertTrue((ROOT/'vendor/licenses/daisyui-MIT.txt').exists())
        self.assertIn('source-derived',(ROOT/'vendor/daisyui/components.source.css').read_text())
    def test_private_export_has_new_components_without_placeholder_injection(self):
        h=read_json(ROOT/'examples/household.synthetic.json');h['name']='__SHARED_CSS__ </script>'
        s=render(payload(h))
        self.assertIn('"name": "__SHARED_CSS__ \\u003c/script\\u003e"',s)
        self.assertIn('OFOCash',s)
    def test_no_fake_repo_is_configured(self):
        config=json.loads((ROOT/'config/site.json').read_text())
        self.assertIsNone(config['repository_url'])

if __name__=='__main__':unittest.main()
