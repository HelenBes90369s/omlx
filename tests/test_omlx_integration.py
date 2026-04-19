"""Integration tests for omlx CLI commands."""

import os
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import omlx


class TestIntegration(unittest.TestCase):
    """Integration tests that simulate real CLI usage."""

    def setUp(self):
        """Set up a temporary directory for each test."""
        self.test_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.test_dir, "config.json")
        # Patch CONFIG_PATH to use temp directory
        self.patcher = patch("omlx.CONFIG_PATH", self.config_path)
        self.patcher.start()

    def tearDown(self):
        """Clean up temporary directory."""
        self.patcher.stop()
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_full_add_list_remove_cycle(self):
        """Test a complete add -> list -> remove workflow."""
        # Add an app
        omlx.add_app("TestApp", "https://example.com/testapp.dmg")

        # Verify it appears in list
        apps = omlx.list_apps()
        self.assertIn("TestApp", [a["name"] for a in apps])

        # Remove the app
        omlx.remove_app("TestApp")

        # Verify it no longer appears
        apps = omlx.list_apps()
        self.assertNotIn("TestApp", [a["name"] for a in apps])

    def test_add_multiple_apps(self):
        """Test adding multiple apps and listing them all."""
        apps_to_add = [
            ("AppOne", "https://example.com/appone.dmg"),
            ("AppTwo", "https://example.com/apptwo.dmg"),
            ("AppThree", "https://example.com/appthree.dmg"),
        ]

        for name, url in apps_to_add:
            omlx.add_app(name, url)

        apps = omlx.list_apps()
        names = [a["name"] for a in apps]

        for name, _ in apps_to_add:
            self.assertIn(name, names)

        self.assertEqual(len(apps), len(apps_to_add))

    def test_config_persists_between_calls(self):
        """Test that config changes persist across load/save cycles."""
        omlx.add_app("PersistApp", "https://example.com/persist.dmg")

        # Reload config from disk
        config = omlx.load_config()
        names = [a["name"] for a in config.get("apps", [])]
        self.assertIn("PersistApp", names)

    def test_remove_nonexistent_app_is_safe(self):
        """Test that removing a non-existent app does not raise an error."""
        try:
            omlx.remove_app("NonExistentApp")
        except Exception as e:
            self.fail(f"remove_app raised an exception for missing app: {e}")

    def test_duplicate_add_does_not_create_duplicates(self):
        """Test that adding the same app twice does not duplicate it."""
        omlx.add_app("DupeApp", "https://example.com/dupe.dmg")
        omlx.add_app("DupeApp", "https://example.com/dupe.dmg")

        apps = omlx.list_apps()
        names = [a["name"] for a in apps]
        self.assertEqual(names.count("DupeApp"), 1)

    def test_config_file_is_valid_json(self):
        """Test that the config file written to disk is valid JSON."""
        omlx.add_app("JsonApp", "https://example.com/json.dmg")

        with open(self.config_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                self.fail("Config file is not valid JSON")

        self.assertIn("apps", data)


if __name__ == "__main__":
    unittest.main()
