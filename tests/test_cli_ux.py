from __future__ import annotations
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from open_family_office import __version__
from open_family_office.agent_kit import agent_kit_status, sync_agent_kit
from open_family_office.cli import find_workspace, main
from open_family_office.resources import public_page, resource_path


class CliUxTests(unittest.TestCase):
    def test_resources_available(self):
        self.assertTrue(resource_path("agent/templates/household.json").is_file())
        self.assertTrue(resource_path(".agents/skills/ofo-start/SKILL.md").is_file())
        self.assertTrue(public_page("demo.html").is_file())

    def test_init_creates_private_workspace_and_agent_kit(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / "family"
            self.assertEqual(main(["init", str(ws)]), 0)
            self.assertTrue((ws / "household.json").is_file())
            self.assertTrue((ws / ".ofo/workspace.json").is_file())
            self.assertTrue((ws / ".agents/skills/ofo-start/SKILL.md").is_file())
            self.assertTrue((ws / "agent/workflows/setup.md").is_file())
            status = agent_kit_status(ws)
            self.assertEqual(status["installed_version"], __version__)
            self.assertGreater(status["managed_files"], 10)

    def test_workspace_discovery_from_child_directory(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / "family"
            main(["init", str(ws), "--no-agent"])
            child = ws / "reports"
            old = Path.cwd()
            try:
                os.chdir(child)
                self.assertEqual(find_workspace(), ws.resolve())
            finally:
                os.chdir(old)

    def test_agent_sync_preserves_user_modified_skill(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / "family"
            main(["init", str(ws)])
            skill = ws / ".agents/skills/ofo-start/SKILL.md"
            skill.write_text(skill.read_text(encoding="utf-8") + "\n# my local note\n", encoding="utf-8")
            result = sync_agent_kit(ws)
            self.assertIn(".agents/skills/ofo-start/SKILL.md", result["conflicts"])
            self.assertIn("# my local note", skill.read_text(encoding="utf-8"))

    def test_mcp_config_uses_explicit_workspace_without_secret_values(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / "family"
            main(["init", str(ws), "--no-agent"])
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["mcp-config", "--workspace", str(ws)]), 0)
            data = json.loads(output.getvalue())
            server = data["mcpServers"]["open-family-office"]
            self.assertEqual(server["env"]["OFO_WORKSPACE"], str(ws.resolve()))
            self.assertEqual(server["args"][-1], "mcp")
            self.assertNotIn("API_KEY", output.getvalue())

    def test_status_does_not_print_household_values(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / "family"
            main(["init", str(ws), "--no-agent"])
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["status", "--workspace", str(ws)]), 0)
            data = json.loads(output.getvalue())
            self.assertIn(data["household"], {"ready", "needs_setup"})
            self.assertNotIn("net_worth", data)


if __name__ == "__main__":
    unittest.main()
