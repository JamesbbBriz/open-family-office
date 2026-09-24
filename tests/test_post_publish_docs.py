import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("post_publish_docs", ROOT / "scripts/post_publish_docs.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class PostPublishDocsTests(unittest.TestCase):
    def test_git_uvx_becomes_pypi_uvx(self):
        source = (
            "uvx --from git+https://github.com/JamesbbBriz/open-family-office.git "
            "ofo demo --open"
        )
        self.assertEqual("uvx open-family-office demo --open", MODULE.transform(source))

    def test_tool_and_pipx_specs_become_pypi_project(self):
        source = "\n".join(
            [
                "uv tool install git+https://github.com/JamesbbBriz/open-family-office.git",
                "pipx install git+https://github.com/JamesbbBriz/open-family-office.git",
            ]
        )
        result = MODULE.transform(source)
        self.assertIn("uv tool install open-family-office", result)
        self.assertIn("pipx install open-family-office", result)
        self.assertNotIn("git+https://github.com/JamesbbBriz/open-family-office.git", result)

    def test_plain_git_clone_url_is_not_changed(self):
        source = "git clone https://github.com/JamesbbBriz/open-family-office.git"
        self.assertEqual(source, MODULE.transform(source))


if __name__ == "__main__":
    unittest.main()
