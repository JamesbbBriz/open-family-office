import json
import re
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCP_NAME = "io.github.jamesbbbriz/open-family-office"


class ReleaseMetadataTests(unittest.TestCase):
    def test_versions_and_distribution_metadata_stay_in_sync(self):
        pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        version = pyproject["project"]["version"]

        package_init = (ROOT / "src/open_family_office/__init__.py").read_text(encoding="utf-8")
        init_version = re.search(r'__version__\s*=\s*"([^"]+)"', package_init).group(1)

        package_json = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        server = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))

        self.assertEqual(version, init_version)
        self.assertEqual(version, package_json["version"])
        self.assertEqual(version, server["version"])
        self.assertEqual(version, server["packages"][0]["version"])

    def test_pypi_and_mcp_identifiers_are_canonical(self):
        pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        scripts = pyproject["project"]["scripts"]
        server = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))

        self.assertEqual("open-family-office", pyproject["project"]["name"])
        self.assertEqual("open_family_office.cli:main", scripts["ofo"])
        self.assertEqual("open_family_office.cli:main", scripts["open-family-office"])
        self.assertEqual(MCP_NAME, server["name"])
        self.assertEqual("pypi", server["packages"][0]["registryType"])
        self.assertEqual("open-family-office", server["packages"][0]["identifier"])
        self.assertEqual("uvx", server["packages"][0]["runtimeHint"])
        self.assertEqual("stdio", server["packages"][0]["transport"]["type"])

    def test_mcp_workspace_is_explicit_and_read_only_boundary_is_documented(self):
        server = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))
        env = {item["name"]: item for item in server["packages"][0]["environmentVariables"]}
        self.assertIn("OFO_WORKSPACE", env)
        self.assertTrue(env["OFO_WORKSPACE"]["isRequired"])

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"mcp-name: {MCP_NAME}", readme)
        self.assertIn("read-only", readme.lower())

    def test_server_json_has_no_remote_transport_or_secret_value(self):
        server = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))
        package = server["packages"][0]
        self.assertEqual({"type": "stdio"}, package["transport"])
        for item in package.get("environmentVariables", []):
            self.assertNotIn("value", item)


if __name__ == "__main__":
    unittest.main()
