"""Unit tests for omlx.py core functionality."""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from omlx import load_config, save_config, list_apps, add_app, remove_app


CONFIG_TEMPLATE = {
    "apps": []
}


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.tmpdir, "config.json")

    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.tmpdir)

    def test_load_config_creates_default_when_missing(self):
        config = load_config(self.config_path)
        self.assertIn("apps", config)
        self.assertIsInstance(config["apps"], list)

    def test_save_and_load_config(self):
        data = {"apps": [{"name": "test-app", "url": "https://example.com"}]}
        save_config(data, self.config_path)
        loaded = load_config(self.config_path)
        self.assertEqual(loaded["apps"][0]["name"], "test-app")

    def test_load_config_returns_existing_data(self):
        with open(self.config_path, "w") as f:
            json.dump({"apps": [{"name": "existing"}]}, f)
        config = load_config(self.config_path)
        self.assertEqual(len(config["apps"]), 1)
        self.assertEqual(config["apps"][0]["name"], "existing")


class TestAppManagement(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.tmpdir, "config.json")
        save_config({"apps": []}, self.config_path)

    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.tmpdir)

    def test_add_app(self):
        add_app("myapp", "https://example.com/myapp", self.config_path)
        config = load_config(self.config_path)
        names = [a["name"] for a in config["apps"]]
        self.assertIn("myapp", names)

    def test_add_duplicate_app_raises(self):
        add_app("myapp", "https://example.com/myapp", self.config_path)
        with self.assertRaises(ValueError):
            add_app("myapp", "https://example.com/myapp2", self.config_path)

    def test_remove_app(self):
        add_app("myapp", "https://example.com/myapp", self.config_path)
        remove_app("myapp", self.config_path)
        config = load_config(self.config_path)
        names = [a["name"] for a in config["apps"]]
        self.assertNotIn("myapp", names)

    def test_remove_nonexistent_app_raises(self):
        with self.assertRaises(ValueError):
            remove_app("ghost", self.config_path)

    def test_list_apps_empty(self):
        apps = list_apps(self.config_path)
        self.assertEqual(apps, [])

    def test_list_apps_returns_all(self):
        add_app("app1", "https://example.com/app1", self.config_path)
        add_app("app2", "https://example.com/app2", self.config_path)
        apps = list_apps(self.config_path)
        self.assertEqual(len(apps), 2)


if __name__ == "__main__":
    unittest.main()
